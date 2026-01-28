ALFABETO_BASE64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


def ascii_a_binario(texto: str, separador: str = " ") -> str:
	return separador.join(format(ord(c), "08b") for c in texto)


def binario_a_ascii(binario: str) -> str:
	return "".join(chr(int(b, 2)) for b in binario.split())


def base64_a_binario(texto: str, separador: str = " ") -> str:
	texto = "".join(texto.split())
	bits = ""

	for c in texto:
		if c == "=":
			break
		i = ALFABETO_BASE64.find(c)
		if i == -1:
			raise ValueError("Base64 invalido")
		bits += format(i, "06b")

	pad = texto.count("=")
	if pad:
		bits = bits[: -(pad * 2)]

	while len(bits) % 8 != 0:
		bits += "0"

	salida = []
	for i in range(0, len(bits), 8):
		salida.append(bits[i : i + 8])

	return separador.join(salida)


def binario_a_base64(binario: str) -> str:
	bits = "".join(binario.split())

	if len(bits) % 8 != 0:
		raise ValueError("Binario invalido (debe venir en bytes de 8 bits)")

	pad_bytes = (3 - ((len(bits) // 8) % 3)) % 3
	if pad_bytes:
		bits += "0" * (pad_bytes * 8)

	salida = []
	for i in range(0, len(bits), 6):
		grupo = bits[i : i + 6]
		if len(grupo) < 6:
			grupo = grupo.ljust(6, "0")
		salida.append(ALFABETO_BASE64[int(grupo, 2)])

	pad_chars = pad_bytes * 8 // 6
	return "".join(salida[: len(salida) - pad_chars] + ["="] * pad_chars)


def base64_a_ascii(texto: str) -> str:
	binario = base64_a_binario(texto)
	return binario_a_ascii(binario)


def xor_binario(binario: str, clave: str, separador: str = " ") -> str:
	bits = binario.split()
	clave_bits = clave.split()

	resultado = []
	for i in range(len(bits)):
		x = int(bits[i], 2) ^ int(clave_bits[i % len(clave_bits)], 2)
		resultado.append(format(x, "08b"))

	return separador.join(resultado)


def menu() -> None:
	print("1) ASCII a Binario")
	print("2) Base64 a Binario")
	print("3) Binario a Base64")
	print("4) Binario a ASCII")
	print("5) Base64 a ASCII")
	print("6) XOR a un Binario")
	print("0) Salir")


if __name__ == "__main__":
	while True:
		menu()
		opcion = input("Opcion: ").strip()

		if opcion == "0":
			break

		if opcion == "1":
			texto = input("Texto ASCII: ")
			print(ascii_a_binario(texto))

		elif opcion == "2":
			texto = input("Texto Base64: ")
			print(base64_a_binario(texto))

		elif opcion == "3":
			binario = input("Binario (bytes separados por espacios): ")
			print(binario_a_base64(binario))

		elif opcion == "4":
			binario = input("Binario (bytes separados por espacios): ")
			print(binario_a_ascii(binario))

		elif opcion == "5":
			texto = input("Texto Base64: ")
			print(base64_a_ascii(texto))

		elif opcion == "6":
			binario = input("Binario (bytes separados por espacios): ")
			clave = input("Clave binaria (bytes separados por espacios): ")
			print(xor_binario(binario, clave))

		else:
			print("Opcion invalida")