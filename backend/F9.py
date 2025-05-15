from flask import Flask, request, jsonify
import os
import math
import numpy as np
from multiprocessing import Pool, cpu_count, Manager
from coordTransform_utils import wgs84_to_gcj02
from datetime import datetime
import time
import heapq

app = Flask(__name__)

# 使用slots减少内存占用
class TrajectoryNode:
    __slots__ = ['hour', 'lng', 'lat', 'timestamp']
    def __init__(self, hour, lng, lat, timestamp):
        self.hour = hour
        self.lng = lng
        self.lat = lat
        self.timestamp = timestamp

def calculate_distance(p1, p2):
    """快速距离计算（使用平方避免开方）"""
    return (p2[0] - p1[0])**2 + (p2[1] - p1[1])**2

def process_trajectory(args):
    """优化后的轨迹处理函数"""
    filename, area1, area2, result_dict = args
    hourly_stats = {}
    
    with open(filename, 'r') as f:
        current_taxi = None
        trajectory = []
        
        for line in f:
            # 使用快速分割方法
            parts = line.split(',', 3)
            if len(parts) < 4:
                continue
            
            try:
                taxi_id = parts[0]
                time_str = parts[1]
                lng, lat = wgs84_to_gcj02(float(parts[2]), float(parts[3]))
                hour = int(time_str[11:13])  # 直接提取小时部分
                
                if taxi_id != current_taxi:
                    if trajectory:
                        process_single_trajectory(trajectory, area1, area2, hourly_stats)
                    current_taxi = taxi_id
                    trajectory = []
                
                trajectory.append(TrajectoryNode(hour, lng, lat, time_str))
            except (ValueError, IndexError):
                continue
        
        if trajectory:
            process_single_trajectory(trajectory, area1, area2, hourly_stats)
    
    # 合并结果到共享字典
    for hour, stats in hourly_stats.items():
        if hour not in result_dict or stats['time'] < result_dict[hour]['time']:
            result_dict[hour] = stats

def process_single_trajectory(trajectory, area1, area2, hourly_stats):
    """处理单条轨迹的核心逻辑"""
    in_area1 = False
    path_segment = []
    a1_min_lng, a1_max_lng, a1_min_lat, a1_max_lat = area1
    a2_min_lng, a2_max_lng, a2_min_lat, a2_max_lat = area2
    
    for i, point in enumerate(trajectory):
        # 使用短路计算加速区域判断
        if not in_area1:
            if (a1_min_lng <= point.lng <= a1_max_lng and 
                a1_min_lat <= point.lat <= a1_max_lat):
                in_area1 = True
                path_segment = [(point.lng, point.lat)]
            continue
        
        path_segment.append((point.lng, point.lat))
        
        # 检查是否到达区域B
        if (a2_min_lng <= point.lng <= a2_max_lng and 
            a2_min_lat <= point.lat <= a2_max_lat):
            travel_time = len(path_segment)
            hour = point.hour
            
            # 更新当前处理线程的最短路径
            if hour not in hourly_stats or travel_time < hourly_stats[hour]['time']:
                hourly_stats[hour] = {
                    'path': path_segment.copy(),
                    'time': travel_time,
                    'count': 1
                }
            elif travel_time == hourly_stats[hour]['time']:
                hourly_stats[hour]['count'] += 1
            
            break

@app.route('/api/optimized_path', methods=['GET'])
def analyze_shortest_path():
    """优化后的API端点"""
    start_time = time.time()
    
    try:
        # 参数解析和验证
        area1 = tuple(map(float, request.args['area1'].split(',')))
        area2 = tuple(map(float, request.args['area2'].split(',')))
        folder_path = request.args.get('folder_path', 'taxi_log_2008_by_id')
        workers = min(int(request.args.get('workers', cpu_count())), cpu_count())
        
        # 坐标转换
        def convert_area(area):
            min_lng, max_lng, min_lat, max_lat = area
            return (
                wgs84_to_gcj02(min_lng, min_lat)[0],
                wgs84_to_gcj02(max_lng, max_lat)[0],
                wgs84_to_gcj02(min_lng, min_lat)[1],
                wgs84_to_gcj02(max_lng, max_lat)[1]
            )
        
        area1 = convert_area(area1)
        area2 = convert_area(area2)
        
        # 使用Manager共享结果
        with Manager() as manager:
            result_dict = manager.dict()
            
            # 准备任务
            files = [os.path.join(folder_path, f) 
                    for f in os.listdir(folder_path) 
                    if f.endswith('.txt')]
            
            # 并行处理
            with Pool(workers) as pool:
                pool.map(process_trajectory, 
                        [(f, area1, area2, result_dict) for f in files],
                        chunksize=10)
            
            # 构建响应
            response_data = []
            for hour in range(24):
                if hour in result_dict:
                    stats = result_dict[hour]
                    response_data.append({
                        "hour": hour,
                        "path": stats['path'],
                        "travel_time": stats['time'],
                        "sample_count": stats['count']
                    })
                else:
                    response_data.append({
                        "hour": hour,
                        "path": None,
                        "travel_time": -1,
                        "sample_count": 0
                    })
            
            return jsonify({
                "status": "success",
                "processing_time": round(time.time() - start_time, 2),
                "data": response_data,
                "params": {
                    "area1": area1,
                    "area2": area2,
                    "workers_used": workers
                }
            })
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "processing_time": round(time.time() - start_time, 2)
        }), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=False, processes=1)
