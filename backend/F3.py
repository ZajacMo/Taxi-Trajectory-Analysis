"""
出租车轨迹查询模块

该模块提供了一个Flask API接口，用于查询指定时间段和地理区域内的出租车轨迹数据。
主要功能包括：
1. 根据时间范围和地理区域查询出租车轨迹
2. 将查询结果以JSON格式返回

依赖：
- Flask: Web框架
- sqlite3: 数据库连接
- datetime: 时间处理
"""

from flask import Flask, request, jsonify
import sqlite3
import datetime

# 初始化Flask应用
app = Flask(__name__)

# 数据库路径
DB_PATH = "trajectory.db"

def query_trajectory(start_time, end_time, lt_point, rb_point):
    """
    查询指定时间和区域内的出租车轨迹

    参数：
        start_time (datetime): 查询开始时间
        end_time (datetime): 查询结束时间
        lt_point (list): 区域左上角坐标 [经度, 纬度]
        rb_point (list): 区域右下角坐标 [经度, 纬度]

    返回：
        dict: 包含出租车ID及其轨迹的字典，格式为：
            {
                taxi_id: [
                    {
                        "time": 时间,
                        "lng": 经度,
                        "lat": 纬度
                    }
                ]
            }
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    start_str = start_time.strftime("%Y-%m-%d %H:%M:%S")
    end_str = end_time.strftime("%Y-%m-%d %H:%M:%S")

    min_lng, max_lng = lt_point[0], rb_point[0]
    min_lat, max_lat = rb_point[1], lt_point[1]

    cursor.execute(f"""
        SELECT d.taxi_id, d.time, d.lng, d.lat
        FROM traj_index AS i
        JOIN traj_data AS d ON d.point_id = i.point_id
        WHERE
            i.min_lng >= ? AND i.max_lng <= ?
            AND i.min_lat >= ? AND i.max_lat <= ?
            AND d.time BETWEEN ? AND ?
        """, (min_lng, max_lng, min_lat, max_lat, start_str, end_str))

    result = {}
    for taxi_id, time, lng, lat in cursor.fetchall():
        if taxi_id not in result:
            result[taxi_id] = []
        result[taxi_id].append({
            "time": time,
            "lng": lng,
            "lat": lat
        })

    conn.close()
    return result

@app.route('/query_region', methods=['POST'])
def query_region():
    """
    处理区域查询请求

    请求参数（JSON）：
        {
            "startTime": "YYYY-MM-DD HH:MM:SS",  # 开始时间
            "endTime": "YYYY-MM-DD HH:MM:SS",    # 结束时间
            "ltPoint": [经度, 纬度],              # 区域左上角坐标
            "rbPoint": [经度, 纬度]               # 区域右下角坐标
        }

    返回：
        JSON响应：包含查询结果的JSON对象，格式为：
            {
                "total": 轨迹数量,
                "path": [
                    {
                        "id": 出租车ID,
                        "trail": [轨迹点]
                    }
                ]
            }
    """
    req = request.get_json()
    try:
        start_time = datetime.datetime.strptime(req.get('startTime'), "%Y-%m-%d %H:%M:%S")
        end_time = datetime.datetime.strptime(req.get('endTime'), "%Y-%m-%d %H:%M:%S")
        lt_point = req.get('ltPoint', [116.0, 40.0])
        rb_point = req.get('rbPoint', [117.0, 39.0])
    except Exception as e:
        return jsonify({"error": "Invalid input format", "details": str(e)}), 400

    result = query_trajectory(start_time, end_time, lt_point, rb_point)

    # 组装返回
    response = {
        "total": len(result),
        "path": [{"id": taxi_id, "trail": trail} for taxi_id, trail in result.items()]
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True, port=5000)
