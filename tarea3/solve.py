import re
import hashlib
import unicodedata
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def es_primo(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

def obtener_primos(cantidad):
    primos = []
    n = 2
    while len(primos) < cantidad:
        if es_primo(n):
            primos.append(n)
        n += 1
    return primos

def resolver():
    print(" Iniciando proceso de extracción ")
    
    # Leer y limpiar el texto
    with open('file.txt', 'r', encoding='utf-8') as f:
        raw_text = f.read()
    
    # quitar acentos, filtrar solo letras y convertir a MINÚSCULAS
    text_norm = unicodedata.normalize('NFKD', raw_text).encode('ASCII', 'ignore').decode('utf-8')
    clean_text = re.sub(r'[^a-zA-Z]', '', text_norm).lower()
    length = len(clean_text)
    
    # generar índices primos y extraer caracteres de forma cíclica
    primos = obtener_primos(25)
    extracted = []
    for p in primos:
        idx = (p - 2) % length
        extracted.append(clean_text[idx])
        
    # Construir la clave de 50 caracteres intercalando la palabra base
    base_word = "kevinmitnick"
    key = ""
    for i in range(25):
        key += extracted[i]
        key += base_word[i % len(base_word)]
        
    print(f"Clave construida: {key}")
    
    # Calcular y verificar el Hash SHA-256
    key_hash = hashlib.sha256(key.encode()).hexdigest()
    print(f"Hash de la clave: {key_hash}")
    
    with open('hashes.txt', 'r') as f:
        hashes = [line.strip() for line in f if line.strip()]
        
    if key_hash in hashes:
        print("Hash verificado! La clave coincide con un hash de hashes.txt.")
    else:
        print("[-] El hash no coincide. Verifica el archivo file.txt.")
        return
    # Descifrado AES-GCM
    key_bytes = hashlib.sha256(key_hash.encode()).digest()
    aesgcm = AESGCM(key_bytes)
    
    print("\n[*] Descifrando cipher.txt...")
    print("="*50)
    
    with open('cipher.txt', 'r') as f:
        # Leemos todo el archivo y eliminamos saltos de línea
        cipher_hex = f.read().replace('\n', '').replace('\r', '').replace(' ', '').strip()
        
    try:
        data = bytes.fromhex(cipher_hex)
        nonce = data[:12] # Los primeros 12 bytes son el nonce
        ciphertext = data[12:]
        dec = aesgcm.decrypt(nonce, ciphertext, None).decode('utf-8')
        print(dec)
    except Exception as e:
        # Si ocurre un error, forzamos a imprimir el tipo de excepción para no ver un mensaje vacío
        print(f" Error en el descifrado (posible InvalidTag). Detalle: {repr(e)}")
        
    print("="*50)

if __name__ == '__main__':
    resolver()
