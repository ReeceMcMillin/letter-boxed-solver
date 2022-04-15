from collections import defaultdict

class TrieNode:
    """Ripped from leetcode: https://leetcode.com/problems/implement-trie-prefix-tree/discuss/58834/AC-Python-Solution"""
    def __init__(self):
        self.children = defaultdict(TrieNode)
        self.is_word = False

class Trie:
    """Ripped from leetcode: https://leetcode.com/problems/implement-trie-prefix-tree/discuss/58834/AC-Python-Solution"""
    def __init__(self, words=None):
        self.root = TrieNode()
        if words:
            for word in words:
                self.insert(word)

    def insert(self, word):
        current = self.root
        for letter in word:
            current = current.children[letter]
        current.is_word = True

    def search(self, word):
        current = self.root
        for letter in word:
            current = current.children.get(letter)
            if current is None:
                return False
        return current.is_word

    def startsWith(self, prefix):
        current = self.root
        for letter in prefix:
            current = current.children.get(letter)
            if current is None:
                return False
        return True
