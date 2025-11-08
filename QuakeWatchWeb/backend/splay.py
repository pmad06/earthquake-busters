from typing import Optional, List



#https://www.geeksforgeeks.org/dsa/searching-in-splay-tree/
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = [value]  # store a list of values
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None

class SplayTree:
    def __init__(self):
        self.root: Optional[Node] = None

    def _right_rotate(self, x: Node) -> Node:
        y = x.left
        x.left = y.right
        y.right = x
        return y

    def _left_rotate(self, x: Node) -> Node:
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def _splay(self, root: Optional[Node], key) -> Optional[Node]:
        if root is None or root.key == key:
            return root

        if key < root.key:
            if root.left is None:
                return root
            if key < root.left.key:  # Zig-Zig
                root.left.left = self._splay(root.left.left, key)
                root = self._right_rotate(root)
            elif key > root.left.key:  # Zig-Zag
                root.left.right = self._splay(root.left.right, key)
                if root.left.right:
                    root.left = self._left_rotate(root.left)
            return root if root.left is None else self._right_rotate(root)
        else:
            if root.right is None:
                return root
            if key < root.right.key:  # Zag-Zig
                root.right.left = self._splay(root.right.left, key)
                if root.right.left:
                    root.right = self._right_rotate(root.right)
            elif key > root.right.key:  # Zag-Zag
                root.right.right = self._splay(root.right.right, key)
                root = self._left_rotate(root)
            return root if root.right is None else self._left_rotate(root)

    def insert(self, key, value):
        if self.root is None:
            self.root = Node(key, value)
            return
        self.root = self._splay(self.root, key)
        if self.root.key == key:
            # If duplicate, append value to the existing node
            self.root.value.append(value)
            return
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

    def search(self, key) -> Optional[List]:
        """
        Splay the node with `key` to root and return its value list.
        If not found, return None.
        """
        if self.root is None:
            return None
        self.root = self._splay(self.root, key)
        if self.root.key == key:
            return self.root.value
        return None

    def inorder(self, node=None):
        if node is None:
            node = self.root
        result = []
        if node.left:
            result.extend(self.inorder(node.left))
        result.append(node.value)  # append the list of values
        if node.right:
            result.extend(self.inorder(node.right))
        return result
