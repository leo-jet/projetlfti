import operator
import turtle
"""
Fonction qui ouvre un fichier et renvoie le tableau des caractères
"""

PONCTUATION = [".", ",", ":", "!", "?", "’", ";"]

STRICTE_EXPRESSION = ["m’", "t’", "s’", "l’","d'", "j'", "c'", "n'"]

PRONOMS_PERSONNELS_ARTICLES = ["je", "me", "pour", "n", "ne", "la", "et",
                               "moi", "tu", "te", "toi","de", "et", "il",
                               "elle", "on","se", "soi", "lui", "le", "à",
                               "nos", "la", "y", "en", "nous", "vous", "ils",
                               "elles", "mon", "ma", "mes", "ton", "ta",
                               "tes", "son", "les", "leur", "eux", "un",
                               "est", "a", "même", "si", "sont", "comme", "ont",
                               "dont", "ces", "sans",
                               "une", "au", "aux", "les", "des", "sa", "ses",
                               "avec", "sur", "du", "c", "plus", "qu", "tout",
                               "par", "mais", "tous","ce", "cette", "se", "ses",
                               "son", "parce",
                               "notre", "nos", "votre", "vos", "pas", "d", "dans"]

PRONOMS_POSSESSIFS = ["mien", "mienne", "miens", "miennes",
                      "tien", "tienne", "tiens", "tiennes",
                      "sien", "sienne", "siens", "siennes",
                      "nôtre", "nôtre", "nôtres", "vôtre",
                      "vôtre", "vôtres",
                      "leurs"]

PRONOMS_DEMONSTRATIFS = ["celui", "celle", "ceux", "celles", "ce", "ceci",
                         "cela", "ça", "celui-ci", "celle-ci", "ceux-ci",
                         "celles-ci"]

PRONOMS_INTERROGATIFS = ["qui", "que", "quoi", "lequel", "laquelle",
                         "lesquels", "lesquelles"]

PRONOMS_RELATIFS = ["qui", "que", "quoi", "dont", "où", "lequel", "laquelle",
                    "lesquels", "lesquelles"]

PRONOMS_INDEFINIS = ["personne", "certains", "rien", "quelqu",
                     "quelque", "importe"]


BLACKLIST = [PRONOMS_DEMONSTRATIFS, PRONOMS_INDEFINIS, PRONOMS_INTERROGATIFS, PRONOMS_PERSONNELS_ARTICLES, PRONOMS_POSSESSIFS]

def ouvrir_fichier_retourne_liste_ligne(nom_fichier):
    fichier = open(nom_fichier, "r")
    lignes = []
    while 1:
        ligne = fichier.readline() # lit une ligne
        if ligne == "": # la ligne est vide ?
            break # on sort de la boucle sinon...
        l = ligne.strip("\n") # affiche la ligne
        if(len(l)!=0):
            lignes.append(l)
    fichier.close()
    return lignes

def ouvrir_fichier_retourne_string(nom_fichier):
    fichier = open(nom_fichier, "r")
    lignes = ""
    while 1:
        ligne = fichier.readline()  # lit une ligne
        if ligne == "":  # la ligne est vide ?
            break  # on sort de la boucle sinon...
        l = ligne.strip("\n")  # affiche la ligne
        if (len(l) != 0):
            lignes = lignes + " " + l
    fichier.close()
    return lignes


"""
Compter le nombre d'apparition d'un caractère sur une ligne
"""
def nombre_apparition_caractere_ligne(ligne, caractere):
    return ligne.count(caractere)

def nombre_apparition_caractere_fichier(nom_fichier, caractere):
    lignes = ouvrir_fichier_retourne_liste_ligne(nom_fichier=nom_fichier)
    nb_apparition_par_ligne = []
    for ligne in lignes:
        nb_apparition = nombre_apparition_caractere_ligne(ligne=ligne, caractere=caractere)
        i = 0
        while i < len(nb_apparition_par_ligne):
            if nb_apparition_par_ligne[i]['nb_apparition']<nb_apparition:
                nb_apparition_par_ligne.insert(i,{
                    "ligne": ligne,
                    "nb_apparition": nb_apparition
                })
                break
            i = i + 1
        if i == len(nb_apparition_par_ligne):
            nb_apparition_par_ligne.append({
                "ligne": ligne,
                "nb_apparition": nb_apparition
            })

    return nb_apparition_par_ligne

