from flask import Flask, request, jsonify
import os
import math
from collections import defaultdict
from coordTransform_utils import wgs84_to_gcj02
from multiprocessing import Pool, cpu_count

app = Flask(__name__)

def process_file(params):
    """处理单个文件的核心函数（修正参数接收方式）"""
    filename, folder_path, r, target_hour = params  # 解包参数
    file_counts = defaultdict(int)
    
    with open(os.path.join(folder_path, filename), 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) < 4:
                continue
            
            try:
                _, time_str, lng_str, lat_str = parts[:4]
                hour = int(time_str.split(' ')[1].split(':')[0])
                
                # 时间过滤
                if target_hour is not None and hour != target_hour:
                    continue
                
                # 坐标转换和网格化
                lng, lat = wgs84_to_gcj02(float(lng_str), float(lat_str))
                grid_x, grid_y = math.floor(lng / r), math.floor(lat / r)
                center_lng, center_lat = (grid_x + 0.5) * r, (grid_y + 0.5) * r
                
                file_counts[(center_lng, center_lat)] += 1
            except (ValueError, IndexError):
                continue
                
    return file_counts

def process_taxi_data(folder_path, r, target_hour=None):
    """优化后的主处理函数"""
    files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    if not files:
        return []
    
    # 准备参数列表（每个元素是包含所有参数的元组）
    params_list = [(f, folder_path, r, target_hour) for f in files]
    
    # 并行处理（使用map而不是starmap）
    with Pool(processes=min(cpu_count(), 4)) as pool:  # 限制最大进程数
        results = pool.map(process_file, params_list)
    
    # 合并结果
    total_counts = defaultdict(int)
    for file_result in results:
        for point, count in file_result.items():
            total_counts[point] += count
    
    return [{
        "lng": lng,
        "lat": lat,
        "count": count
    } for (lng, lat), count in total_counts.items()]

@app.route('/api/heatmap', methods=['GET'])
def get_heatmap_data():
    # 参数获取
    folder_path = request.args.get('folder_path', 'taxi_log_2008_by_id')
    grid_width = float(request.args.get('grid_width', 0.01))
    
    # 时间参数（0~23的整数）
    hour_param = request.args.get('hour')
    target_hour = None
    if hour_param and hour_param.isdigit():
        hour = int(hour_param)
        if 0 <= hour <= 23:
            target_hour = hour
    
    try:
        result = process_taxi_data(folder_path, grid_width, target_hour)
        return jsonify({
            "status": "success",
            "data": result,
            "params": {
                "grid_width": grid_width,
                "hour": target_hour if target_hour is not None else "全部时段"
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
