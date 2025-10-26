#include "splaytree.h"
#include <iostream>

using namespace std;

SplayTree :: SplayTree() : root(nullptr) {}

SplayTree :: ~SplayTree() {
    clear();
}

void SplayTree :: clear() {
    freeNode(root);
    root = nullptr;
}

void SplayTree :: freeNode(SplayNode* node) {
    if (node == nullptr) {
        return;
    }

    freeNode(node->left);
    freeNode(node->right);

    delete node;
}

SplayNode* SplayTree :: rightRotate(SplayNode* x) {
    SplayNode* y = x->left;
    x->left = y->right;
    y->right = x;
    return y;
}

SplayNode* SplayTree :: leftRotate(SplayNode* x) {
    SplayNode* y = x->right;
    x->right = y->left;
    y->left = x;
    return y;
}

SplayNode* SplayTree :: splay(SplayNode* root, int key) {
    if (root == nullptr || root->key == key) {
        return root;
    }

    if (key < root->key) {
        if (root->left == nullptr) {
            return root;
        }

        if (key < root->left->key) {
            root->left->left = splay(root->left->left, key);
            root = rightRotate(root);
        } else if (key > root->left->key) {
            root->left->right = splay(root->left->right, key);
            if (root->left->right != nullptr) {
                root->left = leftRotate(root->left);
            }
        }

        return (root->left == nullptr) ? root : rightRotate(root);
    } else {
        if (root->right == nullptr) {
            return root;
        }

        if (key > root->right->key) {
            root->right->right = splay(root->right->right, key);
            root = leftRotate(root);
        } else if (key < root->right->key) {
            root->right->left = splay(root->right->left, key);
            if (root->right->left != nullptr) {
                root->right = rightRotate(root->right);
            }
        }

        return (root->right == nullptr) ? root : leftRotate(root);
    }
}

void SplayTree :: insert(int key, const string& city) {
    if (root == nullptr) {
        root = new SplayNode(key, city);
        return;
    }

    root = splay(root, key);

    if (root->key == key) {
        return; // Key already exists
    }

    SplayNode* newNode = new SplayNode(key, city);

    if (key < root->key) {
        newNode->right = root;
        newNode->left = root->left;
        root->left = nullptr;
    } else {
        newNode->left = root;
        newNode->right = root->right;
        root->right = nullptr;
    }

    root = newNode;
}

bool SplayTree :: search(int key, string& outCity) {
    root = splay(root, key);

    if (root == nullptr || root->key != key) {
        return false; // Key not found
    }

    outCity = root->city;
    return true;
}

void SplayTree :: inorderHelper(SplayNode* node) const {
    if (node == nullptr) {
        return;
    }

    inorderHelper(node->left);
    cout << node->key << ": " << node->city << endl;
    inorderHelper(node->right);
    
}

void SplayTree :: inorder() const {
    inorderHelper(root);
}