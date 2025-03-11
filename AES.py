import math
import random

# Table S-Box pour la substitution des octets
s_box = {
    0: 99,   1: 124,   2: 119,   3: 123,   4: 242,   5: 107,   6: 111,   7: 197,  
    8: 48,   9: 1,     10: 103,  11: 43,   12: 254,  13: 215,  14: 127,  15: 227,  
    16: 2,    17: 225,  18: 170,  19: 228,  20: 199,  21: 248,  22: 201,  23: 125,  
    24: 89,   25: 79,   26: 171,  27: 18,   28: 28,   29: 60,   30: 150,  31: 5,    
    32: 88,   33: 224,  34: 196,  35: 9,    36: 82,   37: 210,  38: 7,    39: 67,   
    40: 77,   41: 51,   42: 131,  43: 163,  44: 201,  45: 18,   46: 134,  47: 41,   
    48: 1,    49: 93,   50: 127,  51: 234,  52: 47,   53: 66,   54: 11,   55: 113,  
    56: 41,   57: 66,   58: 3,    59: 199,  60: 214,  61: 33,   62: 46,   63: 58,   
    64: 118,  65: 14,   66: 174,  67: 143,  68: 77,   69: 60,   70: 62,   71: 59,   
    72: 243,  73: 138,  74: 36,   75: 44,   76: 197,  77: 77,   78: 3,    79: 240,  
    80: 83,   81: 106,  82: 219,  83: 87,   84: 92,   85: 101,  86: 120,  87: 177,  
    88: 122,  89: 40,   90: 107,  91: 135,  92: 11,   93: 60,   94: 44,   95: 144,  
    96: 211,  97: 19,   98: 93,   99: 98,   100: 72,  101: 49,   102: 87,   103: 139, 
    104: 71,  105: 88,   106: 114,  107: 143,  108: 99,   109: 122,  110: 56,   111: 48,  
    112: 48,   113: 144,  114: 23,   115: 60,   116: 239,  117: 76,   118: 184,  119: 146,  
    120: 42,   121: 87,   122: 67,   123: 137,  124: 134,  125: 116,  126: 0,    127: 64,  
    128: 0,    129: 96,   130: 47,   131: 4,    132: 177,  133: 39,   134: 189,  135: 249,  
    136: 230,  137: 63,   138: 84,   139: 92,   140: 136,  141: 46,   142: 116,  143: 124,  
    144: 35,   145: 189,  146: 7,    147: 187,  148: 155,  149: 102,  150: 222,  151: 123,  
    152: 0,    153: 56,   154: 45,   155: 38,   156: 55,   157: 13,   158: 40,   159: 81,  
    160: 27,   161: 31,   162: 39,   163: 96,   164: 98,   165: 144,  166: 60,   167: 62,  
    168: 44,   169: 176,  170: 24,   171: 125,  172: 68,   173: 99,   174: 173,  175: 213,  
    176: 147,  177: 124,  178: 131,  179: 33,   180: 83,   181: 176,  182: 77,   183: 231,  
    184: 144,  185: 107,  186: 6,    187: 248,  188: 137,  189: 141,  190: 113,  191: 160,  
    192: 119,  193: 38,   194: 28,   195: 222,  196: 10,   197: 26,   198: 75,   199: 54,  
    200: 106,  201: 97,   202: 140,  203: 48,   204: 55,   205: 126,  206: 108,  207: 149,  
    208: 70,   209: 195,  210: 89,   211: 20,   212: 165,  213: 204,  214: 56,   215: 213,  
    216: 179,  217: 161,  218: 120,  219: 133,  220: 145,  221: 81,   222: 151,  223: 202,  
    224: 27,   225: 89,   226: 173,  227: 37,   228: 56,   229: 8,    230: 104,  231: 117,  
    232: 234,  233: 22,   234: 245,  235: 122,  236: 70,   237: 65,   238: 95,   239: 142,  
    240: 213,  241: 178,  242: 114,  243: 162,  244: 0,    245: 50,   246: 178,  247: 191,  
    248: 18,   249: 15,   250: 55,   251: 16,   252: 24,   253: 211,  254: 222,  255: 41
}

# Fonction de chiffrement AES CBC
def chiffrement_aes_cbc(string):
    key = generate_random_bytes()  # Génère une clé 4x4
    IV = generate_random_bytes()   # Génère un IV 4x4

    # Conversion du message en une liste d'hexadécimaux
    hex_array = string_to_hex(string)

    # Ajout d'un padding
    hex_array = add_padd(hex_array)

    # Mise sous forme de matrices
    list_matrix = list_to_matrix(hex_array)

    # XOR entre le premier bloc du message et l'IV
    list_matrix = xor_blocs_and_IV(list_matrix, IV)

    # Chiffrement AES pour le premier Bloc
    list_matrix = first_bloc_AES(list_matrix, key)

    # Chiffrement AES pour les autres Blocs
    if len(list_matrix) != 1:
        list_matrix = blocs_AES(list_matrix, key)

    # Concaténation du ciphertext
    cipher_text = concat_to_string(list_matrix)

    return cipher_text, key, IV


# Fonction de conversion de string à hexadécimale
def string_to_hex(string):
    hex_array = []
    for char in string:
        hex_array.append(ord(char))  # Utilise ord pour obtenir le code Unicode du caractère
    return hex_array


# Fonction d'ajout de padding
def add_padd(hex_array):
    padding_length = 16 - (len(hex_array) % 16)
    if padding_length != 16:
        hex_array.extend([0] * padding_length)  # Ajoute des zéros pour le padding
    return hex_array


