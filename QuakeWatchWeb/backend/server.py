from flask import Flask, jsonify
from flask_cors import CORS
from bridges.bridges import *
from bridges.data_src_dependent import *
from splay import SplayTree

app = Flask(__name__)
CORS(app)

@app.route("/earthquakes", methods=["GET"])
def get_earthquakes():
    try:
        bridges = Bridges(0, "pranathim", "1735501070239")
        data = get_earthquake_usgs_data(1000)

        tree = SplayTree()

        for quake in data:
            key = quake.magnitude
            value = {
                "title": quake.title,
                "magnitude": quake.magnitude,
                "location": quake.location,
                "lat": quake.latit,
                "long": quake.longit,
                "url": quake.url,
            }
            tree.insert(key, value)

        result = tree.inorder()    
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True)

#testing 