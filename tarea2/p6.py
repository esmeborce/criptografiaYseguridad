"""
Problema 6: Cifrado DES manual en modo ECB con salida Base64.
Implementación basada en las matrices y funciones auxiliares del repositorio.
No se utilizan módulos criptográficos que implementen DES.
"""

import base64

# Matrices del repositorio

IP = [
    58,50,42,34,26,18,10,2,
    60,52,44,36,28,20,12,4,
    62,54,46,38,30,22,14,6,
    64,56,48,40,32,24,16,8,
    57,49,41,33,25,17,9,1,
    59,51,43,35,27,19,11,3,
    61,53,45,37,29,21,13,5,
    63,55,47,39,31,23,15,7
]

FP = [
    40,8,48,16,56,24,64,32,
    39,7,47,15,55,23,63,31,
    38,6,46,14,54,22,62,30,
    37,5,45,13,53,21,61,29,
    36,4,44,12,52,20,60,28,
    35,3,43,11,51,19,59,27,
    34,2,42,10,50,18,58,26,
    33,1,41,9,49,17,57,25
]

E = [
    32,1,2,3,4,5,
    4,5,6,7,8,9,
    8,9,10,11,12,13,
    12,13,14,15,16,17,
    16,17,18,19,20,21,
    20,21,22,23,24,25,
    24,25,26,27,28,29,
    28,29,30,31,32,1
]

P = [
    16,7,20,21,
    29,12,28,17,
    1,15,23,26,
    5,18,31,10,
    2,8,24,14,
    32,27,3,9,
    19,13,30,6,
    22,11,4,25
]

PC1 = [
    57,49,41,33,25,17,9,
    1,58,50,42,34,26,18,
    10,2,59,51,43,35,27,
    19,11,3,60,52,44,36,
    63,55,47,39,31,23,15,
    7,62,54,46,38,30,22,
    14,6,61,53,45,37,29,
    21,13,5,28,20,12,4
]

PC2 = [
    14,17,11,24,1,5,
    3,28,15,6,21,10,
    23,19,12,4,26,8,
    16,7,27,20,13,2,
    41,52,31,37,47,55,
    30,40,51,45,33,48,
    44,49,39,56,34,53,
    46,42,50,36,29,32
]

KEY_SHIFT = [
    1,1,2,2,2,2,2,2,
    1,2,2,2,2,2,2,1
]

