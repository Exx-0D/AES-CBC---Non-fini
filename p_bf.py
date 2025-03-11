alphabet = "abcdefghijklmnopqrstuvwxyz"

def string_extraction(path):
    """
    Retourne le texte contenu dans un fichier donné
    """
    with open(path, "r", encoding="utf8") as cipher_file:
        return cipher_file.read()

def generate_keys(length, alphabet, current_key="", keys=None):
    if keys is None:
        keys = [] 

    if len(current_key) == length:
        grille = generate_grille(current_key)
        clair = clair_text(string, grille)
        if "formidable" in clair:
            print(clair, '\n\n', current_key)
            keys.append(current_key)
        return keys

    for char in alphabet:
        generate_keys(length, alphabet, current_key + char, keys)

    return keys

def generate_grille(key):
    key = key.replace("j", "i")
    unique_chars = []
    for char in key:
        if char not in unique_chars and char in alphabet:
            unique_chars.append(char)
    for char in alphabet:
        if char not in unique_chars and char != "j":
            unique_chars.append(char)
    grille = {}
    for line in range(1, 6):
        for row in range(1, 6):
            grille[str(line) + str(row)] = unique_chars[(line - 1) * 5 + row - 1]
    return grille

def clair_text(string, grille):
    """
    Retourne le texte déchiffré
    """
    clair = ""
    for indice in range(0, len(string)-1, 2):
        clair += grille[string[indice:indice+2]]
    return clair

string = string_extraction('cipher_p.txt')
for lenght in range (1, 26):
    generate_keys(lenght, alphabet)