alphabet = "abcdefghijklmnopqrstuvwxyz"

def string_extraction (path):
    """
    Retourne le texte contenu dans un fichier donné
    """
    cipher_file = open(path, "r", encoding="utf8")
    return str(cipher_file.readlines())

def letters_extraction (string):
    """
    Retourne une chaîne de caractère contenant les lettres uniquements
    """
    indice = 0
    letters = ""
    while indice < len(string):
        if string[indice] == '\\':
            indice += 1
        elif string[indice].lower() in alphabet:
            letters += string[indice].lower()
        indice += 1
    return letters

def subdivision (string, n):
    """
    Subdivise le texte en n blocs. Soit x = numéro du bloc - 1, tout les blocs contiennent les caractères aux indices x + n*r pour r un entier positif.
    Retourne une liste contenant n blocs.
    """
    blocs = ['' for x in range(n)]
    for x in range (n):
        r = 0
        while x + n * r < len(string):
            blocs[x] += string[x + n * r]
            r += 1
    return blocs

def frequence (blocs):
    """
    Retourne une liste contenant la lettre les plus fréquente pour chaque bloc.
    """
    frequences = ['' for x in range(len(blocs))]
    for x in range(len(blocs)):
        counter = 0
        for letter in alphabet:
            if blocs[x].count(letter) > counter:
                counter = blocs[x].count(letter)
                frequences[x] = letter
    return frequences

def cle (frequences):
    """
    Retourne la clé associé au texte chiffré.
    La fonction part du principe que la lettre "e" est la plus fréquente dans le texte clair tout comme dans la langue française.
    """
    key = ""
    for letter in frequences:
        key += alphabet[alphabet.index(letter) - alphabet.index("e")]
    return key

def dechiffre (string, key):
    """
    Retourne le texte string déchiffré à l'aide de la clé fournie.
    Déchiffre en fonction du chiffrement de Vigenere.
    """
    clair = ""
    for indice in range (len(string)):
        clair += alphabet[alphabet.index(string[indice]) - alphabet.index(key[indice % 18])]
    return clair

def construct (string1, string2):
    """
    Retourne le text original (contenant des ponctuation...) déchiffré.
    """
    string3 = ""
    original = ""
    indice2 = 0
    indice1 = 0
    while indice1 < len(string1):
        if string1[indice1] == '\\':
            string3 += string1[indice1] + string1[indice1 + 1]
            indice1 += 1
        elif string1[indice1] in alphabet:
            string3 += string2[indice2]
            indice2 += 1
        elif string1[indice1].lower() in alphabet:
            string3 += string2[indice2].upper()
            indice2 += 1
        else:
            string3 += string1[indice1]
        indice1 += 1
    return string3

        
string = string_extraction('cipher.txt')
letters = letters_extraction(string)

for lenght in range (13, 20):
    blocs = subdivision(letters, lenght)
    frequences = frequence(blocs)
    key = cle(frequences)
    print(key)

# On présume que la clé est:
key = 'guardialyonguardia'
clair = dechiffre(letters, key)
original = construct(string, clair)
print('\n\n',key, ':')
print(original)