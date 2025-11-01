from flask import Flask, jsonify
from bridges.bridges import Bridges
from bridges.data_src_dependent import get_earthquake_usgs_data

app = Flask(__name__)

@app.route("/earthquakes", methods=["GET"])
def get_earthquakes():
    try:
        bridges = Bridges(0, "pranathim", "1735501070239")
        data = get_earthquake_usgs_data(50)

        result = []
        for quake in data:
            result.append({
                "title": quake.title,
                "magnitude": quake.magnitude,
                "location": quake.location,
                "time": quake.time,
            })
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True)