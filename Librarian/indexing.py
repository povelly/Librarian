import os
import pathlib
from collections import Counter
import re
import pickle

LIBRARY = str(pathlib.Path().absolute()) + os.path.sep + \
    "static" + os.path.sep + "library"


def create_index():
    # le resultat sera une Map<Int, Map<String, Int>> avec Map<nomfichier, Map<mot,occurences>>
    res = dict()
    # on parcourt chaque fichier de la base et chaque mot des fichiers
    for i, fileName in enumerate(os.listdir(LIBRARY)):
        if ".txt" in fileName:
            print("Indexing file : " + str(i) + "(" + fileName + ")")
            with open(LIBRARY + "/" + fileName, 'r', errors="ignore") as file:
                # on ajoute tout les mots dans une list
                words = []
                for line in file:
                    line = re.sub('[^A-Za-z]+', ' ', line)
                    for word in line.split():
                        words.append(word.lower())
                # on créer la map qui associe à chaque mot son nombre d'occurences
                words = Counter(words)
                # on ajoute a la map res la map du fichier actuel
                res[fileName] = words
    return res


if __name__ == "__main__":
    # on créer la map
    index = create_index()
    # on la sauvegarde
    pickle.dump(index, open("./static/indexing.p", "wb"))
