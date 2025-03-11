# Récupération du cipher
cipher_file = open("cipher.txt", "r", encoding="utf8")
cipher_text = str(cipher_file.readlines())
print("Cipher:",cipher_text)

alphabet = "abcdefghijklmnopqrstuvwxyz"
cipher_letters = ""

# Récupération des caractères alphabétiques
status = True
for letter in cipher_text:
    if letter == '\\':
        status = False
    elif letter.lower() in alphabet and status:
        cipher_letters += letter.lower()
    else:
        status = True

print("Texte:\n", cipher_letters, '\n\n')


sequences = []
sequences_only = []

# Analyse de fréquence
i = 0
k = 3
status = False
while i != len(cipher_letters)-4:
    if cipher_letters[i:k] in cipher_letters[k:]:
        status = True
        temp_seq = cipher_letters[i:k]
        k += 1
    elif status:
        if cipher_letters[i:k-1] not in sequences_only:
            sequences.append([cipher_letters[i:k-1], cipher_letters.index(cipher_letters[i:k-1]), cipher_letters[k:].index(cipher_letters[i:k-1])+k])
            sequences[len(sequences)-1].append(abs(sequences[len(sequences)-1][2] - sequences[len(sequences)-1][1]))
            sequences_only.append(cipher_letters[i:k-1])
        i = k
        k = i+3
        status = False
    elif k > i+10 or k == len(cipher_letters)-1:
        i += 1
        k = i+3
    else:
        k += 1

# Séparation des statistiques
distances = []
sequences_only = []
sequences_lenght = []
for seq in sequences:
    distances.append(seq[3])
    sequences_only.append(seq[0])
    sequences_lenght.append(len(seq[0]))

# Analyse de longueur de clée
diviseurs = []
for diviseur in range (2, 20):
    status = True
    for lenght in sequences_lenght:
        if lenght % diviseur != 0 and lenght>diviseur:
            status = False
    if status:
        diviseurs.append(diviseur)
    
print("Diviseurs:\n", diviseurs, '\n\n')

key_lenght = 18
# Récupération des lettres selon emplacement
chaines = []
for indice in range (key_lenght):
    chaine = ""
    for index in range (indice, len(cipher_letters), key_lenght-1):
        chaine += cipher_letters[index]
    chaines.append(chaine)

print("Chaînes:\n", chaines, '\n\n')

# Récupération de la lettre la plus fréquente pour chaque chaines
most_frequent_letters = [0 for number in range (key_lenght)]
for indice in range (len(chaines)):
    a = 0
    for letter in alphabet:
        freq = chaines[indice].count(letter)
        if freq > a:
            a = freq
            most_frequent_letters[indice] = letter

print("Lettres les plus fréquentes pour chaque chaines:\n", most_frequent_letters, '\n\n')

# Détermination de la clée
key = ""
alphabets = {}
for indice in range (len(chaines)):
    decalage = alphabet.index("e") - alphabet.index(most_frequent_letters[indice])
    new_alphabet = [alphabet[(i - decalage) % len(alphabet)] for i in range (len(alphabet))]
    key += new_alphabet[0]
    alphabets[new_alphabet[0]] = new_alphabet


key = "guardialyonguardia"
print("Clé:\n", key, '\n\n')
print(alphabets)

clair_text = ""
for i in range (len(cipher_letters)):
    clair_text += alphabet[alphabet.index(cipher_letters[i]) - alphabet.index(key[i % 18])]


print("Key:\n", key)
print("Text:\n", clair_text, '\n\n')







        





