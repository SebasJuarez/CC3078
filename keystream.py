def normalizar(seed):
    if isinstance(seed, int):
        return seed & 0xFFFFFFFF
    if isinstance(seed, str):
        valor = 0
        i = 0
        while i < len(seed):
            valor = ((valor << 8) + ord(seed[i])) & 0xFFFFFFFF
            i += 1
        return valor
    raise TypeError("seed debe ser int o str")


def generar_keystream(seed, longitud):

    a = 1664525
    c = 1013904223
    m = 2**32

    estado = normalizar(seed)
    salida = bytearray()

    while len(salida) < longitud:
        estado = (a * estado + c) % m
        salida.append(estado & 0xFF)

    return bytes(salida)


def texto_a_bytes(texto):
    salida = bytearray()
    i = 0
    while i < len(texto):
        codigo = ord(texto[i])
        if codigo > 255:
            raise ValueError("Solo se soportan caracteres con codigo <= 255")
        salida.append(codigo)
        i += 1
    return bytes(salida)


def bytes_a_texto(datos):
    caracteres = []
    i = 0
    while i < len(datos):
        caracteres.append(chr(datos[i]))
        i += 1
    return "".join(caracteres)


def cifrar(mensaje, clave):
    mensaje_bytes = texto_a_bytes(mensaje)
    keystream = generar_keystream(seed=clave, longitud=len(mensaje_bytes))
    salida = bytearray()
    i = 0
    while i < len(mensaje_bytes):
        salida.append(mensaje_bytes[i] ^ keystream[i])
        i += 1
    return bytes(salida)


def descifrar(texto_cifrado, clave):
    keystream = generar_keystream(seed=clave, longitud=len(texto_cifrado))
    salida = bytearray()
    i = 0
    while i < len(texto_cifrado):
        salida.append(texto_cifrado[i] ^ keystream[i])
        i += 1
    return bytes_a_texto(bytes(salida))


if __name__ == "__main__":
    mensaje = ["Hola mundo", "Pruebas", "CC3078"]
    clave = ["clave", "otra-clave", "cifrados"]

    for key in clave:
        keystream = generar_keystream(seed=key, longitud=len(texto_a_bytes(mensaje[clave.index(key)])))
        print("Keystream:", keystream)

        texto_cifrado = cifrar(mensaje[clave.index(key)], key)
        print("Cifrado (bytes):", texto_cifrado)

        texto_descifrado = descifrar(texto_cifrado, key)
        print("Descifrado:", texto_descifrado)