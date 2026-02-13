def normalizar(seed: int | str) -> int:
    if isinstance(seed, int):
        return seed & 0xFFFFFFFF
    if isinstance(seed, str):
        seed = seed.encode("utf-8")
        return int.from_bytes(seed, byteorder="big", signed=False) & 0xFFFFFFFF


def generar_keystream(seed: int | str, longitud: int) -> bytes:

    a = 1664525
    c = 1013904223
    m = 2**32

    estado = normalizar(seed)
    salida = bytearray()

    while len(salida) < longitud:
        estado = (a * estado + c) % m
        salida.append(estado & 0xFF)

    return bytes(salida)


if __name__ == "__main__":
    mensaje = "Hola mundo"
    keystream = generar_keystream(seed="clave", longitud=len(mensaje.encode("utf-8")))
print(keystream)
