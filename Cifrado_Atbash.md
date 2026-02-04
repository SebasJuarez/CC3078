# Cifrado Atbash

## 1. Historia del Atbash

El Cifrado Atbash es uno de los mas antiguos en la criptografía. Su origen viene de los hebreos antiguos en donde se queria ocultar ciertas palabras en textos de la religion, especialmente en el antiguo testamento.

El nombre viene de Aleph (siendo la letra A), Tav (siendo la letra Z), Bet (siendo la letra B) y Shin (siendo la letra Y). Todo esto junto es el principio de sustituir la primera letra del alfabeto por la ultima y la segunda por la penultima y asi sucesivamente.

El cifrado es uno de sustitucion simple, ya que cada letra sel texto se remplaza siempre por la misma letra.

---

## 2. Funcionamiento de Atbash

Este cifrado, como se mencionaba anteriormente, funciona al cambiar la primera letra del abecedario por la última, la segunda por la penúltima, y así sucesivamente.

| Letra original | Letra cifrada |
|--------------|---------------|
| A | Z |
| B | Y |
| C | X |
| ... | ... |
| X | C |
| Y | B |
| Z | A |

Ya que este cifrado es uno simple de sustitución, se aplica el mismo metodo para descifrar el mensaje.

---

## 3. Ejemplo de aplicación (usando el alfabeto inglés)

### Texto original:
```
HOLA
```

### Aplicando Atbash:
- H → S  
- O → L  
- L → O  
- A → Z  

### Texto cifrado:
```
SLOZ
```

Si aplicamos nuevamente el cifrado Atbash sobre SLOZ, obtenemos el mensaje original HOLA.

---

## 4. ¿Por qué el Atbash?

Primeramente, me interesaba ya que no era uno de los que hemos trabajado en los ejercicios pero siento que es importante de revisar ya que es la base de muchos cifrados de sustitución. Comparandolo con otros clasicos, este es el más simple y directo, lo que lo hace ideal para entender los conceptos básicos de la criptografía.

Ademas, nos enseña mucho de la historia interesante, como los hebreos antiguos usaban este cifrado para ocultar mensajes en textos religiosos.

---

## 5. Ventajas del cifrado Atbash

- **Simplicidad**: No requiere claves ni configuraciones adicionales.
- **Facilidad de implementación**: Puede implementarse fácilmente usando lógica básica y el alfabeto.
- **Simetría**: Por lo mismo que es simple, se usa el mismo orden para cifrar y descifrar.

---

## 6. Vulnerabilidades y limitaciones

Aunque se sabe que este cifrado es importante por la historia, tambien es de conocimiento general que es completamente inseguro para cualquier uso serio. Algunas de sus vulnerabilidades son:

- **Simetría**: El mapeo es fijo y conocido.
- **Vulnerable al análisis de frecuencia**: Las frecuencias de las letras se conservan.
- **Sin clave secreta**: Cualquiera que conozca el método puede descifrar el mensaje.
