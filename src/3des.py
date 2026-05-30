from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad
from generacion_llaves import generate_3des_key, generate_iv


BLOCK_SIZE = DES3.block_size


def encrypt_3des_cbc(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    if len(key) not in (16, 24):
        raise ValueError("La clave debe ser de 16 o 24 bytes")
    if len(iv) != BLOCK_SIZE:
        raise ValueError(f"El IV debe ser de {BLOCK_SIZE} bytes")

    padded = pad(plaintext, BLOCK_SIZE)

    cipher = DES3.new(key, DES3.MODE_CBC, iv=iv)

    return cipher.encrypt(padded)


def decrypt_3des_cbc(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    if len(key) not in (16, 24):
        raise ValueError("La clave debe ser de 16 o 24 bytes")
    if len(iv) != BLOCK_SIZE:
        raise ValueError(f"El IV debe ser de {BLOCK_SIZE} bytes")
    if len(ciphertext) == 0 or len(ciphertext) % BLOCK_SIZE != 0:
        raise ValueError("El ciphertext debe ser multiplo del tamano de bloque")

    cipher = DES3.new(key, DES3.MODE_CBC, iv=iv)

    padded_plaintext = cipher.decrypt(ciphertext)

    return unpad(padded_plaintext, BLOCK_SIZE)


def encrypt_3des_cbc_with_iv(plaintext: bytes, key: bytes) -> bytes:
    """Devuelve IV || ciphertext, formato comun para transmitir CBC."""
    iv = generate_iv(BLOCK_SIZE)
    ciphertext = encrypt_3des_cbc(plaintext, key, iv)
    return iv + ciphertext


def decrypt_3des_cbc_with_iv(payload: bytes, key: bytes) -> bytes:
    if len(payload) <= BLOCK_SIZE:
        raise ValueError("El payload debe contener IV + ciphertext")
    iv = payload[:BLOCK_SIZE]
    ciphertext = payload[BLOCK_SIZE:]
    return decrypt_3des_cbc(ciphertext, key, iv)


if __name__ == "__main__":
    key = generate_3des_key(2)
    iv = generate_iv(BLOCK_SIZE)

    mensaje = b"Amo hacer block ciphers con 3DES"

    print("Plaintext: ", mensaje)
    print("Key (hex): ", key.hex())
    print("IV  (hex):  ", iv.hex())

    ciphertext = encrypt_3des_cbc(mensaje, key, iv)
    print("Ciphertext: ", ciphertext.hex())
    print("Longitud ciphertext: ", len(ciphertext), "bytes (multiplo de 8: ", len(ciphertext) % 8 == 0, ")")

    decrypted = decrypt_3des_cbc(ciphertext, key, iv)
    
    if decrypted == mensaje:
        print("Decrypted:  ", decrypted)
    else:
        print("Error en descifrado")

    payload = encrypt_3des_cbc_with_iv(mensaje, key)
    restored = decrypt_3des_cbc_with_iv(payload, key)
    print("Formato IV correcto?:", restored == mensaje)