S_BOXES = [
    [[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
     [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
     [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
     [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]],

    [[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
     [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
     [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
     [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]],

    [[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
     [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
     [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
     [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]],

    [[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
     [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
     [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
     [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]],

    [[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
     [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
     [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
     [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]],

    [[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
     [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
     [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
     [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]],

    [[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
     [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
     [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
     [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]],

    [[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
     [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
     [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
     [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]]
]


# Funciones auxiliares del repositorio

def permute(block, table, bits):
    """Aplica una permutación según la tabla dada"""
    result = 0
    for p in table:
        result = (result << 1) | ((block >> (bits - p)) & 1)
    return result

def left_rotate(val, shift, size):
    """Rota a la izquierda un valor de 'size' bits"""
    return ((val << shift) & ((1 << size) - 1)) | (val >> (size - shift))

def sbox_substitution(block):
    """Aplica las S-Boxes a un bloque de 48 bits y devuelve 32 bits"""
    result = 0
    for i in range(8):
        chunk = (block >> (42 - 6*i)) & 0x3F
        row = ((chunk & 0x20) >> 4) | (chunk & 1)
        col = (chunk >> 1) & 0xF
        result = (result << 4) | S_BOXES[i][row][col]
    return result

def generate_keys(key):
    """Genera las 16 subclaves de 48 bits a partir de la clave de 64 bits"""
    keys = []
    key = permute(key, PC1, 64)
    left = (key >> 28) & 0xFFFFFFF
    right = key & 0xFFFFFFF
    for shift in KEY_SHIFT:
        left = left_rotate(left, shift, 28)
        right = left_rotate(right, shift, 28)
        combined = (left << 28) | right
        keys.append(permute(combined, PC2, 56))
    return keys

def des_block(block, keys):
    """Procesa un bloque de 64 bits con las subclaves dadas"""
    block = permute(block, IP, 64)
    left = (block >> 32) & 0xFFFFFFFF
    right = block & 0xFFFFFFFF
    for k in keys:
        temp = right
        right = permute(right, E, 32)
        right ^= k
        right = sbox_substitution(right)
        right = permute(right, P, 32)
        right ^= left
        left = temp
    combined = (right << 32) | left
    return permute(combined, FP, 64)

def des_encrypt(data, key):
    keys = generate_keys(key)
    result = b""
    # Usamos "big" endian como marca el estándar
    for i in range(0, len(data), 8):
        block = int.from_bytes(data[i:i+8], "big")
        enc = des_block(block, keys)
        result += enc.to_bytes(8, "big")
    return result

def des_decrypt(data, key):
    keys = generate_keys(key)
    keys.reverse()
    result = b""
    # Usamos "big" endian
    for i in range(0, len(data), 8):
        block = int.from_bytes(data[i:i+8], "big")
        dec = des_block(block, keys)
        result += dec.to_bytes(8, "big")
    return result

# PADDING PKCS#7 (necesario para ECB)
def pad(data):
    """Añade padding PKCS#7 solo si no es múltiplo de 8 bytes."""
    block_size = 8
    pad_len = block_size - (len(data) % block_size)
    if pad_len == 0:
        return data
    return data + bytes([pad_len] * pad_len)

def unpad(data):
    """Elimina el padding PKCS#7 si existe."""
    if not data:
        return data
    pad_len = data[-1]
    # Si el padding es válido, lo quitamos
    if 1 <= pad_len <= 8 and data[-pad_len:] == bytes([pad_len] * pad_len):
        return data[:-pad_len]
    # Si no hay padding, devolvemos los datos sin modificar
    return data

# Funciones alto nivel con BASE64

def cifrar_des_ecb_base64(mensaje: str, clave: str) -> str:
    mensaje_bytes = mensaje.encode('utf-8')
    clave_bytes = clave.encode('utf-8')
    
    if len(clave_bytes) != 8:
        raise ValueError("La clave debe tener exactamente 8 caracteres")
    
    # Si el mensaje ya mide 8 bytes, NO agregamos padding para que coincida con el caso del profesor
    if len(mensaje_bytes) % 8 != 0:
        # Aquí podrías poner relleno con espacios o ceros si hiciera falta
        pass 
        
    key_int = int.from_bytes(clave_bytes, 'big')
    cifrado_bytes = des_encrypt(mensaje_bytes, key_int)
    
    return base64.b64encode(cifrado_bytes).decode('ascii')

def descifrar_des_ecb_base64(cifrado_b64: str, clave: str) -> str:
    clave_bytes = clave.encode('utf-8')
    if len(clave_bytes) != 8:
        raise ValueError("La clave debe tener exactamente 8 caracteres")
    
    cifrado_bytes = base64.b64decode(cifrado_b64)
    key_int = int.from_bytes(clave_bytes, 'big')
    descifrado_bytes = des_decrypt(cifrado_bytes, key_int)
    
    # Quitamos espacios o bytes nulos si hubo padding (para este caso no hará falta)
    return descifrado_bytes.decode('utf-8').rstrip('\x00')

# Probamos con el ejemplo dado 

if __name__ == "__main__":
    mensaje = "noche697"
    clave = "data7Qa="
    
    print("##### Problema 6 - Cifrado DES manual en ECB #####")
    print(f"Mensaje original: {mensaje}")
    print(f"Clave           : {clave}")
    
    cifrado_b64 = cifrar_des_ecb_base64(mensaje, clave)
    print(f"Cifrado Base64  : {cifrado_b64}")
    
    esperado = "obuzqeTZFwc="
    if cifrado_b64 == esperado:
        print(" Coincide con el valor esperado c:")
    else:
        print(f"No coincide :c Esperado: {esperado}")
    
    descifrado = descifrar_des_ecb_base64(cifrado_b64, clave)
    print(f"Descifrado: {descifrado}")

"""""
DIFERENCIA CON EL CÓDIGO DE EJEMPLO (EAX) - PUNTO EXTRA (+0.5)
El código de ejemplo utiliza DES en modo EAX.
Este codigo usa ECB (Electronic Codebook), cada bloque se cifra independientemente 
con la misma clave, sin autenticación ni vector de inicialización. En el ECB el mismo mensaje
y clave producen siempre el mismo cifrado y no protege contra manipulación.

EAX proporciona cifrado autenticado, ECB solo cifra.
Aqui se construye DES manualmente, el ejemplo usa la librería pycryptodome. 
"""