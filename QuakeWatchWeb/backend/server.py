from flask import Flask, jsonify
from flask_cors import CORS
from bridges.bridges import *
from bridges.data_src_dependent import *
from splay import SplayTree
from trie import Trie

app = Flask(__name__)
CORS(app)

@app.route("/earthquakes", methods=["GET"])
def get_earthquakes():
    try:
        bridges = Bridges(0, "pranathim", "1735501070239")
        data = get_earthquake_usgs_data(1000)

        splay_tree = SplayTree()
        trie_tree = Trie()

        for quake in data:
            quake_info = {
                "title": quake.title,
                "magnitude": quake.magnitude,
                "location": quake.location,
                "lat": quake.latit,
                "long": quake.longit,
                "url": quake.url,
            }

            splay_tree.insert(quake.magnitude, quake_info)
            trie_tree.insert(quake.title, quake_info)

        #result = tree.inorder()    
        result = {
            "splay_sorted": splay_tree.inorder(),
            "total_stored_in_trie": trie_tree.wordCtr
        }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


if __name__ == "__main__":
    app.run(debug=True)

#testing 