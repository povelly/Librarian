import os
import pathlib
import time
import re
import pickle
LIBRARY = str(pathlib.Path().absolute()) + os.path.sep + \
    "static" + os.path.sep + "library"


class Node():
    """un noeud possède un identifiant (fileName) et une liste d'arcs vers d'autre noeuds, chaque arc est
        représenté par une pair (fileName, distance) avec fileName = nom du noeud vers lequel va l'arc
        et distance = distance de jaccard entre les deux noeuds qui composent l'arc"""

    def __init__(self, fileName, links=None):
        self.fileName = fileName
        self.links = links or []  # list of pair (fileName, distance)
        # calcule la liste des mots du livre et la stock pour éviter calculs multiples
        self.words = set()
        with open(LIBRARY + "/" + fileName, 'r', errors="ignore") as file:
            for line in file:
                line = re.sub('[^A-Za-z]+', ' ', line)
                for word in line.split():
                    self.words.add(word.lower())

    def __str__(self):
        return "Node(" + self.fileName + "):\n  Links:" + str(self.links) + "]"

    def add_link(self, fileName, distance):
        if fileName == self.fileName:
            return
        self.links.append((fileName, distance))

    def distance(self, node):
        return (len(self.words.union(node.words)) - len(self.words.intersection(node.words))) / len(self.words.union(node.words))


class Graph():
    """un graphe est un ensemble de noeuds, stockés dans une liste"""

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
        """Créer un graph de jaccard, sommets = noms des fichiers"""
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
            for j in range(i+1, len(graph.nodes)):
                n2 = graph.nodes[j]
                # si distance entre les deux noeuds < p, on créer une arrete entre les deux noeuds
                distance = n1.distance(n2)
                if distance < p:
                    n1.add_link(n2.fileName, distance)
                    n2.add_link(n1.fileName, distance)
        return graph


def closeness_ranking(jaccard, book_list):
    """trie la liste par closeness ranking en ordre decroissant"""

    def ranking(node):
        """donne un rank au noeud"""
        sum = 0
        for link in bookNode.links:
            # on ajoute la distance associé à chaque arc à la somme
            sum += link[1]
        # dans le cas ou le noeud n'as pas d'arcs, son ranking est le plus mauvais : 0
        if sum == 0:
            return 0
        return 1 / sum

    def insert(res_list, bookName, bookRank):
        """insert bookName de rank bookRank au bon endroit dans res_list 
        pour que la liste contiennent tout les livres par ranking decroissant.
        La list est de forme [(bookName, bookRank)]"""
        # si la liste est vide, on ajoute l'élément
        if len(res_list) == 0:
            res_list.append((bookName, bookRank))
        else:
            # on parcourt la list et insert l'élement au bon endroit
            isInserted = False
            for i in range(len(res_list)):
                if res_list[i][1] < bookRank:
                    res_list.insert(i, (bookName, bookRank))
                    isInserted = True
                    break
            # si il n'a pas été inséré, il a le plus grand rang, on l'insert à la fin
            if not isInserted:
                res_list.append((bookName, bookRank))

    res = []
    # on parcourt la liste des livres à classés
    for bookName in book_list:
        # on récupère le noeud associé au livre dans le graphe
        bookNode = None
        for node in jaccard.nodes:
            if node.fileName == bookName:
                bookNode = node
                break
        # on calcul le rank du livre
        bookRank = ranking(bookNode)
        # on insert le livre au bon endroit dans la liste
        insert(res, bookName, bookRank)
    # on enleve les ranking dans res pour ne garde que les bookName
    res = [elem[0] for elem in res]
    return res


if __name__ == "__main__":
    # create jaccard graph
    j = Graph.jaccard()
    # save the graph to a file
    pickle.dump(j, open("./static/jaccard.p", "wb"))
    # jaccard = pickle.load(open("./static/jaccard.p", "rb"))
    # closeness_ranking(jaccard, ["110.txt", "119.txt", "125.txt"])

    # print(data)
