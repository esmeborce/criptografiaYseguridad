"""
Problema 7 - Segunda parte: Descifrado PlayFair
Se utiliza la clave obtenida del descifrado DES: PEgAsuzs -> PEGASUZ
y la matriz construida según la pista.
"""

import re

def generar_matriz_playfair():
    # La pista fija la disposición de la matriz
    matriz = [
        ['P', 'E', 'G', 'A', 'S'],
        ['U', 'Z', 'B', 'C', 'D'],
        ['F', 'H', 'I', 'K', 'L'],
        ['M', 'N', 'O', 'Q', 'R'],
        ['T', 'V', 'W', 'X', 'Y']
    ]
    return matriz

def buscar_posicion(matriz, letra):
    for i, fila in enumerate(matriz):
        for j, val in enumerate(fila):
            if val == letra:
                return i, j
    return None

def descifrar_playfair(texto_cifrado, matriz):
    # Limpiar: solo letras, mayúsculas
    texto = re.sub(r'[^A-Za-z]', '', texto_cifrado).upper()
    
    # Asegurar longitud par
    if len(texto) % 2 != 0:
        texto += 'X'
        
    pares = [texto[i:i+2] for i in range(0, len(texto), 2)]
    resultado = ''
    
    for a, b in pares:
        pos_a = buscar_posicion(matriz, a)
        pos_b = buscar_posicion(matriz, b)
        
        # Manejo de error por si se cuela algo raro (no debería con el regex)
        if pos_a is None or pos_b is None:
            continue
            
        fila_a, col_a = pos_a
        fila_b, col_b = pos_b
        
        # Regla 1: Misma fila (Mover a la izquierda)
        if fila_a == fila_b:
            resultado += matriz[fila_a][(col_a - 1) % 5]
            resultado += matriz[fila_b][(col_b - 1) % 5]
        # Regla 2: Misma columna (Mover hacia arriba)
        elif col_a == col_b:
            resultado += matriz[(fila_a - 1) % 5][col_a]
            resultado += matriz[(fila_b - 1) % 5][col_b]
        # Regla 3: Rectángulo (Intercambiar columnas)
        else:
            resultado += matriz[fila_a][col_b]
            resultado += matriz[fila_b][col_a]
            
    return resultado

# Texto cifrado exacto del PDF
cifrado = """
SHPETXSQZNSPLBMBWFFKCEBRBQMVQSEGOLRBLGXPPSUXHWLGXPDL-
SZSNAZINELFTEQRGTSRIFWKBRGZVNPWKBQPGPBMZOMGEQMXPHGUF
DIKBSCMGQMSHVZXTQMFXFOGPSHBWIOSNOQNPWKKCOQMFAVSHSM-
FOSNDKHGMVSZSHQPIYSQAVPNEGCERZQBQOKSSCOFOHPYQSBKQOZSHP
FKEGKCRLSNQOIKOQOWPSTDPSBRAVGMVZQZKGFRZVVPZVSHPG-
VAOHRBGEZVEQHGWMKSNSZSRZPHZVPSZSIRDLSNAZINDLOBFWSKGPZS
MZQZOWMCAVSHGRMPXGNSPGFPKFHBMGSQSGPEKGQSFSSNOW-
BLPYSQKBSQBRQSEFSGKSKSUXHWLGXPZSZSNSZKRGFZQPOQDYSXTFRZQ
MPQRGXECNZPCEGLBQNQPCMESNOWBLPYSCGSOHQPFSRIFWKBQB-
DTQOQNDOZVMIZPUFDIKBSCNGRYCYBLQGBQOQZAMRZPBRPESNGRQEPE
SNVPVZBKZVVPPSKSSPQBKGBKQOBKWHKDZVYMMGMQZLKEIOEQGLBR-
WHUXFOSPZSGPGFQOGKAV
"""

matriz = generar_matriz_playfair()
texto_descifrado = descifrar_playfair(cifrado, matriz)

print("Texto descifrado:\n")
print(texto_descifrado)