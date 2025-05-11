import json
import os
from collections import defaultdict
import math

def process_taxi_data(folder_path, r):
    """
    处理出租车轨迹数据，生成热力图所需的数据格式

    参数:
        folder_path (str): 包含出租车轨迹数据的文件夹路径
        r (float): 网格宽度参数，用于划分地理网格

    返回:
        list: 包含热力图点数据的列表，每个元素是一个字典，包含经纬度、时间和计数
    """
    # 使用defaultdict统计每个(经度, 纬度, 小时)三元组的出现次数
    # 键格式: (center_lng, center_lat, hour)
    # 值: 该位置在该小时内的车流量
    grid_data = defaultdict(int)
    
    # 遍历指定文件夹中的所有txt文件，处理每个文件中的轨迹数据
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            with open(os.path.join(folder_path, filename), 'r') as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) < 4:
                        continue
                    
                    # 解析每行数据，提取时间、经度和纬度信息
                    _, time_str, lng_str, lat_str = parts[:4]
                    try:
                        lng = float(lng_str)
                        lat = float(lat_str)
                        
                        # 从时间字符串中提取小时信息，用于时间维度统计
                        time_parts = time_str.split(' ')
                        if len(time_parts) < 2:
                            continue
                        date_part, time_part = time_parts
                        hour = int(time_part.split(':')[0])
                        
                        # 根据网格宽度r，计算当前坐标所在的网格编号
                        grid_x = math.floor(lng / r)
                        grid_y = math.floor(lat / r)
                        
                        # 计算网格中心点坐标，作为该网格的代表位置
                        center_lng = (grid_x + 0.5) * r
                        center_lat = (grid_y + 0.5) * r
                        
                        # 以(网格中心经度, 网格中心纬度, 小时)为键，统计车流量
                        grid_data[(center_lng, center_lat, hour)] += 1
                    except ValueError:
                        continue
    
    # 将统计结果转换为热力图点数据格式，每个点包含位置、时间和车流量
    heat_points = []
    for (lng, lat, time), count in grid_data.items():
        heat_points.append({
            "lat": lat,
            "lng": lng,
            "count": count,
            "time": time
        })
    
    return heat_points

# 示例使用
if __name__ == "__main__":
    # 参数设置
    folder_path = "GO"  # 替换为实际的文件夹路径
    grid_width = 0.01   # 网格宽度参数r
    
    # 处理数据
    result = process_taxi_data(folder_path, grid_width)
    
    # 输出JSON格式结果
    print(json.dumps(result, indent=2))