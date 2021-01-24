import os
import requests
import json
try:
    from Librarian import env
except:
    LIBRARY = os.path.dirname(os.path.dirname(
        __file__)) + os.path.sep + "static" + os.path.sep + "library"


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
    matches = []
    book_count = 0
    for fileName in os.listdir(env.LIBRARY):
        with open(os.path.join(env.LIBRARY, fileName), 'r', errors="ignore") as f:
            print("processing search : ", book_count, " book")
            occurences = criterion(pattern, f.read())
            if occurences > 0:
                matches.append({"file": fileName, "occurences": occurences})
        book_count = book_count + 1
        if len(matches) > 10:
            break
    return json.dumps(matches)
