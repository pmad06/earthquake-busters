#include <iostream>
#include <unordered_map>
#include <vector>

using namespace std;

class Trie {
    public:
        //constructor + destructor
        Trie();
        ~Trie();

        void insert(const string& word);
        bool search(const string& word) const;
        vector<string> autocomplete(const string& prefix, size_t limit = 0) const;
        void clear();

    private:
        struct TrieNode {
            unordered_map<char, TrieNode*> children;
            bool isEnd;

            TrieNode() : isEnd(false) {}
        };

        TrieNode* root;
        size_t wordCount;

        void dfsCollect(TrieNode* node, const string& prefix, vector<string>& out, size_t limit) const;
        TrieNode* findNode(const string& prefix) const;
        void freeNode(TrieNode* node);
        static string normalize(const string& str);

};