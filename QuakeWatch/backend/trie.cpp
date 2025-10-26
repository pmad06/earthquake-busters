#include <iostream>
#include <unordered_map>
#include <vector>
#include <algorithm>
#include <cctype>

#include "trie.h"

using namespace std;

//constructor
Trie :: Trie() {
    root = new TrieNode();
    wordCount = 0;
}

//destructor
Trie :: ~Trie() {
    clear();
    delete root;
}

void Trie :: insert(const string& word) {
    string wordNorm = normalize(word);
    if (wordNorm.empty()) {
        return;
    }

    TrieNode* node = root;
    for (char c : wordNorm) {
        if (node->children.find(c) == node->children.end()) {
            node->children[c] = new TrieNode();
        }
        node = node->children[c];
    }

    if (!node->isEnd) {
        node->isEnd = true;
        wordCount++;
    }
}

bool Trie :: search(const string& word) const {
    string wordNorm = normalize(word);
    if (wordNorm.empty()) {
        return false;
    }

    TrieNode* node = root;
    for (char c : wordNorm) {
        if (node->children.find(c) == node->children.end()) {
            return false;
        }
        node = node->children[c];
    }

    return node->isEnd;
}

vector<string> Trie :: autocomplete(const string& prefix, size_t limit) const {
    vector<string> results;
    string prefixNorm = normalize(prefix);

    if (prefixNorm.empty()) {
        return results;
    }

    TrieNode* node = findNode(prefixNorm);
    if (node == nullptr) {
        return results;
    }

    if (node) {
        dfsCollect(node, prefixNorm, results, limit);
    }

    return results;
}

void Trie :: dfsCollect(TrieNode* node, const string& prefix, vector<string>& out, size_t limit) const {
    if (node == nullptr) {
        return;
    }

    if (limit > 0 && out.size() >= limit) {
        return;
    }

    if (node->isEnd) {
        out.push_back(prefix);
    }

    vector<char> keys;
    for (auto& k : node->children) {
        keys.push_back(k.first);
    }

    sort(keys.begin(), keys.end());

    for (char c : keys) {
        if (limit > 0 && out.size() >= limit) {
            break;
        }
        dfsCollect(node->children.at(c), prefix + c, out, limit);
    }
}

Trie :: TrieNode* Trie :: findNode(const string& prefix) const {
    TrieNode* node = root;
    for (char c : prefix) {
        if (node->children.find(c) == node->children.end()) {
            return nullptr;
        }
        node = node->children[c];
    }
    return node;
}

void Trie :: clear() {
    for (auto& child : root->children) {
        freeNode(child.second);
    }

    root->children.clear();
    wordCount = 0;
}

void Trie :: freeNode(TrieNode* node) {
    for (auto& child : node->children) {
        freeNode(child.second);
    }

    delete node;
}

string Trie :: normalize(const string& str) {
    string out;
    out.reserve(str.size());

    for (unsigned char c : str) {
        if (isalnum(c)) {
            out.push_back(tolower(c));
        } else if (isspace(c)) {
            if (out.empty() || out.back() != ' ') {
                out.push_back(' ');
            }
        }
    } 

    if (out.empty() == false && out.front() == ' ') {
        out.erase(out.begin());
    }

    if (out.empty() == false && out.back() == ' ') {
        out.pop_back();
    }

    return out;
}