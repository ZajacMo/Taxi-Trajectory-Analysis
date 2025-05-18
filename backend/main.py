from flask import Flask, request, jsonify
from F1 import get_trail_lists,get_trails_post
from F3 import query_region
from F4 import get_heatmap_data
from F56 import analyze_flow
from F7 import frequent_paths
from F8 import frequent_paths_ab
from F9 import analyze_shortest_path

app = Flask(__name__)

# F1
@app.route('/trailLists', methods=['GET'])
def new_get_trail_lists():
    return get_trail_lists()

@app.route('/trails/data', methods=['POST'])
def new_get_trails_post():
    return get_trails_post()

# F3
@app.route('/query_region', methods=['POST'])
def new_query_region():
    return query_region()


# F4
@app.route('/heatmap', methods=['GET'])
def new_get_heatmap_data():
    return get_heatmap_data()

# F56
@app.route('/flow_analysis', methods=['GET'])
def new_analyze_flow():
    return analyze_flow()

# F7
@app.route('/frequent_paths', methods=['POST'])
def new_frequent_paths():
    return frequent_paths()

# F8
@app.route('/frequent_paths_ab', methods=['POST'])
def new_frequent_paths_ab():
    return frequent_paths_ab()

# F9
@app.route('/optimized_path', methods=['GET'])
def new_analyze_shortest_path():
    return analyze_shortest_path()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)