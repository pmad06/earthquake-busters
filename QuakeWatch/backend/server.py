from flask import Flask, jsonify
from flask_cors import CORS
from bridges.bridges import *
from bridges.data_src_dependent import *
from trie import Trie
from splay import SplayTree

import math

#explore nearby locations
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))
    return R * c

app = Flask(__name__)
CORS(app)

#initialize trie with all data - autocomplete
quake_trie = Trie()
quake_data = []

#initialize splay tree - repeated lookups
quake_splay = SplayTree()

@app.before_first_request
def initialize_trie():
    global quake_data
    quake_data = []
    data = get_earthquake_usgs_data(1000)
    for quake in data:
        quake_obj = {
            "title": quake.title,
            "magnitude": quake.magnitude,
            "location": quake.location,
            "lat": quake.latit,
            "long": quake.longit,
            "url": quake.url,
        }
        quake_data.append(quake_obj)

        #choose which we want autocomplete to work with
        #location name
        quake_trie.insert(quake.location, quake_obj)
        #loocation coordinates
        quake_trie.insert(f"{quake.latit}, {quake.longit}", quake_obj)

        #splay
        quake_splay.insert(quake.location, quake_obj)

#search 2.0 with haversine
@app.route("/search", methods=["GET"])
def search_quakes():
    prefix = request.args.get("prefix", "")
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)
    radius = request.args.get("radius", type=float)

    # If lat/lon/radius provided do nearby search
    if lat is not None and lon is not None and radius is not None:
        results = []
        for quake in quake_data:
            d = haversine(lat, lon, quake["lat"], quake["long"])
            if d <= radius:
                quake_copy = quake.copy()
                quake_copy["distance_km"] = round(d, 2)
                results.append(quake_copy)
        results.sort(key=lambda q: q["distance_km"])
        return jsonify(results)

    # Otherwise fall back to Trie autocomplete
    if prefix:
        return jsonify(quake_trie.autocomplete(prefix, limit=20))

    return jsonify({"error": "Provide either prefix or lat/lon/radius"}), 400

#splay find using title
@app.route("/quake", methods=["GET"]) 
def get_quake():
    title = request.args.get("title", "")
    result = quake_splay.search(title)
    if result:
        return jsonify(result)
    return jsonify({"error": "Earthquake not found"}), 404

#search functionality for coordinates- calling funciton
# @app.route("/search", methods=["GET"])
# def search_quakes():
#     prefix = request.args.get("prefix", "")
#     results = quake_trie.autocomplete(prefix, limit=20)
#     #returns all matching strings (coordinates)
#     return jsonify(results)

# @app.route("/earthquakes", methods=["GET"])
# def get_earthquakes():
#     try:
#         bridges = Bridges(0, "pranathim", "1735501070239")
#         data = get_earthquake_usgs_data(1000)

#         result = []
#         for quake in data:
#             result.append({
#                 "title": quake.title,
#                 "magnitude": quake.magnitude,
#                 "location": quake.location,
#                 "lat": quake.latit,
#                 "long": quake.longit,
#                 "url": quake.url,
#             })
        
#         return jsonify(result)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
    

if __name__ == "__main__":
    app.run(debug=True)

#testing 