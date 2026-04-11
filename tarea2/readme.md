# Tarea 2 - Criptografía y Seguridad

---

##  Problema 6 – Punto extra (+0.5)

**Diferencia entre el código manual DES‑ECB y el ejemplo con `DES.MODE_EAX`:**

El código de ejemplo utiliza DES en modo EAX.
Este codigo usa ECB (Electronic Codebook), cada bloque se cifra independientemente  con la misma clave, sin autenticación ni vector de inicialización. En el ECB el mismo mensaje y clave producen siempre el mismo cifrado y no protege contra manipulación.

EAX proporciona cifrado autenticado, ECB solo cifra.
Aqui se construye DES manualmente, el ejemplo usa la librería pycryptodome. 



---

## Problema 7 

**Pregunta:** ¿Qué pasaría si no se consiguiera la lista de claves? ¿Cuánto tiempo tardaría una computadora básica en un ataque de fuerza bruta completo?

**Respuesta:**

Si no se contara con la lista reducida de claves (`words.txt`), sería necesario realizar un ataque de fuerza bruta sobre el espacio completo de **2⁵⁶** claves posibles de DES.  
Una computadora que pueda probar **10 millones de claves por segundo** tardaría aproximadamente:

> 2⁵⁶ / 10⁷ ≈ 7.2 × 10⁹ segundos ≈ **228 años**.

Este cálculo demuestra por qué es crucial **no utilizar claves débiles o basadas en diccionarios** y por qué DES ya no se considera seguro frente a atacantes con recursos modernos.

---

##  Problema 8 – Bandera obtenida

Luego de ver la vulnerabilidad de **SQL injection** en el login de la aplicación Flask, se accedió la página. Entre los datos se identifico una cadena en Base64 que es 

- `ZmxhZ3tTUUxfSW5qZWN0aW9uX29uc2V2ZXJ9`

El decodificarlo con CyberChet, se obtuvo la cadena:
- **flag{SQL_Injection_onsever}**
