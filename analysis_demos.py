from Crypto.Cipher import AES, DES
from Crypto.Util.Padding import pad
from generacion_llaves import generate_des_key, generate_aes_key, generate_iv
from manual_padding import pkcs7_pad, pkcs7_unpad


def split_blocks(data: bytes, block_size: int) -> list[str]:
    return [data[i : i + block_size].hex() for i in range(0, len(data), block_size)]


def demo_ecb_vs_cbc_repeated_blocks():
    key = generate_des_key()
    message = b"ATAQUE!!" * 4  # 4 bloques identicos de 8 bytes
    padded = pkcs7_pad(message, DES.block_size)

    ecb = DES.new(key, DES.MODE_ECB)
    cbc = DES.new(key, DES.MODE_CBC, iv=generate_iv(DES.block_size))

    ecb_ct = ecb.encrypt(padded)
    cbc_ct = cbc.encrypt(padded)

    print("Mensaje:", message)
    print("Bloques ECB:")
    ecb_blocks = split_blocks(ecb_ct, DES.block_size)
    for block in ecb_blocks:
        print(" ", block)
    print("Bloques repetidos en ECB:", len(set(ecb_blocks)) < len(ecb_blocks))
    print("Bloques CBC:")
    cbc_blocks = split_blocks(cbc_ct, DES.block_size)
    for block in cbc_blocks:
        print(" ", block)
    print("Bloques repetidos en CBC:", len(set(cbc_blocks)) < len(cbc_blocks))


def demo_iv_reuse():
    key = generate_aes_key(256)
    msg = b"Mismo mensaje cifrado dos veces con CBC"
    iv = generate_iv(AES.block_size)

    ct_same_1 = AES.new(key, AES.MODE_CBC, iv=iv).encrypt(pad(msg, AES.block_size))
    ct_same_2 = AES.new(key, AES.MODE_CBC, iv=iv).encrypt(pad(msg, AES.block_size))

    iv_a = generate_iv(AES.block_size)
    iv_b = generate_iv(AES.block_size)
    ct_diff_1 = AES.new(key, AES.MODE_CBC, iv=iv_a).encrypt(pad(msg, AES.block_size))
    ct_diff_2 = AES.new(key, AES.MODE_CBC, iv=iv_b).encrypt(pad(msg, AES.block_size))

    print("Mismo IV -> iguales:", ct_same_1 == ct_same_2)
    print("IV diferentes -> diferentes:", ct_diff_1 != ct_diff_2)


def demo_padding():
    samples = [b"ABCDE", b"12345678", b"1234567890"]
    for s in samples:
        padded = pkcs7_pad(s, 8)
        recovered = pkcs7_unpad(padded)
        print(f"Mensaje ({len(s)} bytes): {s}")
        print("  Padded (hex):", padded.hex())
        print("  Unpad correcto:", recovered == s)


if __name__ == "__main__":
    print("== ECB vs CBC con bloques repetidos ==")
    demo_ecb_vs_cbc_repeated_blocks()
    print("\n== Experimento IV en CBC ==")
    demo_iv_reuse()
    print("\n== Padding PKCS#7 ==")
    demo_padding()
