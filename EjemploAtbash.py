alphabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALPHABETO = alphabeto[::-1]


def atbash_cifrar(mensaje: str) -> str:
    resultado = ""

    for char in mensaje:
        if char.isalpha():
            es_minuscula = char.islower()
            indice = ord(char.upper()) - ord('A')
            nuevo_char = ALPHABETO[indice]
            if es_minuscula:
                nuevo_char = nuevo_char.lower()
            resultado += nuevo_char
        else:
            resultado += char

    return resultado

def atbash_descifrar(mensaje: str) -> str:
    return atbash_cifrar(mensaje)

# Ejemplo de uso
if __name__ == "__main__":
    texto_original = "Hola Mundo"
    texto_cifrado = atbash_cifrar(texto_original)
    texto_descifrado = atbash_descifrar(texto_cifrado)

    print("Texto original: ", texto_original)
    print("Texto cifrado: ", texto_cifrado)
    print("Texto descifrado: ", texto_descifrado)