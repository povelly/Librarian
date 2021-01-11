from Librarian import env

# retourne la liste de tout les mots du livre bookname
def get_keywords(bookname):
    res = []
    file = open(env.LIBRARY + bookname, 'r')
    for line in file:
        for word in line:
            # ajoute le mot que si il n'y est pas déjà
            if not (word in res):
                res.append(word)
    return res
