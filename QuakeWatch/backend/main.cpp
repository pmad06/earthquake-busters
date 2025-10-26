#include "splaytree.h"
#include "trie.h"

using namespace std;

int main() {
    //trie
    Trie t;
    t.insert("Los Angeles");
    t.insert("Los Alamos");
    t.insert("San Francisco");
    t.insert("San Diego");

    std::cout << "Autocomplete for 'Lo':\n";
    auto results = t.autocomplete("Lo");
    for (auto& city : results) {
        std::cout << "  " << city << "\n";
    }

    //splay
    SplayTree st;
    st.insert(50, "Los Angeles");
    st.insert(30, "San Francisco");
    st.insert(70, "New York");
    st.insert(90, "Seattle");

    std::cout << "\nInorder traversal of Splay Tree:\n";
    st.inorder();

    std::string foundCity;
    if (st.search(70, foundCity)) {
        std::cout << "\nSearch for risk=70: Found " << foundCity << "\n";
    } else {
        std::cout << "\nSearch for risk=70: Not found\n";
    }

    return 0;
}
