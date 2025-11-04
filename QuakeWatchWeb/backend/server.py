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

def extract_city(location_str):
    if " of " in location_str:
        return location_str.split(" of ")[-1].strip()
    return location_str.strip()

def load_data_into_trees():

    global splay_tree
    global trie_tree
    splay_tree = SplayTree()
    trie_tree = Trie()

    bridges = Bridges(0, "pranathim", "1735501070239")
    data = get_earthquake_usgs_data(1000)

    for quake in data:

        city = extract_city(quake.location)
        quake_info = {
            "title": quake.title,
            "magnitude": quake.magnitude,
            "location": city,
            "lat": quake.latit,
            "long": quake.longit,
            "url": quake.url,
        }

        splay_tree.insert(quake.magnitude, quake_info)
        trie_tree.insert(city, quake_info)

load_data_into_trees()

@app.route("/earthquakes", methods=["GET"])
def get_earthquakes():
    try:
        #bridges = Bridges(0, "pranathim", "1735501070239")

        # global splay_tree
        # global trie_tree
        # splay_tree = SplayTree()
        # trie_tree = Trie()

        #data = get_earthquake_usgs_data(1000)


        # for quake in data:
        #     quake_info = {
        #         "title": quake.title,
        #         "magnitude": quake.magnitude,
        #         "location": quake.location,
        #         "lat": quake.latit,
        #         "long": quake.longit,
        #         "url": quake.url,
        #     }

        #     splay_tree.insert(quake.magnitude, quake_info)
        #     trie_tree.insert(quake.title, quake_info)

        result = splay_tree.inorder()    
        # result = {
        #     "splay_sorted": splay_tree.inorder(),
        #     "total_stored_in_trie": trie_tree.wordCtr
        # }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/search_trie/<prefix>", methods=["GET"])
def search_trie(prefix):
    try:
        #build trie once from global var
        #trie_tree = Trie()
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

#testing 