import random
import os
from flask import Flask, request, jsonify
from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime
from flask_cors import CORS  # 引入flask-cors
from flask_socketio import SocketIO, emit
from concurrent.futures import ThreadPoolExecutor
from coordTransform import wgs84_to_gcj02

app = Flask(__name__)
# DATA_DIR = ".\\src\\utils\\taxi_log_2008_by_id"
DATA_DIR = "taxi_log_2008_by_id"
socketio = SocketIO(app, cors_allowed_origins='*')
CORS(app)  # 启用CORS支持
# F1
@dataclass
class TrailPoint:
    """
    表示轨迹中的一个点
    Attributes:
        latitude: 纬度
        longitude: 经度
        timestamp: 时间戳
    """
    latitude: float
    longitude: float
    timestamp: str

@dataclass
class TrailLine:
    """
    表示一辆出租车的轨迹线
    Attributes:
        taxi_id: 出租车ID
        points: 轨迹点列表
    """
    taxi_id: str
    points: List[TrailPoint]

def is_valid_point(lat: float, lng: float, timestamp: str) -> bool:
    """
    验证点是否有效
    Args:
        lat: 纬度
        lng: 经度
        timestamp: 时间戳
    Returns:
        bool: 如果点在有效范围内且时间格式正确返回True，否则返回False
    """
    try:
        if not (39.4 <= lat <= 41.0 and 115.7 <= lng <= 117.4):
            return False
        datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        return True
    except:
        return False

