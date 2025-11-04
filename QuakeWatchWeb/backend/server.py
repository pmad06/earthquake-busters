from flask import Flask, jsonify
from flask_cors import CORS
from bridges.bridges import *
from bridges.data_src_dependent import *
from splay import SplayTree  

app = Flask(__name__)
CORS(app)

splay_tree = SplayTree()
earthquake_data = []

def build_splay_tree():
    global splay_tree, earthquake_data
    try:
        bridges = Bridges(0, "pranathim", "1735501070239")
        data = get_earthquake_usgs_data(1000)
        earthquake_data = []  

        for quake in data:
            quake_info = {
                "title": quake.title,
                "magnitude": quake.magnitude,
                "location": quake.location,
                "lat": quake.latit,
                "long": quake.longit,
                "url": quake.url,
            }
            earthquake_data.append(quake_info)

            splay_tree.insert(quake.magnitude, quake_info)

        print(f"Built splay tree with {len(data)} earthquakes")
    except Exception as e:
        print("Error building splay tree:", e)

build_splay_tree()

@app.route("/earthquakes", methods=["GET"])
def get_earthquakes():
    """Return all earthquake data for map display."""
    return jsonify(earthquake_data)

@app.route("/earthquakes/search/<float:magnitude>", methods=["GET"])
def search_by_magnitude(magnitude: float):
    """Search splay tree for earthquakes with a given magnitude."""
    matches = splay_tree.search(magnitude) 
    if matches is None:
        matches = []
    return jsonify(matches)

if __name__ == "__main__":
    app.run(debug=True)
