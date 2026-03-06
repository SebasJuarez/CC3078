from Crypto.Cipher import DES
from generacion_llaves import generate_des_key
from manual_padding import pkcs7_pad, pkcs7_unpad


BLOCK_SIZE = DES.block_size


def encrypt_des_ecb(plaintext: bytes, key: bytes) -> bytes:
    if len(key) != 8:
        raise ValueError("La clave DES debe ser de 8 bytes")
    padded = pkcs7_pad(plaintext, BLOCK_SIZE)
    cipher = DES.new(key, DES.MODE_ECB)
    return cipher.encrypt(padded)


def decrypt_des_ecb(ciphertext: bytes, key: bytes) -> bytes:
    if len(key) != 8:
        raise ValueError("La clave DES debe ser de 8 bytes")
    if len(ciphertext) == 0 or len(ciphertext) % BLOCK_SIZE != 0:
        raise ValueError("El ciphertext debe ser multiplo de 8 bytes")
    cipher = DES.new(key, DES.MODE_ECB)
    padded = cipher.decrypt(ciphertext)
    return pkcs7_unpad(padded)


if __name__ == "__main__":
    key = generate_des_key()
    message = b"Amo hacer block ciphers"

    ct = encrypt_des_ecb(message, key)
    pt = decrypt_des_ecb(ct, key)

    print("Plaintext: ", message)
    print("Key (hex): ", key.hex())
    print("Ciphertext: ", ct.hex())
    print(
        "Longitud ciphertext: ",
        len(ct),
        "bytes (multiplo de 8: ",
        len(ct) % BLOCK_SIZE == 0,
        ")",
    )

    if pt == message:
        print("Decrypted:  ", pt)
    else:
        print("Error en descifrado")
