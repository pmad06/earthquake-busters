from typing import Optional, List

class Earthquake:
    def __init__(self, magnitude, location, lat, long, url, title):
        self.magnitude = magnitude
        self.location = location
        self.lat = lat
        self.long = long
        self.url = url
        self.title = title

class Splay:
    def __init__(self, quake: Earthquake):
        self.quake = quake
        self.left: Optional['Splay'] = None
        self.right: Optional['Splay'] = None

class SplayTree:
    def __init__(self):
        self.root: Optional[Splay] = None

    def _right_rotate(self, x: Splay) -> Splay:
        y = x.left
        x.left = y.right
        y.right = x
        return y
    
    def _left_rotate(self, x: Splay) -> Splay:
        y = x.right
        x.right = y.left
        y.left = x
        return y
    
    def splay(self, root: Optional[Splay], key: float, key_attr: str) -> Optional[Splay]:
        if root is None or getattr(root.quake, key_attr) == key:
            return root

        if getattr(root.quake, key_attr) > key:
            if root.left is None:
                return root
            if getattr(root.left.quake, key_attr) > key:
                root.left.left = self.splay(root.left.left, key, key_attr)
                root = self._right_rotate(root)
            elif getattr(root.left.quake, key_attr) < key:
                root.left.right = self.splay(root.left.right, key, key_attr)
                if root.left.right is not None:
                    root.left = self._left_rotate(root.left)
            return self._right_rotate(root) if root.left is not None else root
        else:
            if root.right is None:
                return root
            if getattr(root.right.quake, key_attr) > key:
                root.right.left = self.splay(root.right.left, key, key_attr)
                if root.right.left is not None:
                    root.right = self._right_rotate(root.right)
            elif getattr(root.right.quake, key_attr) < key:
                root.right.right = self.splay(root.right.right, key, key_attr)
                root = self._left_rotate(root)
            return self._left_rotate(root) if root.right is not None else root
    
    def insert(self, quake: Earthquake, key_attr: str):
        key = getattr(quake, key_attr)

        if not self.root:
            self.root = Splay(quake)
            return  
        
        self.root = self.splay(self.root, getattr(quake, key_attr), key_attr)

        if key < getattr(self.root.quake, key_attr):
            new_node = Splay(quake)
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
            self.root = new_node
        elif key > getattr(self.root.quake, key_attr):
            new_node = Splay(quake)
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None
            self.root = new_node
        else: 
            self.root.quake = quake
    
    def range_query(self, key_attr: str, low: float, high: float) -> List[Earthquake]:
        result = []
        def inorder(node: Optional[Splay]):
            if not node: 
                return 
            val = getattr(node.quake, key_attr)
            if val > low:
                inorder(node.left)
            if low <= val <= high:
                result.append(node.quake)
            if val < high:
                inorder(node.right)
        inorder(self.root)
        return result
    
