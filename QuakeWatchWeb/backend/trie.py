#constructor
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.data = [] #quake objects

class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.wordCtr = 0

#destructor
    def __del__(self):
        self.clear()
        del self.root

    def insert(self, word : str, quake_obj: dict):
        wordNorm = self.normalize(word)
        if not wordNorm:
            return
        
        node = self.root
        for c in wordNorm:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
            node.data.append(quake_obj)

        if not node.is_end_of_word:
            node.is_end_of_word = True
            self.wordCtr += 1
        
    def search(self, word : str) -> bool:
        wordNorm = self.normalize(word)
        if not wordNorm:
            return False
        
        node = self.root
        for c in wordNorm:
            if c not in node.children:
                return False
            node = node.children[c]
        return node.is_end_of_word

    def autocomplete(self, prefix : str, limit: int = 0):
        prefixNorm = self.normalize(prefix)
        #results = []
        if not prefixNorm:
            return []
        
        node = self.findNode(prefixNorm)
        if not node:
            return []
        
        results = node.data
        if limit > 0:
            results = results[:limit]
        return results
        #if node:
        #    self.dfs(node, prefixNorm, results, limit)
        #return results

    def dfs(self, node, prefix: str, out: list, limit: int):
        if node is None:
            return
        
        if limit > 0 and len(out) >= limit:
            return
        
        if node.is_end_of_word:
            out.append(prefix)
            
        keys = sorted(node.children.keys())
        
        for c in keys:
            if limit > 0 and len(out) >= limit:
                break
            self.dfs(node.children[c], prefix + c, out, limit)

    def findNode(self, prefix: str):
        node = self.root
        for c in prefix:
            if c not in node.children:
                return None
            node = node.children[c]
        return node

    def clear(self):
        def clear_node(node):
            for child in node.children.values():
                self.freeNode(child)
        clear_node(self.root)
        self.root.children.clear()
        self.wordCtr = 0

    def freeNode(self, node):
        for child in node.children.values():
            self.freeNode(child)
        del node

    def normalize(self, word: str) -> str:
        out = []
        for c in word:
            if c.isalnum() or c in ['.', '-']:  # ✅ allow digits, letters, dot, minus
                out.append(c.lower())
            elif c.isspace():
                if not out or out[-1] != ' ':
                    out.append(' ')
        if out and out[0] == ' ':
            out = out[1:]
        if out and out[-1] == ' ':
            out = out[:-1]
        return ''.join(out)