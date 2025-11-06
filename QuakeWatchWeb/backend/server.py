from flask import Flask, jsonify
from flask_cors import CORS
from bridges.bridges import *
from bridges.data_src_dependent import *
from splay import SplayTree
from trie import Trie

app = Flask(__name__)
CORS(app)

#make sure trees r global
splay_tree = SplayTree()
trie_tree = Trie()
earthquake_data = []

def risk_factor(magnitude: float) -> str:
    if magnitude < 4:
        return "Low Risk Earthquake"
    elif 4 <= magnitude <= 6.9:
        return "Moderate Risk Earthquake"
    elif 7 <= magnitude <= 7.9:
        return "High Risk Earthquake"
    else:
        return "Severe Risk Earthquake"


def extract_city(location_str):
    if " of " in location_str:
        return location_str.split(" of ")[-1].strip()
    return location_str.strip()


def build_tree():
   global splay_tree, earthquake_data, trie_tree
   try:
       bridges = Bridges(0, "pranathim", "1735501070239")
       data = get_earthquake_usgs_data(1000)
       earthquake_data = []


       for quake in data:
            city = extract_city(quake.location)
            quake_info = {
                "title": quake.title,
                "magnitude": quake.magnitude,
                "location": city,
                "lat": quake.latit,
                "long": quake.longit,
                "url": quake.url,
                "risk_factor": risk_factor(quake.magnitude),
            }

            earthquake_data.append(quake_info)
           
            trie_tree.insert(city, quake_info)

            splay_tree.insert(quake.magnitude, quake_info)

       print(f"Built splay tree with {len(data)} earthquakes")
   except Exception as e:
       print("Error building splay tree:", e)

build_tree()

@app.route("/earthquakes", methods=["GET"])
def get_earthquakes():
    return jsonify(earthquake_data)

@app.route("/earthquakes/search/<float:magnitude>", methods=["GET"])
def search_by_magnitude(magnitude: float):
   """Search splay tree for earthquakes with a given magnitude."""
   matches = splay_tree.search(magnitude)
   if matches is None:
       matches = []
   
   results = []
   for quake in matches: 
       quakeWithRisk = quake.copy()
       quakeWithRisk["risk_factor"] = risk_factor(quake["magnitude"])
       results.append(quakeWithRisk)
   return jsonify(matches)

@app.route("/search_trie/<prefix>", methods=["GET"])
def search_trie(prefix):
    try:
        results = trie_tree.autocomplete(prefix, limit=10)
        shaped = [
            {
                "location": quake_obj["location"],
                "lat": quake_obj["lat"],
                "long": quake_obj["long"],
                "magnitude": quake_obj["magnitude"],
                "url": quake_obj["url"]
            }
            for quake_obj in results
        ]

        print("Autocomplete results for", prefix, ":", shaped[:3]) #debug
        #return jsonify(results)
        return jsonify(shaped)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)


