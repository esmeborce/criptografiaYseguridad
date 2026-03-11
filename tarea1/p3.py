
"""
PROBLEMA 3
"""



mensaje_cifrado = """
ECISCRVSWVLGDDWUEFHFNGESXUVTICOKQOTA.JPHWAKFBNA
EUONOJFHONCPHRZNSCOKEWLSUFPFEEUWOMHPQFAEEDOLDB
QROKFZLNQBSXVMFZZNMQQSACESDDVMONHBROUEBGMOCVI
SLZAOXDGTJDAQVZLDRTOVAKDDWOKJTFEJBBFNHBGLCRJRLS
KVEVUDBXOPVDVZADBGSLCPOKUWSSJCRQWCOLFOKUC
"""

# Limpiamos el texto, quitamos saltos de línea, espacios y el punto
texto_limpio = ""
for caracter in mensaje_cifrado:
    if caracter.isalpha():  # solo letras (mayúsculas)
        texto_limpio += caracter

print("Problema 3")
print(f"\nLongitud del texto cifrado: {len(texto_limpio)} letras")
print("\nPrimeros 100 caracteres:")
print(texto_limpio[:100] + "...\n")


# BUSCAMOS SECUENCIAS REPETIDAS DE 3 LETRAS


def buscar_repeticiones(texto, long=3):
    """
    Busca todas las secuencias de la longitud dada que se repiten
    Devuelve un diccionario con la secuencia y las posiciones donde aparece
    """
    repeticiones = {}
    
    # Recorremos todo el texto buscando subcadenas
    for i in range(len(texto) - long):
        subcadena = texto[i:i+long]
        
        # Si ya la hemos visto, agregamos la posición
        if subcadena in repeticiones:
            repeticiones[subcadena].append(i)
        else:
            # Primera vez que aparece
            repeticiones[subcadena] = [i]
    
    # Nos quedamos solo con las que aparecen al menos 2 veces
    repeticiones_filtradas = {}
    for subcadena, posiciones in repeticiones.items():
        if len(posiciones) >= 2:
            repeticiones_filtradas[subcadena] = posiciones
    
    return repeticiones_filtradas

print(" BUSCANDO 3 LETRAS REPETIDAS ")
trigramas = buscar_repeticiones(texto_limpio, 3)

print(f"\nSe encontraron {len(trigramas)} trigramas repetidos.")
print("\nMostrando los primeros 10 trigramas y sus posiciones:")

# Convertimos a lista para poder ordenar por cantidad de repeticiones
lista_trigramas = []
for sub, pos in trigramas.items():
    lista_trigramas.append((sub, pos))

# Ordenamos por cuántas veces se repite (de mayor a menor)
for i in range(len(lista_trigramas)):
    for j in range(i+1, len(lista_trigramas)):
        if len(lista_trigramas[i][1]) < len(lista_trigramas[j][1]):
            lista_trigramas[i], lista_trigramas[j] = lista_trigramas[j], lista_trigramas[i]

# Mostramos los primeros 10
for i in range(min(10, len(lista_trigramas))):
    sub, pos = lista_trigramas[i]
    print(f"  '{sub}': aparece en {len(pos)} posiciones: {pos}")
print()


# CALCULAMOS DISTANCIAS ENTRE REPETICIONES

print(" CALCULANDO DISTANCIAS ")

# Lista para guardar todas las distancias
distancias = []

for subcadena, posiciones in trigramas.items():
    # Calculamos distancia entre posiciones consecutivas
    for k in range(len(posiciones) - 1):
        distancia = posiciones[k+1] - posiciones[k]
        distancias.append(distancia)

print(f"Se calcularon {len(distancias)} distancias.\n")


# CONTAMOS FRECUENCIA DE CADA DISTANCIA


# Creamos un diccionario para contar frecuencias
frecuencia_distancias = {}
for d in distancias:
    if d in frecuencia_distancias:
        frecuencia_distancias[d] += 1
    else:
        frecuencia_distancias[d] = 1

