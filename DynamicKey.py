PRINTABLE_START = 32
PRINTABLE_END = 126
ALPHABET_SIZE = (PRINTABLE_END - PRINTABLE_START) + 1  # 95 valores
MODULUS = 2**31


def validate_printable_ascii(s: str, label: str) -> None:
    for idx, ch in enumerate(s):
        code = ord(ch)
        if code < PRINTABLE_START or code > PRINTABLE_END:
            raise ValueError(
                label + " contiene un caracter no-ASCII-imprimible en índice " + str(idx) + ": "
                + "U+" + format(code, "04X")
            )


def shift(ch: str) -> int:
    return ord(ch) - PRINTABLE_START


def unshift(v: int) -> str:
    return chr(PRINTABLE_START + (v % ALPHABET_SIZE))


def lcg_next(state: int) -> int:
    return (1103515245 * state + 12345) % MODULUS


def seed_from_key(seed_key: str) -> int:
    seed = 0
    for ch in seed_key:
        seed = (seed * 131 + ord(ch)) % MODULUS
    seed &= 0x7FFFFFFF
    if seed == 0:
        seed = 1
    return seed


def keystream(seed_key: str, length: int) -> str:
    validate_printable_ascii(seed_key, "seed_key")
    if not seed_key:
        raise ValueError("seed_key no puede ser vacía")
    if length < 0:
        raise ValueError("length inválido")

    state = seed_from_key(seed_key)

    chars: list[str] = []
    for _ in range(length):
        state = lcg_next(state)
        chars.append(unshift(state % ALPHABET_SIZE))
    return "".join(chars)


def encrypt(plaintext: str, seed_key: str) -> tuple[str, str]:
    validate_printable_ascii(plaintext, "texto")
    ks = keystream(seed_key, len(plaintext))

    out: list[str] = []
    for i, ch in enumerate(plaintext):
        p = shift(ch)
        k = shift(ks[i])
        out.append(unshift(p + k))

    return ks, "".join(out)


def decrypt(ciphertext: str, seed_key: str) -> str:
    validate_printable_ascii(ciphertext, "cipher")
    ks = keystream(seed_key, len(ciphertext))

    out: list[str] = []
    for i, ch in enumerate(ciphertext):
        c = shift(ch)
        k = shift(ks[i])
        out.append(unshift(c - k))

    return "".join(out)


def interactive() -> int:
    mode = input("Modo (enc/dec): ").strip().lower()
    if mode not in ("enc", "dec"):
        raise ValueError("Modo inválido (usa enc o dec)")

    if mode == "enc":
        plaintext = input("Texto (ASCII imprimible): ")
        seed_key = input("Seed key (ASCII imprimible): ")
        ks, cipher = encrypt(plaintext, seed_key)
        print("KEYSTREAM=" + ks)
        print("CIPHER=" + cipher)
        return 0

    ciphertext = input("Cipher (ASCII imprimible): ")
    seed_key = input("Seed key (ASCII imprimible): ")
    plaintext = decrypt(ciphertext, seed_key)
    print(plaintext)
    return 0


def main() -> None:
    interactive()


if __name__ == "__main__":
    main()