def load_taxi_data(taxi_id: str) -> Optional[TrailLine]:
    """
    加载指定出租车ID的轨迹数据
    Args:
        taxi_id: 出租车ID
    Returns:
        Optional[TrailLine]: 如果文件存在且包含有效数据返回TrailLine对象，否则返回None
    """
    filepath = os.path.join(DATA_DIR, f"{taxi_id}.txt")
    if not os.path.exists(filepath):
        return None

    points = []
    with open(filepath, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 4:
                _, timestamp, lng, lat = parts
                try:
                    lat_f = float(lat)
                    lng_f = float(lng)
                    if is_valid_point(lat_f, lng_f, timestamp):
                        points.append(TrailPoint(lat_f, lng_f, timestamp))
                except:
                    continue
    return TrailLine(taxi_id=taxi_id, points=points) if points else None

def remove_duplicate_points(trail: TrailLine) -> List[TrailPoint]:
    """
    移除轨迹中的重复点
    Args:
        trail: 原始轨迹线
    Returns:
        List[TrailPoint]: 去重后的轨迹点列表
    """
    if not trail.points:
        return []
    unique = [trail.points[0]]
    for pt in trail.points[1:]:
        if pt.latitude != unique[-1].latitude or pt.longitude != unique[-1].longitude:
            unique.append(pt)
    return unique

def perpendicular_distance(p: TrailPoint, start: TrailPoint, end: TrailPoint) -> float:
    """
    计算点到线段的垂直距离
    Args:
        p: 目标点
        start: 线段起点
        end: 线段终点
    Returns:
        float: 点到线段的垂直距离
    """
    if start.latitude == end.latitude and start.longitude == end.longitude:
        return ((p.latitude - start.latitude) ** 2 + (p.longitude - start.longitude) ** 2) ** 0.5
    area = abs((end.longitude - start.longitude) * (start.latitude - p.latitude) -
               (start.longitude - p.longitude) * (end.latitude - start.latitude))
    base = ((end.latitude - start.latitude) ** 2 + (end.longitude - start.longitude) ** 2) ** 0.5
    return area / base

def douglas_peucker(points: List[TrailPoint], tolerance: float) -> List[TrailPoint]:
    """
    使用Douglas-Peucker算法简化轨迹
    Args:
        points: 原始轨迹点列表
        tolerance: 简化容忍度
    Returns:
        List[TrailPoint]: 简化后的轨迹点列表
    """
    if len(points) <= 2:
        return points.copy()
    max_dist = 0.0
    index = 0
    end = len(points) - 1
    for i in range(1, end):
        dist = perpendicular_distance(points[i], points[0], points[end])
        if dist > max_dist:
            index = i
            max_dist = dist
    if max_dist > tolerance:
        left = douglas_peucker(points[:index+1], tolerance)
        right = douglas_peucker(points[index:], tolerance)
        return left[:-1] + right
    else:
        return [points[0], points[-1]]

def clean_trail(trail: TrailLine, simplify: bool = False, tolerance: float = 0.0001) -> TrailLine:
    """
    清理轨迹数据
    Args:
        trail: 原始轨迹线
        simplify: 是否进行轨迹简化
        tolerance: 简化容忍度
    Returns:
        TrailLine: 清理后的轨迹线
    """
    points = remove_duplicate_points(trail)
    if simplify:
        points = douglas_peucker(points, tolerance)
    return TrailLine(taxi_id=trail.taxi_id, points=points)

# F1
@app.route('/trailLists', methods=['GET'])
def get_trail_lists():
    """
    处理GET请求，根据传入的关键字返回带有该关键字的前50条出租车轨迹ID列表
    Returns:
        JSON响应：包含符合条件的出租车轨迹ID列表
    """
    keyword = request.args.get('keyword', '')
    try:
        all_taxi_ids = [f.split('.')[0] for f in os.listdir(DATA_DIR) if f.endswith('.txt')]
        matching_ids = []
        for taxi_id in all_taxi_ids:
            if keyword in taxi_id:
                matching_ids.append(taxi_id)
                if len(matching_ids) >= 50:
                    break
    except FileNotFoundError:
        return jsonify({"error": "Data directory not found"}), 500

    return jsonify(matching_ids)

@app.route('/trails/data', methods=['POST'])
def get_trails_post():
    """
    处理POST请求，获取轨迹数据
    Returns:
        JSON响应：包含请求的轨迹数据或错误信息
    """
    """
    POST /trails
    Body 参数（JSON）:
    {
        "taxi_ids": ["1", "2"],         # 可选，若不传则查询所有
        "simplify": true,               # 可选，默认 false
        "tolerance": 0.0001             # 可选，轨迹简化容忍度
        "sample_count": 10               # 可选，随机抽样数量
    }
    """
    try:
        req = request.get_json(force=True)
        print(req)
    except Exception:
        return jsonify({"error": "Invalid JSON body"}), 400

    taxi_ids = req.get("taxi_ids", "all")
    sample_count = req.get("sampleCount", None)
    simplify = req.get("simplify", False)
    tolerance = float(req.get("tolerance", 0.0001))
                      
    if taxi_ids == "all":
        try:
            all_ids = [f.split('.')[0] for f in os.listdir(DATA_DIR) if f.endswith('.txt')]
            if sample_count:
                sample_count = int(sample_count)
                random.shuffle(all_ids)
                taxi_ids = all_ids[:sample_count]
            else:
                taxi_ids = all_ids
        except FileNotFoundError:
            return jsonify({"error": "Data directory not found"}), 500

    result = []
    def process_taxi_id(taxi_id):
        trail = load_taxi_data(taxi_id)
        if trail:
            trail = clean_trail(trail, simplify, tolerance)
            transformed_points = []
            for pt in trail.points:
                lng_gcj, lat_gcj = wgs84_to_gcj02(pt.longitude, pt.latitude)
                transformed_points.append([lat_gcj, lng_gcj, datetime.strptime(pt.timestamp, "%Y-%m-%d %H:%M:%S").timestamp()])
            return {
                "vendor": int(trail.taxi_id),
                "path": transformed_points
            }
        return None

    with ThreadPoolExecutor(max_workers=16) as executor:
        results = list(executor.map(process_taxi_id, taxi_ids))

    result = [r for r in results if r]
    return jsonify(result)


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True, port=5000)