# Fonction de mise sous forme de Matrices
def list_to_matrix(hex_array):
    list_matrix = []
    for i in range(0, len(hex_array), 16):
        block = hex_array[i:i + 16]
        if len(block) < 16:
            block += [0] * (16 - len(block))  # Padding avec des zéros si nécessaire
        matrix = [block[j:j + 4] for j in range(0, 16, 4)]
        list_matrix.append(matrix)
    return list_matrix


# Fonction de XOR entre le premier bloc du message et l'IV
def xor_blocs_and_IV(list_matrix, IV):
    if len(list_matrix) == 0:
        return list_matrix
    for i in range(4):
        for k in range(4):
            list_matrix[0][i][k] = list_matrix[0][i][k] ^ IV[i][k]
    return list_matrix


# Fonction SubBytes
def sub_bytes(bloc):
    for i in range(4):
        for k in range(4):
            bloc[i][k] = s_box[bloc[i][k]]
    return bloc


# Fonction ShiftRows
def shift_rows(bloc):
    bloc[1] = [bloc[1][1], bloc[1][2], bloc[1][3], bloc[1][0]]
    bloc[2] = [bloc[2][2], bloc[2][3], bloc[2][0], bloc[2][1]]
    bloc[3] = [bloc[3][3], bloc[3][0], bloc[3][1], bloc[3][2]]
    return bloc


# Fonction MixColumns
def mix_columns(bloc):
    standard_matrix = [[2, 3, 1, 1], [1, 2, 3, 1], [1, 1, 2, 3], [3, 1, 1, 2]]
    for i in range(4):
        column = [bloc[0][i], bloc[1][i], bloc[2][i], bloc[3][i]]
        for j in range(4):
            bloc[j][i] = galois_multiplication(standard_matrix[j][0], column[0]) ^ \
                         galois_multiplication(standard_matrix[j][1], column[1]) ^ \
                         galois_multiplication(standard_matrix[j][2], column[2]) ^ \
                         galois_multiplication(standard_matrix[j][3], column[3])
    return bloc


# Fonction XOR entre 2 blocs
def xor_two_blocs(bloc1, bloc2):
    for i in range(4):
        for k in range(4):
            bloc1[i][k] = bloc1[i][k] ^ bloc2[i][k]
    return bloc1


# Expansion de la clé
def key_expension(key):
    list_keys = []
    list_words = key
    round_constant = [1, 2, 4, 8, 16, 32, 64, 128, 27, 54]

    for i in range(4, 44):
        if i % 4 == 0:
            temp = xor_two_words(xor_two_words(list_words[i - 4], sub_word(rot_word(list_words[i - 1]))),
                                [round_constant[math.floor(i / 4) - 1], 0, 0, 0])
            list_words.append(temp)
        else:
            list_words.append(xor_two_words(list_words[i - 4], list_words[i - 1]))

    for i in range(0, len(list_words), 4):
        list_keys.append(list_words[i:i + 4])
    return list_keys


# RotWord sur un mot
def rot_word(word):
    return [word[1], word[2], word[3], word[0]]


# SubWord sur un mot
def sub_word(word):
    return [s_box[word[i]] for i in range(4)]


# XOR entre 2 mots
def xor_two_words(word1, word2):
    return [word1[i] ^ word2[i] for i in range(4)]


# Multiplication dans GF(2^8)
def galois_multiplication(a, b):
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a
        a <<= 1
        if a & 0x100:
            a ^= 0x11B
        b >>= 1
    return p & 0xFF


# Fonction de chiffrement AES pour le premier Bloc
def first_bloc_AES(list_matrix, key):
    first_bloc = list_matrix[0]
    list_keys = key_expension(key)
    for j in range(10):
        first_bloc = sub_bytes(first_bloc)
        first_bloc = shift_rows(first_bloc)
        if j != 9:
            first_bloc = mix_columns(first_bloc)
        first_bloc = xor_two_blocs(first_bloc, list_keys[j])
    list_matrix[0] = first_bloc
    return list_matrix


# Fonction de chiffrement AES pour les autres Blocs
def blocs_AES(list_matrix, key):
    list_keys = key_expension(key)
    for i in range(1, len(list_matrix)):
        bloc = list_matrix[i]
        bloc = xor_two_blocs(bloc, list_matrix[i - 1])
        for j in range(10):
            bloc = sub_bytes(bloc)
            bloc = shift_rows(bloc)
            if j != 9:
                bloc = mix_columns(bloc)
            bloc = xor_two_blocs(bloc, list_keys[j])
        list_matrix[i] = bloc
    return list_matrix


# Fonction de génération d'un IV ou d'une clé secrète (AES CBC) (128 bits)
def generate_random_bytes():
    return [[random.randint(0, 255) for _ in range(4)] for _ in range(4)]


# Concaténation du ciphertext
def concat_to_string(list_matrix):
    cipher_text = ""
    for matrix in list_matrix:
        for row in matrix:
            for byte in row:
                cipher_text += f"{byte:02x}"  # Format hexadécimal
    return cipher_text


# Test
print(chiffrement_aes_cbc('lucas'))


# Fonction de déchiffrement AES CBC
def dechiffrement_aes_cbc(string, key, IV):

    # Mise sous forme de blocs
    # Copie des blocs

    # Déchiffrement 1er bloc
        # Décryption
        # Xor IV

    # Déchiffrement autres blocs
        # Décryption
        # XOR blocs précédents chiffrer

    # concaténation
    # hex to ascii

    return 

