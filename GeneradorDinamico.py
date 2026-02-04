PRINTABLE_START = 32
PRINTABLE_END = 126
ALPHABET_SIZE = PRINTABLE_END - PRINTABLE_START + 1 #95 valores
MODULUS = 2**31

A = 1103515245
C = 12345

def seed_from_text(text: str) -> int:
    seed = 0
    for ch in text:
        seed = (seed * 131 + ord(ch)) % MODULUS
    seed &= 0x7FFFFFFF
    return seed or 1

def parse_seed(raw: str) -> int:
    raw = raw.strip()
    if not raw:
        phrase = input("Frase para generar la semilla: ")
        return seed_from_text(phrase)

    try:
        s = int(raw) & 0x7FFFFFFF
        return s or 1
    except ValueError:
        return seed_from_text(raw)

def make_key(length: int, seed: int) -> str:
    state = seed or 1
    out = []

    for _ in range(length):
        state = (A * state + C) % MODULUS
        out.append(chr(PRINTABLE_START + (state % ALPHABET_SIZE)))

    return "".join(out)

def main():
    length = int(input("Longitud de la llave (>0): ").strip())
    if length <= 0:
        raise ValueError

    raw_seed = input("Semilla (número o texto). Enter para frase: ")
    seed = parse_seed(raw_seed)

    print(make_key(length, seed))

if __name__ == "__main__":
    main()