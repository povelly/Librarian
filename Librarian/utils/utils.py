import os
import requests
import json
import re
import pickle
from ..models.graph import closeness_ranking

try:
    from Librarian import env
except:
    LIBRARY = os.path.dirname(os.path.dirname(
        __file__)) + os.path.sep + "static" + os.path.sep + "library"


# on load le graph de jaccard
jaccard = pickle.load(open("./static/jaccard.p", "rb"))

# on load la table d'index
indexing = pickle.load(open("./static/indexing.p", "rb"))


def basic_search_on_index(keyword, indexing):
    occurences = indexing.get(keyword)
    if occurences is not None:
        return occurences
    else:
        return 0


def suggestion(jaccard, book_list):
    res = set()
    # on parcourt la liste de livres résultat
    for i, bookName in enumerate(book_list):
        # on visite au plus les voisins des 3 premiers, jusqu'a avoir max 10 suggestion
        if i > 2 or len(res) > 10:
            break
        # on trouve le noeud dans jaccard
        for node in jaccard.nodes:
            if bookName == node.fileName:
                # on ajoute ses voisins
                for link in node.links:
                    if len(res) < 10:
                        res.add(link[0])
                    else:
                        break
    return list(res)


def KMP(pattern, text):
    tab = [0] * len(pattern)               # Tableau du pattern
    occurences = 0

    i = 0                                  # Indice dans le text
    j = 0                                  # Indice dans le pattern

    while i < len(text):                   # Pour chaque caractere du texte
        if text[i] == pattern[j]:          # Si le texte colle au pattern jusque là
            if j == len(pattern) - 1:      # Si le dernier caractère du pattern est ok
                occurences += 1            # On incrémente le nombre d'occurences
                tab = [0] * len(pattern)   # Reset
                j = 0
            else:
                j += 1                     # Sinon on passe au caractere suivant du pattern
            i += 1
        else:                              # Si les caractères ne sont pas identiques
            if j >= 1:
                j = tab[j - 1]
            else:
                i += 1
    return occurences


def map_library(pattern, criterion):
    # on récupère la liste de tout les livres qui contiennent pattern
    matches = []
    book_count = 0

    for fileName in indexing:
        occurences = criterion(pattern, indexing.get(fileName))
        if occurences > 0:
            matches.append(fileName)
        book_count = book_count + 1
    # on trie la liste par closeness ranking
    matches = closeness_ranking(jaccard, matches)
    # on recupère les suggestions
    suggestions = suggestion(jaccard, matches)
    # on construit le resultat
    res = {"results": matches, "suggestions": suggestions}
    return json.dumps(res)

# retourne la liste de tout les mots du livre bookname


def get_keywords(bookname):
    res = set()
    with open(LIBRARY + "/" + bookname, 'r', errors="ignore") as file:
        for line in file:
            line = re.sub('[^A-Za-z]+', ' ', line)
            for word in line.split():
                print(word.lower())
                res.add(word.lower())
        return res
