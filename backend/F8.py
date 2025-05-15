"""
出租车轨迹分析模块

该模块提供基于Flask的Web服务，用于分析出租车在两个指定区域之间的频繁路径。
"""

from flask import Flask, request, jsonify
import sqlite3
import math
from collections import defaultdict, Counter
from coordTransform import wgs84_to_gcj02

# 初始化Flask应用
app = Flask(__name__)

# 数据库路径
DB_PATH = "trajectory.db"

def point_in_rect(lng, lat, lt, rb):
    """
    判断点是否在矩形区域内

    参数:
        lng (float): 经度
        lat (float): 纬度
        lt (list): 矩形左上角坐标 [经度, 纬度]
        rb (list): 矩形右下角坐标 [经度, 纬度]

    返回:
        bool: 如果点在矩形区域内返回True，否则返回False
    """
    return lt[0] <= lng <= rb[0] and rb[1] <= lat <= lt[1]

def encode_path(trail, grid_size=0.001):
    """
    对轨迹进行网格化编码

    参数:
        trail (list): 轨迹点列表，每个点包含lat和lng字段
        grid_size (float): 网格大小，默认0.001

    返回:
        tuple: 网格化编码后的轨迹
    """
    return tuple((round(p['lat']/grid_size), round(p['lng']/grid_size)) for p in trail)

@app.route('/frequent_paths_ab', methods=['POST'])
def frequent_paths_ab():
    """
    处理频繁路径查询请求

    请求参数（JSON）:
        {
            "areaA": {
                "ltPoint": [经度, 纬度],  # 区域A左上角
                "rbPoint": [经度, 纬度]   # 区域A右下角
            },
            "areaB": {
                "ltPoint": [经度, 纬度],  # 区域B左上角
                "rbPoint": [经度, 纬度]   # 区域B右下角
            },
            "k": 返回的Top-K路径数量（默认5）
        }

    返回:
        JSON响应：包含最频繁路径的JSON对象
    """
    req = request.get_json()
    areaA = req.get("areaA")
    areaB = req.get("areaB")
    top_k = req.get("k", 5)

    # 验证输入参数
    if not areaA or not areaB:
        return jsonify({"error": "Missing areaA or areaB"}), 400

    # 获取区域A和B的边界坐标
    ltA, rbA = areaA["ltPoint"], areaA["rbPoint"]
    ltB, rbB = areaB["ltPoint"], areaB["rbPoint"]

    # 连接数据库并查询所有轨迹数据
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT taxi_id, time, lng, lat FROM traj_data ORDER BY taxi_id, time")
    rows = cursor.fetchall()
    conn.close()

    # 初始化统计变量
    result_counter = Counter()  # 用于统计路径出现次数
    path_samples = {}  # 用于存储路径样本

    # 初始化轨迹处理变量
    current_id = None  # 当前处理的出租车ID
    insideA = False  # 标记是否进入区域A
    segment = []  # 当前处理的路径段

    # 遍历所有轨迹点
    for taxi_id, time, lng, lat in rows:

        # 如果切换到新的出租车，重置相关变量
        if taxi_id != current_id:
            current_id = taxi_id
            insideA = False
            segment = []

        # 路径段处理逻辑
        if not insideA and point_in_rect(lng, lat, ltA, rbA):
            # 如果进入区域A，开始记录路径段
            insideA = True
            segment = []
        if insideA:
            # 加入轨迹点（GCJ-02 转换后）
            lng_gcj, lat_gcj = wgs84_to_gcj02(lat, lng)
            segment.append({
                "lat": lat_gcj,
                "lng": lng_gcj,
                "time": time
            })
            if point_in_rect(lng, lat, ltB, rbB):
                path_key = encode_path(segment)
                result_counter[path_key] += 1
                if path_key not in path_samples:
                    path_samples[path_key] = segment[:]
                insideA = False  # 结束当前路径
                segment = []

    # 获取出现次数最多的前K条路径
    top_paths = result_counter.most_common(top_k)

    # 构建响应数据
    response = []
    for path_key, count in top_paths:
        response.append({
            "count": count,
            "trail": path_samples[path_key]
        })

    # 返回JSON响应
    return jsonify({
        "total": len(result_counter),  # 总路径数
        "topK": top_k,  # 请求的Top-K值
        "result": response  # 最频繁路径列表
    })
if __name__ == '__main__':
    app.run(debug=True)
