#include <string>

using namespace std;

struct SplayNode {
    int key;
    string city;
    SplayNode* left;
    SplayNode* right;

    SplayNode(int k, const string& c) : key(k), city(c), left(nullptr), right(nullptr) {}
};

class SplayTree {
    public:
        SplayTree();
        ~SplayTree();

        void insert(int key, const string& city);
        bool search(int key, string& outCity);
        void clear();

        void inorder() const;

    private:
        SplayNode* root;

        SplayNode* splay(SplayNode* root, int key);

        //rotations
        SplayNode* rightRotate(SplayNode* x);
        SplayNode* leftRotate(SplayNode* x);

        //helpers
        void freeNode(SplayNode* node);
        void inorderHelper(SplayNode* node) const;
};