import os
import pathlib
import time
import re
LIBRARY = str(pathlib.Path().absolute()) + os.path.sep + \
    "static" + os.path.sep + "library"


class Node():
    def __init__(self, fileName, links=None):
        self.fileName = fileName
        self.links = links or []
        # calcule la liste des mots du livre et la stock pour éviter calculs multiples
        self.words = set()
        with open(LIBRARY + "/" + fileName, 'r', errors="ignore") as file:
            for line in file:
                line = re.sub('[^A-Za-z]+', ' ', line)
                for word in line.split():
                    self.words.add(word.lower())

    def __str__(self):
        res = "Node(" + self.fileName + "):\n  Links:["
        for i in range(len(self.links) - 1):
            res += self.links[i] + ", "
        if len(self.links) > 0:
            res += self.links[len(self.links) - 1]
        return res + "]"

    def add_link(self, fileName):
        if fileName == self.fileName:
            return
        self.links.append(fileName)

    def distance(self, node):
        return (len(self.words.union(node.words)) - len(self.words.intersection(node.words))) / len(self.words.union(node.words))
        # return 1 - len(words_self.intersection(words_node)) / len(words_self.union(words_node))


class Graph():
    def __init__(self, nodes=[]):
        self.nodes = nodes

    def __str__(self):
        res = "Graph():\n  Nodes:["
        for i in range(len(self.nodes) - 1):
            res += self.nodes[i].fileName + ", "
        if len(self.nodes) > 0:
            res += self.nodes[len(self.nodes) - 1].fileName
        return res + "]"

    def add_node(self, node):
        self.nodes.append(node)

    @ staticmethod
    def jaccard(p=0.65):
        graph = Graph()
        # on met tout les livres comme sommet du graphe
        for i, fileName in enumerate(os.listdir(LIBRARY)):
            if ".txt" in fileName:  # pour ne pas ajouter le script .sh
                print("Create node for book number " +
                      str(i) + " (" + fileName + ")")
                graph.add_node(Node(fileName))
        # pour chaque noeud du graphe
        for i in range(len(graph.nodes)):
            print("Create links for node number " + str(i) +
                  " (" + graph.nodes[i].fileName + ")")
            n1 = graph.nodes[i]
            # pour chaque autre noeud du graphe
            for j in range(len(graph.nodes)):
                if i != j:
                    n2 = graph.nodes[j]
                    # si distance entre les deux noeuds < p, on créer une arrete entre les deux noeuds
                    if n1.distance(n2) < p:
                        n1.add_link(n2.fileName)
                        n2.add_link(n1.fileName)
        return graph


"""
def distance(n1, n2):
    size_intersection = 0
    size_union = 0
    s1 = set()
    s2 = set()
    with open(LIBRARY + os.path.sep + n1.fileName, 'r') as file:
        for line in file:
            for word in line.split():
                s1.add(word)
    with open(LIBRARY + os.path.sep + n2.fileName, 'r') as file:
        for line in file:
            for word in line.split():
                s2.add(word)
    return 1 - len(s1.intersection(s2)) / len(s1.union(s2))

def jaccard_old(p = 0.70):
    def distance_bouchon(n1, n2): # bouchon
        return 0.4

    # def distance_naive(n1, n2): # algo naif pour la distance Jaccard
    #     def get_keywords(book_name):
    #         res = []
    #         with open(LIBRARY + os.path.sep + book_name, 'r') as file:
    #             for line in file:
    #                 for word in line.split():
    #                     if word not in res:
    #                         res.append(word)
    #             return res
    #     n1_words = get_keywords(n1.fileName)
    #     size_intersection = 0
    #     size_union = len(n1_words)
    #     for w in get_keywords(n2.fileName):
    #         if w in n1_words:
    #             size_intersection += 1
    #         else:
    #             size_union += 1
    #     return 1 - size_intersection / size_union

    graph = Graph()

    for fileName in os.listdir(LIBRARY):
        graph.add_node(Node(fileName))

    for i in range(len(graph.nodes)):
        n1 = graph.nodes[i]
        for j in range(i + 1, len(graph.nodes)):
            n2 = graph.nodes[j]
            # starting_time = time.process_time()
            # dn = distance_naive(n1, n2)
            # time_elapsed = time.process_time() - starting_time
            # print("time elapsed, distance(): ", time_elapsed)
            # print("dn: ", dn)
            # starting_time2 = time.process_time()
            # d = distance(n1, n2)
            # time_elapsed2 = time.process_time() - starting_time2
            # print("time elapsed2, distance(): ", time_elapsed2)
            # print("d3: ", n1.fileName, "<>", n2.fileName, ">>", d3)
            # TODO remplacer la fonction
            if n2.fileName not in n1.links and distance(n1, n2) < p:
                n1.add_link(n2.fileName)
                n2.add_link(n1.fileName)

    # for n1 in graph.nodes:
    #     for n2 in graph.nodes:
    #         if n2.fileName not in n1.links and distance(n1, n2) < p:
    #             n1.add_link(n2.fileName)
    return graph
"""

if __name__ == "__main__":
    # j = jaccard_old()
    j = Graph.jaccard()
    print("j:", j)
    print("\nLinks:")
    for i in range(len(j.nodes)):
        print("  links[" + j.nodes[i].fileName + "]:", j.nodes[i].links)