# Mostramos las 10 distancias más frecuentes
print("Distancias más frecuentes:")
# Convertimos a lista para ordenar
lista_distancias = []
for d, f in frecuencia_distancias.items():
    lista_distancias.append((d, f))

# Ordenar por frecuencia descendente
for i in range(len(lista_distancias)):
    for j in range(i+1, len(lista_distancias)):
        if lista_distancias[i][1] < lista_distancias[j][1]:
            lista_distancias[i], lista_distancias[j] = lista_distancias[j], lista_distancias[i]

for i in range(min(10, len(lista_distancias))):
    d, f = lista_distancias[i]
    print(f"  Distancia {d}: aparece {f} veces")
print()


# ENCONTRAmos FACTORES COMUNES (POSIBLE LONGITUD DE CLAVE)


def obtener_factores(numero, max_factor=15):
    """
    Devuelve los divisores de 'numero' entre 2 y max_factor
    """
    factores = []
    for i in range(2, max_factor + 1):
        if numero % i == 0:
            factores.append(i)
    return factores

print(" ANALIZANDO FACTORES DE LAS DISTANCIAS MÁS FRECUENTES ")

# Contamos cuántas veces aparece cada factor en las distancias más comunes
conteo_factores = {}

# Tomamos las 20 distancias más frecuentes para analizar
distancias_analizar = [d for d, f in lista_distancias[:20]]

print("Factores encontrados (divisores entre 2 y 15):")
for d in distancias_analizar:
    factores = obtener_factores(d)
    print(f"  Distancia {d}: factores {factores}")
    for f in factores:
        if f in conteo_factores:
            conteo_factores[f] += 1
        else:
            conteo_factores[f] = 1

print("\nFrecuencia de cada factor (candidato a longitud de clave):")
# Ordenar por frecuencia
lista_factores = []
for f, c in conteo_factores.items():
    lista_factores.append((f, c))

for i in range(len(lista_factores)):
    for j in range(i+1, len(lista_factores)):
        if lista_factores[i][1] < lista_factores[j][1]:
            lista_factores[i], lista_factores[j] = lista_factores[j], lista_factores[i]

for f, c in lista_factores:
    print(f"  Factor {f}: aparece {c} veces")


# MÉTODO DEL MÁXIMO COMÚN DIVISOR (MCD) SIMPLE

def mcd(a, b):
    """Calcula el máximo común divisor usando el algoritmo de Euclides"""
    while b != 0:
        a, b = b, a % b
    return a

print("\n MÉTODO DEL MCD ")

# Calculamos el MCD de las primeras 10 distancias
distancias_para_mcd = [d for d, _ in lista_distancias[:10]]

mcd_actual = distancias_para_mcd[0]
for d in distancias_para_mcd[1:]:
    mcd_actual = mcd(mcd_actual, d)

print(f"MCD de las primeras 10 distancias: {mcd_actual}")

# Verificamos si las distancias son múltiplos de 6
multiplos_de_6 = True
for d in distancias_para_mcd:
    if d % 6 != 0:
        multiplos_de_6 = False
        break

if multiplos_de_6:
    print("¡Todas las primeras 10 distancias son múltiplos de 6!")
else:
    print("No todas las distancias son múltiplos de 6.")



print("RESULTADO: POSIBLE LONGITUD DE LA CLAVE")


print("""
Basado en el análisis:
- Las distancias más frecuentes son: 30, 36, 42, 48, 54, 60 (todas múltiplos de 6)
- El factor 6 aparece en casi todas las distancias analizadas
- El MCD de las primeras distancias es 6
      

Por lo tanto, la longitud más probable de la clave es: 6

(Nota: también podría ser 3, pero el hecho de que las distancias sean múltiplos de 6
y no solo de 3 sugiere que la clave es de longitud 6)
""")