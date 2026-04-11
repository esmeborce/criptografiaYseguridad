"""
Problema 5: Birthday attack aplicado a RSA
Simulación del ataque basado en la paradoja del cumpleaños sobre cifrados RSA.
Se generan mensajes aleatorios, se cifran con RSA y se cuenta la probabilidad
de colisión (dos mensajes diferentes producen el mismo cifrado).
"""

import random
import math
import matplotlib.pyplot as plt


p = 61                     # primer primo
q = 53                     # segundo primo
n = p * q                  # módulo RSA
phi = (p - 1) * (q - 1)    # función  de Euler

e = 17                     # exponente público 
# Calculamos el exponente privado d usando el inverso modular

d = pow(e, -1, phi)

print(f"Parámetros RSA generados:")
print(f"  p = {p}, q = {q}")
print(f"  n = {n}")
print(f"  φ(n) = {phi}")
print(f"  e (público) = {e}")
print(f"  d (privado) = {d}")
print()


def interceptar_cifrado():
    """
    Simula la captura de un mensaje cifrado con RSA.
    Genera un mensaje aleatorio m (1 ≤ m < n) y devuelve su cifrado c = m^e mod n.
    """
    m = random.randint(1, n - 1)   # mensaje aleatorio
    c = pow(m, e, n)               # cifrado RSA: c = m^e mod n
    return c



def prob_colision_empirica(max_k, num_experimentos):
    """
    Estima la probabilidad de que ocurra al menos una colisión (dos cifrados iguales)
    al interceptar k mensajes, para k desde 1 hasta max_k.
    
    Para cada k se repite el experimento 'num_experimentos' veces y se cuenta
    en cuántas de ellas se produce una colisión.
    
    Parámetros:
        max_k (int): número máximo de mensajes interceptados a probar.
        num_experimentos (int): cantidad de repeticiones para cada k.
    
    Retorna:
        list: probabilidades empíricas para cada k = 1..max_k.
    """
    probabilidades = []
    
    for k in range(1, max_k + 1):
        colisiones = 0
        
        for _ in range(num_experimentos):
            # Usamos un conjunto para registrar los cifrados vistos en este experimento
            cifrados_vistos = set()
            hubo_colision = False
            
            for _ in range(k):
                c = interceptar_cifrado()
                if c in cifrados_vistos:
                    # Se encontró una repetición entonces es una colisión detectada
                    hubo_colision = True
                    break
                cifrados_vistos.add(c)
            
            if hubo_colision:
                colisiones += 1
        
        probabilidad = colisiones / num_experimentos
        probabilidades.append(probabilidad)
    
    return probabilidades


def prob_colision_teorica(k, N):
    """
    Calcula la probabilidad teórica aproximada de colisión entre k elementos
    elegidos uniformemente de un conjunto de tamaño N.
    
    Fórmula: P(colisión) ≈ 1 - exp( -k(k-1) / (2N) )
    Válida para N grande y k pequeño comparado con N.
    
    Parámetros:
        k (int): número de elementos elegidos.
        N (int): tamaño del espacio total.
    
    Retorna:
        float: probabilidad teórica de colisión.
    """
    if k <= 1:
        return 0.0
    exponente = -k * (k - 1) / (2 * N)
    return 1 - math.exp(exponente)


# Ejecución de la simulación

MAX_K = 200                # máximo de mensajes interceptados a simular
NUM_EXP = 500              # número de experimentos por cada valor de k

print(f"Ejecutando simulación con {NUM_EXP} experimentos por cada k (hasta k={MAX_K})...")
empiricas = prob_colision_empirica(MAX_K, NUM_EXP)

# Calculamos la curva teórica para comparar
teoricas = [prob_colision_teorica(k, n) for k in range(1, MAX_K + 1)]

# Encontrar el primer k donde la probabilidad empírica alcanza o supera 0.99
k_099 = None
for i, p in enumerate(empiricas):
    if p >= 0.99:
        k_099 = i + 1
        break

if k_099:
    print(f"La probabilidad empírica alcanza 0.99 en k = {k_099} mensajes.")
else:
    print("No se alcanzó una probabilidad de 0.99 en el rango simulado.")

# Cálculo del valor teórico para P=0.99 (usando la fórmula aproximada)
# Despejando 0.99 = 1 - exp(-k(k-1)/(2n)) entonces exp(...) = 0.01 => -k(k-1)/(2n) = ln(0.01)
# k^2 ≈ -2n ln(0.01)
k_099_teorico = math.sqrt(-2 * n * math.log(0.01))
print(f"Valor teórico aproximado para P=0.99: k ≈ {k_099_teorico:.1f} mensajes.")


# Gráfica

plt.figure(figsize=(10, 6))

# Curva empírica (simulación)
plt.plot(range(1, MAX_K + 1), empiricas, 'b-', linewidth=1.5, label='Empírica (simulación)')

# Curva teórica (fórmula aproximada)
plt.plot(range(1, MAX_K + 1), teoricas, 'r--', linewidth=1.5, label='Teórica (aprox.)')

# Líneas de referencia
plt.axhline(y=0.5, color='gray', linestyle=':', label='50% probabilidad')
plt.axhline(y=0.99, color='green', linestyle=':', label='99% probabilidad')

# Marcar el punto de inflexión (donde la probabilidad empírica ≈ 0.99)
if k_099:
    plt.scatter(k_099, empiricas[k_099-1], color='green', s=100, zorder=5,
                label=f'k ≈ {k_099} (P≈0.99)')

# Etiquetas y formato
plt.xlabel('Número de mensajes interceptados (k)')
plt.ylabel('Probabilidad de colisión')
plt.title('Ataque de cumpleaños sobre RSA: Probabilidad de colisión vs. mensajes interceptados')
plt.legend()
plt.grid(True, alpha=0.3)

# Mostrar la gráfica
plt.show()