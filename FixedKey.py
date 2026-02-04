PRINTABLE_START = 32
PRINTABLE_END = 126
ALPHABET_SIZE = (PRINTABLE_END - PRINTABLE_START) + 1  # 95 valores
MODULUS = 2**31
FIXED_KEY_LEN = 16


def validate_printable_ascii(s: str, label: str) -> None:
    for idx, ch in enumerate(s):
        code = ord(ch)
        if code < PRINTABLE_START or code > PRINTABLE_END:
            raise ValueError(
                label + " contiene un caracter no-ASCII-imprimible en índice " + str(idx) + ": U+" + format(code, "04X")
            )


def shift(ch: str) -> int:
    return ord(ch) - PRINTABLE_START


def unshift(v: int) -> str:
    return chr(PRINTABLE_START + (v % ALPHABET_SIZE))


def lcg_next(state: int) -> int:
    return (1103515245 * state + 12345) % MODULUS


def seed_from_text(text: str) -> int:
    seed = 0
    for ch in text:
        seed = (seed * 131 + ord(ch)) % MODULUS
    seed &= 0x7FFFFFFF
    return seed or 1


def generate_fixed_key(length: int, seed: int) -> str:
    state = seed % MODULUS
    if state == 0:
        state = 1

    chars = []
    for _ in range(length):
        state = lcg_next(state)
        chars.append(unshift(state % ALPHABET_SIZE))
    return "".join(chars)


def encrypt(plaintext: str, key: str) -> str:
    validate_printable_ascii(plaintext, "texto")
    validate_printable_ascii(key, "key")
    if len(key) != FIXED_KEY_LEN:
        raise ValueError("La key debe tener longitud fija " + str(FIXED_KEY_LEN))
    out = []
    for i, ch in enumerate(plaintext):
        p = shift(ch)
        k = shift(key[i % len(key)])
        out.append(unshift(p + k))
    return "".join(out)


def decrypt(ciphertext: str, key: str) -> str:
    validate_printable_ascii(ciphertext, "cipher")
    validate_printable_ascii(key, "key")
    if len(key) != FIXED_KEY_LEN:
        raise ValueError("La key debe tener longitud fija " + str(FIXED_KEY_LEN))

    out = []
    for i, ch in enumerate(ciphertext):
        c = shift(ch)
        k = shift(key[i % len(key)])
        out.append(unshift(c - k))
    return "".join(out)


def main() -> None:
    mode = input("Modo (enc/dec): ").strip().lower()

    if mode == "enc":
        plaintext = input("Texto (ASCII imprimible): ")
        key = input(
            "Key fija de " + str(FIXED_KEY_LEN) + " chars (Enter para generar desde una frase): "
        ).strip()
        if not key:
            phrase = input("Frase para generar la key fija: ")
            key = generate_fixed_key(FIXED_KEY_LEN, seed_from_text(phrase))

        cipher = encrypt(plaintext, key)
        print("KEY=" + key)
        print("CIPHER=" + cipher)
        return

    ciphertext = input("Cipher (ASCII imprimible): ")
    key = input("Key fija de " + str(FIXED_KEY_LEN) + " chars: ").strip()
    plaintext = decrypt(ciphertext, key)
    print(plaintext)


if __name__ == "__main__":
    main()
