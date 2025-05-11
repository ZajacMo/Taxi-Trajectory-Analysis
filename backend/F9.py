"""
F9.py - 最短路径分析模块

该模块用于分析出租车轨迹数据中两个区域之间的最短通行路径和时间。
主要功能包括：
1. 计算两个坐标点之间的欧式距离
2. 分析区域A到区域B的最短通行路径及时间
"""
import json
import os
import math
from collections import defaultdict
import heapq

def calculate_distance(lng1, lat1, lng2, lat2):
    """
    计算两个坐标点之间的欧式距离（简化版）

    参数：
        lng1 (float): 第一个点的经度
        lat1 (float): 第一个点的纬度
        lng2 (float): 第二个点的经度
        lat2 (float): 第二个点的纬度

    返回：
        float: 两个点之间的欧式距离
    """
    return math.sqrt((lng2 - lng1)**2 + (lat2 - lat1)**2)

def analyze_shortest_path(folder_path, area1, area2):
    """
    分析区域A到区域B的最短通行路径及时间

    参数：
        folder_path (str): 包含出租车轨迹数据的文件夹路径
        area1 (tuple): 区域A的边界坐标 (min_lng, max_lng, min_lat, max_lat)
        area2 (tuple): 区域B的边界坐标 (min_lng, max_lng, min_lat, max_lat)

    返回：
        list: 包含各时段最短路径信息的列表，每个元素是一个字典，包含：
            - hour: 时段（0-23）
            - path: 最短路径的坐标点列表
            - travel_time: 最短通行时间（分钟）
            - sample_count: 该路径的样本数量
    """
    # 数据结构：{hour: {'path': [(lng,lat)], 'time': minutes, 'count': 数量}}
    hourly_stats = defaultdict(lambda: {
        'path': None,
        'time': float('inf'),
        'count': 0
    })

    for filename in os.listdir(folder_path):
        if not filename.endswith('.txt'):
            continue

        with open(os.path.join(folder_path, filename), 'r') as f:
            trajectories = defaultdict(list)
            
            # 读取并组织轨迹数据
            for line in f:
                parts = line.strip().split(',')
                if len(parts) < 4:
                    continue
                
                try:
                    taxi_id = parts[0]
                    time_str = parts[1]
                    lng = float(parts[2])
                    lat = float(parts[3])
                    timestamp = time_str  # 实际应用应转换为datetime
                    hour = int(time_str.split()[1].split(':')[0])
                    
                    trajectories[taxi_id].append((hour, lng, lat, timestamp))
                except (ValueError, IndexError):
                    continue

            # 分析每条轨迹
            for taxi_id, points in trajectories.items():
                in_area1 = False
                entry_time = None
                path_segment = []
                
                for i, (hour, lng, lat, timestamp) in enumerate(points):
                    # 检查是否进入区域A
                    if (not in_area1 and 
                        area1[0] <= lng <= area1[1] and 
                        area1[2] <= lat <= area1[3]):
                        in_area1 = True
                        entry_time = timestamp
                        path_segment = [(lng, lat)]
                        continue
                    
                    # 如果在区域A中，记录路径
                    if in_area1:
                        path_segment.append((lng, lat))
                        
                        # 检查是否到达区域B
                        if (area2[0] <= lng <= area2[1] and 
                            area2[2] <= lat <= area2[3]):
                            exit_time = timestamp
                            # 计算通行时间（简化：假设每分钟1个点）
                            travel_time = len(path_segment)  
                            
                            # 更新最短路径记录
                            if travel_time < hourly_stats[hour]['time']:
                                hourly_stats[hour] = {
                                    'path': path_segment,
                                    'time': travel_time,
                                    'count': 1
                                }
                            elif travel_time == hourly_stats[hour]['time']:
                                hourly_stats[hour]['count'] += 1
                            
                            break

    # 转换为前端需要的JSON格式
    result = []
    for hour in range(24):
        stats = hourly_stats[hour]
        if stats['path']:
            result.append({
                "hour": hour,
                "path": stats['path'],
                "travel_time": stats['time'],
                "sample_count": stats['count']
            })
        else:
            result.append({
                "hour": hour,
                "path": None,
                "travel_time": -1,
                "sample_count": 0
            })
    
    return result

# 示例使用
if __name__ == "__main__":
    """
    模块测试代码
    示例：分析天安门区域到北京西站区域的最短路径
    """
    # 定义两个区域（示例坐标）
    area1 = (116.30, 116.32, 39.90, 39.92)  # 天安门区域
    area2 = (116.35, 116.37, 39.88, 39.90)  # 北京西站区域
    
    # 分析数据
    analysis_result = analyze_shortest_path("GO", area1, area2)
    
    # 输出JSON结果
    print(json.dumps(analysis_result, indent=2))