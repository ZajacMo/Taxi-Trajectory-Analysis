"""
出租车轨迹分析工具模块

本模块提供对出租车轨迹数据的分析功能，主要包括：
1. 区域流量统计：统计指定区域在不同时段的车辆流入流出情况
2. 空间索引：通过网格划分加速地理位置的区域判断
3. 并行处理：利用多进程加速大规模数据处理

主要功能：
- create_spatial_index: 创建空间索引网格
- point_in_area: 判断点是否在指定区域内
- process_file: 处理单个轨迹文件
- analyze_flow: 主分析函数，统计区域流量

依赖库：
- json: 数据处理和输出
- os: 文件系统操作
- math: 数学计算
- collections.defaultdict: 数据统计
- multiprocessing: 并行处理
"""

import json
import os
import math
from collections import defaultdict
from multiprocessing import Pool, Manager

def create_spatial_index(area, grid_size=0.01):
    """
    创建空间索引网格

    参数:
        area (tuple): 区域边界坐标，格式为(min_lng, max_lng, min_lat, max_lat)
        grid_size (float): 网格大小，默认0.01度

    返回:
        dict: 包含空间索引信息的字典，包括:
            - min_lng: 最小经度
            - min_lat: 最小纬度
            - grid_size: 网格大小
            - cols: 列数
            - rows: 行数
    """
    min_lng, max_lng, min_lat, max_lat = area
    grid_cols = math.ceil((max_lng - min_lng) / grid_size)
    grid_rows = math.ceil((max_lat - min_lat) / grid_size)
    return {
        'min_lng': min_lng,
        'min_lat': min_lat,
        'grid_size': grid_size,
        'cols': grid_cols,
        'rows': grid_rows
    }

def point_in_area(lng, lat, area, spatial_index=None):
    """
    判断点是否在指定区域内

    参数:
        lng (float): 点的经度
        lat (float): 点的纬度
        area (tuple): 区域边界坐标
        spatial_index (dict, optional): 空间索引信息

    返回:
        bool: 如果点在区域内返回True，否则返回False
    """
    if spatial_index:
        col = math.floor((lng - spatial_index['min_lng']) / spatial_index['grid_size'])
        row = math.floor((lat - spatial_index['min_lat']) / spatial_index['grid_size'])
        if 0 <= col < spatial_index['cols'] and 0 <= row < spatial_index['rows']:
            return True
    return (area[0] <= lng <= area[1]) and (area[2] <= lat <= area[3])

def process_file(args):
    """
    处理单个轨迹文件，统计区域流量

    参数:
        args (tuple): 包含以下元素的元组:
            - filename: 文件名
            - area1: 主区域坐标
            - area2: 次区域坐标（可选）
            - area1_index: 主区域空间索引
            - area2_index: 次区域空间索引（可选）

    返回:
        dict: 按小时统计的流量数据，格式为:
            {hour: {"flowIn": 流入量, "flowOut": 流出量}}
    """
    filename, area1, area2, area1_index, area2_index = args
    flow_stats = defaultdict(lambda: {"flowIn": 0, "flowOut": 0})
    
    with open(filename, 'r') as file:
        current_taxi = None
        prev_state = None
        prev_hour = None
        
        for line in file:
            parts = line.strip().split(',')
            if len(parts) < 4:
                continue
            
            try:
                taxi_id = parts[0]
                time_str = parts[1]
                lng = float(parts[2])
                lat = float(parts[3])
                hour = int(time_str.split(' ')[1].split(':')[0])
                
                # 状态机核心逻辑
                if taxi_id != current_taxi:
                    # 新车辆，重置状态
                    current_taxi = taxi_id
                    prev_state = None
                    prev_hour = None
                
                # 计算当前区域状态
                in_area1 = point_in_area(lng, lat, area1, area1_index)
                in_area2 = point_in_area(lng, lat, area2, area2_index) if area2 else False
                
                # 状态转移检测
                if prev_state is not None and prev_hour == hour:
                    # 区域间转移检测
                    if area2:
                        # A→B转移 (流出)
                        if prev_state['in_area1'] and in_area2:
                            flow_stats[hour]["flowOut"] += 1
                        # B→A转移 (流入)
                        elif prev_state['in_area2'] and in_area1:
                            flow_stats[hour]["flowIn"] += 1
                    else:
                        # 外部→A (流入)
                        if not prev_state['in_area1'] and in_area1:
                            flow_stats[hour]["flowIn"] += 1
                        # A→外部 (流出)
                        elif prev_state['in_area1'] and not in_area1:
                            flow_stats[hour]["flowOut"] += 1
                
                # 更新前状态
                prev_state = {'in_area1': in_area1, 'in_area2': in_area2}
                prev_hour = hour
                
            except (ValueError, IndexError):
                continue
    
    return dict(flow_stats)

def analyze_flow(folder_path, area1, area2=None, workers=4):
    """
    主分析函数，统计指定文件夹中所有轨迹文件的区域流量

    参数:
        folder_path (str): 包含轨迹文件的文件夹路径
        area1 (tuple): 主区域坐标
        area2 (tuple, optional): 次区域坐标
        workers (int): 并行处理进程数，默认4

    返回:
        list: 按小时统计的流量数据列表，每个元素包含:
            - timeStamp: 小时
            - flowIn: 流入量
            - flowOut: 流出量
    """
    # 创建空间索引
    area1_index = create_spatial_index(area1)
    area2_index = create_spatial_index(area2) if area2 else None
    
    # 准备多进程任务
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) 
             if f.endswith('.txt')]
    args = [(f, area1, area2, area1_index, area2_index) for f in files]
    
    # 并行处理
    with Pool(workers) as pool:
        results = pool.map(process_file, args)
    
    # 合并结果
    final_stats = defaultdict(lambda: {"flowIn": 0, "flowOut": 0})
    for result in results:
        for hour, counts in result.items():
            final_stats[hour]["flowIn"] += counts["flowIn"]
            final_stats[hour]["flowOut"] += counts["flowOut"]
    
    # 生成输出格式
    output = []
    for hour in range(24):
        output.append({
            "timeStamp": hour,
            "flowIn": final_stats[hour]["flowIn"],
            "flowOut": final_stats[hour]["flowOut"]
        })
    
    return output

# 示例使用
if __name__ == "__main__":
    # 区域定义（示例坐标）
    area1 = (116.35, 116.45, 39.85, 39.95)  # 天安门区域
    area2 = (116.30, 116.40, 39.90, 40.00)  # 北京西站区域
    
    result = analyze_flow("GO", area1, area2)
    print(json.dumps(result, indent=2))