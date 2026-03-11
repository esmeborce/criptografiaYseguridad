
"""
Problema 1
Programa para romper el cifrado César 
Métodos: fuerza bruta, última letra conocida, análisis de frecuencias
"""

# Definimos el alfabeto en orden (a=0, b=1, ..., n=13, ñ=14, o=15, ..., z=26)
ALFABETO = "abcdefghijklmnñopqrstuvwxyz"
# Diccionarios para conversión rápida
letra_a_indice = {letra: i for i, letra in enumerate(ALFABETO)}
indice_a_letra = {i: letra for i, letra in enumerate(ALFABETO)}

def descifrar_cesar(texto_cifrado, desplazamiento):
    """
    Descifra un texto cifrado con César usando un desplazamiento dado.
    Conserva caracteres que no están en el alfabeto (espacios, puntuación)
    """
    texto_plano = []
    for caracter in texto_cifrado.lower():
        if caracter in letra_a_indice:
            indice_original = letra_a_indice[caracter]
            indice_descifrado = (indice_original - desplazamiento) % 27
            texto_plano.append(indice_a_letra[indice_descifrado])
        else:
            texto_plano.append(caracter)  # espacios, etc.
    return ''.join(texto_plano)

def fuerza_bruta(texto_cifrado):
    """Prueba todos los desplazamientos posibles del 0 al 26."""
    print(" Fuerza bruta ")
    for despl in range(27):
        print(f"Desplazamiento {despl:2d}: {descifrar_cesar(texto_cifrado, despl)}")
    print()

def ultima_letra_conocida(texto_cifrado, letra_objetivo='o'):
    """
    Deducir el desplazamiento suponiendo que la última letra del texto cifrado
    (ignorando espacios) se descifra como la letra_objetivo
    """
    # Extraer solo letras del texto cifrado
    letras = [c for c in texto_cifrado.lower() if c in letra_a_indice]
    if not letras:
        print("No hay letras en el texto.")
        return
    ultima = letras[-1]
    indice_cifrado = letra_a_indice[ultima]
    indice_objetivo = letra_a_indice[letra_objetivo]
    despl = (indice_cifrado - indice_objetivo) % 27
    print(" Última letra conocida ")
    print(f"Última letra del cifrado: '{ultima}' y se descifra como '{letra_objetivo}'")
    print(f"Desplazamiento calculado: {despl}")
    print(f"Texto descifrado: {descifrar_cesar(texto_cifrado, despl)}\n")

def analisis_frecuencias(texto_cifrado):
    """
    Encuentra la letra más frecuente en el cifrado y asume que corresponde a la 'e. Calcula el desplazamiento y descifra.
    """
    from collections import Counter
    letras = [c for c in texto_cifrado.lower() if c in letra_a_indice]
    if not letras:
        print("No hay letras en el texto.")
        return
    frecuencia = Counter(letras)
    letra_comun = frecuencia.most_common(1)[0][0]
    print("Análisis de frecuencias")
    print(f"Letra más frecuente en el cifrado: '{letra_comun}' (aparece {frecuencia[letra_comun]} veces)")
    indice_cifrado = letra_a_indice[letra_comun]
    indice_e = letra_a_indice['e']
    despl = (indice_cifrado - indice_e) % 27
    print(f"Desplazamiento calculado (suponiendo que '{letra_comun}' = 'e'): {despl}")
    print(f"Texto descifrado: {descifrar_cesar(texto_cifrado, despl)}\n")

def main():
    # Frases cifradas proporcionadas en el problema
    cifrado1 = "Nc xkfc gu dgnnc"
    cifrado2 = "Zo qgweidugotio sh jb hsqgsid"   # se quitó el acento de "otío" para evitar problemas
    cifrado3 = "Jx qzd kfhnp mjwnw f ptx ijqfx xnr ifwxj hzjryf xtgwj ytit hzfrit jwix ñtajr"

    print(" PROBLEMA 1: ROMPER CIFRADO CÉSAR \n")

    # Aplicar cada método a su frase correspondiente
    fuerza_bruta(cifrado1)
    ultima_letra_conocida(cifrado2, 'o')
    analisis_frecuencias(cifrado3)

if __name__ == "__main__":
    main()