import env

# retourne la liste de tout les mots du livre bookname
def get_keywords(bookname):
    res = []
    with open(env.LIBRARY + "/" + bookname, 'r') as file:
        for line in file:
            for word in line.split():
                # ajoute le mot que si il n'y est pas déjà
                if not (word in res):
                    res.append(word)
        return res
