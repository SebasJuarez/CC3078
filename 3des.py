from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad
from generacion_llaves import generate_3des_key, generate_iv


def encrypt_3des_cbc(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    if len(key) not in (16, 24):
        raise ValueError("La clave debe ser de 16 o 24 bytes")
    if len(iv) != 8:
        raise ValueError("El IV debe ser de 8 bytes")

    padded = pad(plaintext, DES3.block_size)

    cipher = DES3.new(key, DES3.MODE_CBC, iv=iv)

    return cipher.encrypt(padded)


def decrypt_3des_cbc(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    if len(key) not in (16, 24):
        raise ValueError("La clave debe ser de 16 o 24 bytes")
    if len(iv) != 8:
        raise ValueError("El IV debe ser de 8 bytes")

    cipher = DES3.new(key, DES3.MODE_CBC, iv=iv)

    padded_plaintext = cipher.decrypt(ciphertext)

    return unpad(padded_plaintext, DES3.block_size)


if __name__ == "__main__":
    key = generate_3des_key(2)
    iv = generate_iv(8)

    mensaje = b"Mensaje secreto para 3DES"

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