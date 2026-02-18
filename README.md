# CC3078
Ejercicios y laboratorios hechos en Cifrado de Información.

## Parte 2: Análisis de Seguridad

### 2.1 Variación de la Clave

Cuando cambia la clave, cambia el estado inicial del generador y por lo tanto cambia todo el keystream. Con los siguientes ejemplos podemos ver como el mismo mensaje produce un texto cifrado totalmente distinto.

Ejemplo con el mismo mensaje ("Hola mundo"):
- Clave "clave" -> b'\xc8\xb0\xde\x08\x94\xees\xc3L\x08'
- Clave "clavf" -> b'\xc5\xe7+\x9b1Q\x1e\xa0\xb1_'
- Clave "otra" -> b'\x04T2D`\xf2\x07G\x10,'

### 2.2 Reutilización del Keystream

Si se puede reutilizar la clave, pero esto hace que el atacante, conociendo como funcionan los cifrados, pueden ver los textos en hexagecimal y darse cuenta que resultan similares. Un ejemplo puede ser:

- P1 = "ATAQUE AL AMANECER"
- P2 = "DEFENSA AL MEDIODIA"
- Misma clave: "misma-clave"

Si se hace el cifrado, se obtiene:
- C1 XOR C2 = b'\x05\x11\x07\x14\x1b\x16aa\rla\x00\x04\n\x0c\x0c\x01\x1b'
- P1 XOR P2 = b'\x05\x11\x07\x14\x1b\x16aa\rla\x00\x04\n\x0c\x0c\x01\x1b'

Y como se puede ver, son iguales.

### 2.3 Longitud del Keystream

Normalmente, el keystream debe tener una longutud del mismo tamaño de bytes que el mensaje.

Tener un keystream mas corto que el mensaje puede hacer que parte del mensaje se quede sin cifrar. Se puede repetir el keystram pero ya se introducen patrones y esto es una vulnerabilidad.

Si es del mismo tamaño, cada byte del mensaje se va mezclando con un byte distino, haciendo que verdaderamente se oculte la información.

Si el keystream es mas largo que el mensaje no va a faltar informacion como si fuera mas corto, pero hay mas bytes que no se estan usando. No se esta dando mas seguridad y solo esta aumentando el costo.

Por esto, aunque no es obligatorio, es recomendable que el keystream tenga la misma longitud que el mensaje para evitar vulnerabilidades y no desperdiciar recursos.

### 2.4 Consideraciones Prácticas

En una produccion real, al ir generando un keystream tenemos algunos puntos criticos a tener en cuenta:

1. Usar un generador de keystream seguro. En muchos lugares se recomienda ChaCha20 ya que esta probado en estos ambitos.

2. Se debe tratar de mannejar las claves de manera segura. No tenemos que ponerla como texto fijo.

3. Hay que tener cuidado con la validacion y la codificacion de los datos. Es importante elegir el tipo de entrada/salida para evitar perdida de información.

## Parte 3: Validación y Pruebas

Algunos de los ejemplos que se probaron son estos:

- Mensaje: "Hola mundo", Clave: "clave" -> Cifrado: b'\xc8\xb0\xde\x08\x94\xees\xc3L\x08'
- Mensaje: "Pruebas", Clave: "otra-clave" -> Cifrado: b'\xd0\xad\xc7\x0c\xd6\xe2u'
- Mensaje: "CC3078", Clave: "cifrados" -> Cifrado: b'u^\xebg\xfd\x99'

