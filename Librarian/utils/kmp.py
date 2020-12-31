def KMP(pattern, text):
    # Etape 1: construction du tableau pour le pattern
    tab = [0];                          # Tableau du pattern
    i = 1
    j = 0

    while i < len(pattern):             # Tant que l'indicateur i parcour la chaine de caractère
        if pattern[j] == pattern[i]:    # Si les deux caractères sont identiques
            tab[i] = j + 1              # Le tableau a l'indice i prend la valeur de j
            i += 1                      # On incrémente les deux indices
            j += 1
        else:                           #Si pattern[i] != pattern[j]
            if j == 0:
                #tab[i] = 0
                tab.insert(i, 0)
                i += 1
            else:                       #Si j !=0
                j = tab[j - 1]

    # Etape 2: Parcours de la chaine de caractere avec notre beau tableau
    i = 0
    j = 0

    while i < len(text):                # Pour chaque caractere du texte
        if text[i] == pattern[j]:       # Si le texte colle au pattern jusque là
            if j == len(pattern) - 1:   # Si le dernier caractère du pattern est ok
                return True             # Alors true;
            else:                       # Sinon on passe au pattern suivant
                i += 1
                j += 1
        else:                           # Si les caractères ne sont pas identiques
            if j >= 1:
                j = tab[j - 1]
            else:
                i += 1
    return False;



# print(KMP("abc","erjfepgjacefjfep"))
