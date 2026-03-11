"""
PROBLEMA 2
"""

# Construimos el cuadrado de Polibio

# Lista con las 25 letras en orden
letras = [
    'A', 'B', 'C', 'D', 'E',
    'F', 'G', 'H', 'I', 'J',
    'K', 'L', 'M', 'N', 'O',
    'P', 'Q', 'R', 'S', 'T',
    'U', 'V', 'W', 'X', 'Y'
]

# Crear matriz 5x5 
cuadrado = []
fila = []
for i in range(25):
    fila.append(letras[i])
    if (i + 1) % 5 == 0:  # cada 5 letras, guardamos la fila
        cuadrado.append(fila)
        fila = []

# Mostrar el cuadrado 
print("Cuadrado de Polibio:")
print("   1 2 3 4 5")
for i in range(5):
    print(f"{i+1}  {' '.join(cuadrado[i])}")
print()


# Funciones para cifrar y descifrar


def cifrar(texto):
    """
    Recibe un texto (solo letras mayúsculas, sin espacios) y devuelve
    una cadena con los pares de números separados por espacios.
    """
    resultado = []
    for letra in texto:
        # Buscar la letra en la matriz
        for i in range(5):
            for j in range(5):
                if cuadrado[i][j] == letra:
                    # Guardamos fila y columna (sumamos 1 porque empiezan en 1)
                    resultado.append(str(i+1) + str(j+1))
                    break
    return ' '.join(resultado)

def descifrar(codigo):
    """
    Recibe una cadena con números de dos dígitos separados por espacios
    y devuelve el texto descifrado.
    """
    # Separar los números 
    pares = codigo.split()
    resultado = []
    for par in pares:
        # El primer dígito es la fila, el segundo la columna
        fila = int(par[0]) - 1   # restamos 1 para índice de matriz
        col = int(par[1]) - 1
        resultado.append(cuadrado[fila][col])
    return ''.join(resultado)

def limpiar_texto(texto):
    """
    Convierte el texto a mayúsculas, elimina acentos y espacios,
    y filtra solo las letras válidas (A-Y excepto Ñ, Z).
    """
    # Mapa de acentos (solo mayúsculas)
    acentos = {
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'À': 'A', 'È': 'E', 'Ì': 'I', 'Ò': 'O', 'Ù': 'U',
        'Ä': 'A', 'Ë': 'E', 'Ï': 'I', 'Ö': 'O', 'Ü': 'U'
    }
    
    texto_limpio = []
    for caracter in texto.upper():
        # Si tiene acento, lo reemplazamos
        if caracter in acentos:
            caracter = acentos[caracter]
        # Solo nos quedamos con letras de la A a la Y (sin Ñ ni Z)
        if 'A' <= caracter <= 'Y' and caracter not in 'ÑZ':
            texto_limpio.append(caracter)
    return ''.join(texto_limpio)


# Programa principal

print("PARTE 1: Descifrar el mensaje")
codigo1 = "15 32 45 24 15 33 41 35 34 35 15 44 41 15 43 11 11 34 11 14 24 15"
mensaje1 = descifrar(codigo1)
print("Código:", codigo1)
print("Mensaje descifrado:", mensaje1)
print()

print("PARTE 2: Cifrar la frase")
frase_original = (
    "Si la felicidad tuviera una forma, tendría forma de cristal, "
    "porque puede estar a tu alrededor sin que la notes. "
    "Pero si cambias de perspectiva, puede reflejar una luz capaz "
    "de iluminarlo todo."
)
print("Frase original:")
print(frase_original)

# Limpiar el texto
texto_limpio = limpiar_texto(frase_original)
print("\nTexto limpio (solo letras A-Y):")
print(texto_limpio)

# Cifrar
cifrado = cifrar(texto_limpio)
print("\nMensaje cifrado (números):")
print(cifrado)

# Mostrar sin espacios
print("\nFormato compacto (sin espacios):")
print(cifrado.replace(' ', ''))

# Verificacion, desciframos lo cifrado 
print("\n Verificación ")
verificacion = descifrar(cifrado)
print("Descifrando de nuevo:", verificacion)
if verificacion == texto_limpio:
    print(" Todo bien c:")
else:
    print(" Error")