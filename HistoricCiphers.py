def desplazar_caracter(char, desplazamiento):
    if 'a' <= char <= 'z':
        base = ord('a')
        return chr((ord(char) - base + desplazamiento) % 26 + base)
    elif 'A' <= char <= 'Z':
        base = ord('A')
        return chr((ord(char) - base + desplazamiento) % 26 + base)
    else:
        return char
    
def cesar_cifrar(mensaje, desplazamiento):
    resultado = ""
    for char in mensaje:
        resultado += desplazar_caracter(char, desplazamiento)
    return resultado

def cesar_descifrar(mensaje, desplazamiento):
    return cesar_cifrar(mensaje, -desplazamiento)

def rot13(mensaje):
    resultado = ""
    for char in mensaje:
        resultado += desplazar_caracter(char, 13)
    return resultado

def vigenere_cifrar(mensaje, clave):
    resultado = ""
    j = 0  

    for char in mensaje:
        if char.isalpha():
            k = clave[j % len(clave)].lower()
            desplazamiento = ord(k) - ord('a')

            if 'a' <= char <= 'z':
                base = ord('a')
            else:
                base = ord('A')

            nuevo = (ord(char) - base + desplazamiento) % 26 + base
            resultado += chr(nuevo)
            j += 1
        else:
            resultado += char
    return resultado

def vigenere_descifrar(mensaje, clave):
    resultado = ""
    j = 0

    for char in mensaje:
        if char.isalpha():
            k = clave[j % len(clave)].lower()
            desplazamiento = ord(k) - ord('a')

            if 'a' <= char <= 'z':
                base = ord('a')
            else:
                base = ord('A')

            nuevo = (ord(char) - base - desplazamiento) % 26 + base
            resultado += chr(nuevo)
            j += 1
        else:
            resultado += char

    return resultado

def analisis_frecuencia(mensaje):
    frecuencias = {}

    for char in mensaje:
        if char in frecuencias:
            frecuencias[char] += 1
        else:
            frecuencias[char] = 1
    return frecuencias

def mostrar_tabla_frecuencias(frecuencias):
    for c in sorted(frecuencias, key=frecuencias.get, reverse=True):
        print("'" + c + "': " + str(frecuencias[c]))

while True:
    print("Crifrados Históricos\n")
    input_text = input("Ingrese el texto a cifrar/descifrar (o salir para terminar): ")
    if input_text.lower() == "salir":
        print("Saliendo...")
        break
    print("Menú:")
    print("1. Cifrado César y ROT13")
    print("2. Cifrado Vigenère")
    print("3. Salir")
    option = input("Seleccione una opción: ")

    if option == '1':
        desplazamiento = int(input("Ingrese el desplazamiento para César: "))
        cifrado = cesar_cifrar(input_text, desplazamiento)
        print("Cifrado César: " + cifrado)
        print("Descifrado César: " + cesar_descifrar(cifrado, desplazamiento))
        print("ROT13: " + rot13(input_text))
    elif option == '2':
        clave = input("Ingrese la clave para Vigenère: ")
        cifrado = vigenere_cifrar(input_text, clave)
        print("Cifrado Vigenère: " + cifrado)
        print("Descifrado Vigenère: " + vigenere_descifrar(cifrado, clave))
    elif option == '3':
        print("Saliendo...")
        break
    else:
        print("Opción no válida. Intente de nuevo.")
