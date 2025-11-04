from typing import Optional, List

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

class SplayTree:
    def __init__(self):
        self.root = None

    def _right_rotate(self, x):
        y = x.left
        x.left = y.right
        y.right = x
        return y

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def _splay(self, root, key):
        if root is None or root.key == key:
            return root

        # Key lies in left subtree
        if key < root.key:
            if root.left is None:
                return root
            # Zig-Zig (Left Left)
            if key < root.left.key:
                root.left.left = self._splay(root.left.left, key)
                root = self._right_rotate(root)
            # Zig-Zag (Left Right)
            elif key > root.left.key:
                root.left.right = self._splay(root.left.right, key)
                if root.left.right:
                    root.left = self._left_rotate(root.left)
            return root if root.left is None else self._right_rotate(root)
        else:
            if root.right is None:
                return root
            # Zag-Zig (Right Left)
            if key < root.right.key:
                root.right.left = self._splay(root.right.left, key)
                if root.right.left:
                    root.right = self._right_rotate(root.right)
            # Zag-Zag (Right Right)
            elif key > root.right.key:
                root.right.right = self._splay(root.right.right, key)
                root = self._left_rotate(root)
            return root if root.right is None else self._left_rotate(root)

    def insert(self, key, value):
        if self.root is None:
            self.root = Node(key, value)
            return
        self.root = self._splay(self.root, key)
        if self.root.key == key:
            return  # duplicate key
        new_node = Node(key, value)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None
        self.root = new_node

    def inorder(self, node=None):
        if node is None:
            node = self.root
        result = []
        if node.left:
            result.extend(self.inorder(node.left))
        result.append(node.value)
        if node.right:
            result.extend(self.inorder(node.right))
        return result
