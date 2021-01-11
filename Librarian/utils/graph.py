import os
try:
    from Librarian import env
except:
    LIBRARY = os.path.dirname(os.path.dirname(__file__)) + os.path.sep + "static" + os.path.sep + "library"
from utils import map_library

class Node():
    def __init__(self, fileName):
        self.fileName = fileName
        self.content = []
        with open(os.path.join(env.LIBRARY, fileName), 'r') as f:
            for w in f.read():
                self.content.append(w)

class Array():
    def __init__(self, n1,n2):
        pass

class Graph():
    def __init__(self, nodes = []):
        self.nodes = nodes
    def add(self, node):
        self.nodes.append(node)

def jaccard():
    def distance():
        return 0.5
    graph = Graph()
    for fileName in os.listdir(LIBRARY):
        graph.add(Node(fileName))
    return graph

if __name__ == "__main__":
    print(jaccard())
