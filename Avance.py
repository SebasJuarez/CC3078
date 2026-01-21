from typing import Iterable


def ascii_a_binario(texto: str, separador: str = " ") -> str:
	bytes_ascii = texto.encode("ascii")
	return separador.join(format(b, "08b") for b in bytes_ascii)


if __name__ == "__main__":
	import sys

	if len(sys.argv) > 1:
		entrada = " ".join(sys.argv[1:])
		print(ascii_a_binario(entrada))
	else:
		entrada = input("Texto ASCII: ")
		print(ascii_a_binario(entrada))