def nombre_apparition_caractere_fichier_pourcentage(nom_fichier, caractere):
    lignes = ouvrir_fichier_retourne_liste_ligne(nom_fichier=nom_fichier)
    nb_apparition_par_ligne = []
    for ligne in lignes:
        nb_apparition = nombre_apparition_caractere_ligne(ligne=ligne, caractere=caractere)
        pourcentage = nb_apparition/len(ligne)*100
        i = 0
        while i < len(nb_apparition_par_ligne):
            if nb_apparition_par_ligne[i]['nb_apparition']<pourcentage:
                nb_apparition_par_ligne.insert(i,{
                    "ligne": ligne,
                    "nb_apparition": pourcentage
                })
                break
            i = i + 1
        if i == len(nb_apparition_par_ligne):
            nb_apparition_par_ligne.append({
                "ligne": ligne,
                "nb_apparition": pourcentage
            })

    return nb_apparition_par_ligne

def liste_de_mots(nom_fichier):
    texte = ouvrir_fichier_retourne_string(nom_fichier=nom_fichier)
    texte = texte.lower()
    for exp in STRICTE_EXPRESSION:
        texte = texte.replace(exp, ' ')

    for exp in PONCTUATION:
        texte = texte.replace(exp, ' ')
    total_mots = texte.split()
    mots = list(set(total_mots))
    for black_set in BLACKLIST:
        for black in black_set:
            for mot in mots:
                if mot == black:
                    mots.remove(black)
    return {"total_mots":total_mots, "mots_unique": mots}

def nombre_total_de_mot(nom_fichier):
    mots = liste_de_mots(nom_fichier)
    return len(mots["total_mots"])

def longueur_moyenne_mot(nom_fichier):
    total = nombre_total_de_mot(nom_fichier)
    mots = liste_de_mots(nom_fichier)
    somme = 0
    for mot in mots["total_mots"]:
        somme = somme + len(mot)
    moyenne = somme / total

    return moyenne

def diversite_lexicale(nom_fichier):
    mots = liste_de_mots(nom_fichier)
    lexique = []
    for mot in mots["mots_unique"]:
        lexique.append({
                "mot": mot,
                "occurence": mots["total_mots"].count(mot)
            })
    return lexique

def decoupe_fichier_en_phrase(nom_fichier):
    texte = ouvrir_fichier_retourne_string("LePen.txt")
    phrases = texte.replace(".", "$").replace("!", "$").replace("?", "$").split("$")
    return phrases

def statistiques_phrases(nom_fichier):
    phrases = decoupe_fichier_en_phrase(nom_fichier)
    nombre = len(phrases)
    somme = 0
    longueur_min = 1000000000
    longueur_max = 0
    for phrase in phrases:
        somme = somme + len(phrase)
        if len(phrase) >= longueur_max:
            longueur_max = len(phrase)
        if len(phrase) <= longueur_min:
            longueur_min = len(phrase)

    longueur_moyenne = somme/nombre

    return {
            "total_phrases": nombre,
            "longueur_moyenne": longueur_moyenne,
            "longueur_min": longueur_min,
            "longueur_max": longueur_max
        }

def statistiques_type_phrases(nom_fichier):
    texte = ouvrir_fichier_retourne_string(nom_fichier)
    return {
            "phrases_declaratives": texte.count("."),
            "phrases_interrogatives": texte.count("?"),
            "phrases_exclamative": texte.count("!"),
        }

def extraction_n_mots_plus_frequents(n, nom_fichier):
    lexique = diversite_lexicale(nom_fichier)
    lexique_trie = sorted(lexique, key=lambda k: k['occurence'])
    return lexique_trie[-n:]


def rectangle(x, y, largeur, longueur):
    turtle.up()
    turtle.goto(x, y)
    turtle.down()
    turtle.forward(largeur)
    turtle.left(90)
    turtle.forward(longueur)
    turtle.left(90)
    turtle.forward(largeur)
    turtle.left(90)
    turtle.forward(longueur)
    turtle.left(90)

turtle.setup(400,400) # Facultatif
rectangle(5,10, 30, 60)
n=input("")
turtle.update()

print(extraction_n_mots_plus_frequents(10,"LePen.txt"))



