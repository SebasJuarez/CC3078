from __future__ import annotations

import hashlib
from pathlib import Path


BLOCK_SIZE = 64 * 1024
MANIFEST_NAME = "SHA256SUMS.txt"


def calcular_sha256(file_path: str | Path) -> str:
    digest = hashlib.sha256()
    with open(file_path, "rb") as archivo:
        while True:
            bloque = archivo.read(BLOCK_SIZE)
            if not bloque:
                break
            digest.update(bloque)
    return digest.hexdigest()


def verificar_archivo(nombre_archivo: str, hash_esperado: str) -> str:
    ruta = Path(nombre_archivo)
    if not ruta.exists():
        return f"[ERROR] {nombre_archivo} (no encontrado)"

    try:
        hash_actual = calcular_sha256(ruta)
    except PermissionError:
        return f"[ERROR] {nombre_archivo} (sin permisos)"

    if hash_actual.lower() == hash_esperado.lower():
        return f"[OK] {nombre_archivo}"
    return f"[FAIL] {nombre_archivo} (hash incorrecto)"


def leer_manifiesto(manifest_path: str | Path) -> list[tuple[str, str]]:
    ruta = Path(manifest_path)
    if not ruta.exists():
        raise FileNotFoundError(f"No existe el manifiesto: {manifest_path}")

    entradas: list[tuple[str, str]] = []
    with open(ruta, "r", encoding="utf-8") as manifiesto:
        for numero_linea, linea in enumerate(manifiesto, start=1):
            linea = linea.strip()
            if not linea:
                continue
            partes = linea.split(maxsplit=1)
            if len(partes) != 2:
                raise ValueError(f"Formato inválido en la línea {numero_linea}: {linea}")
            hash_esperado, nombre_archivo = partes
            if len(hash_esperado) != 64:
                raise ValueError(f"Hash inválido en la línea {numero_linea}: {linea}")
            entradas.append((hash_esperado, nombre_archivo))
    return entradas


def main() -> None:
    try:
        entradas = leer_manifiesto(MANIFEST_NAME)
    except FileNotFoundError as error:
        print(f"[ERROR] {error}")
        return
    except ValueError as error:
        print(f"[ERROR] {error}")
        return

    correctos = 0
    incorrectos = 0
    errores = 0

    for hash_esperado, nombre_archivo in entradas:
        estado = verificar_archivo(nombre_archivo, hash_esperado)
        print(estado)
        if estado.startswith("[OK]"):
            correctos += 1
        elif estado.startswith("[FAIL]"):
            incorrectos += 1
        else:
            errores += 1

    print()
    print("Resumen")
    print(f"Archivos correctos: {correctos}")
    print(f"Archivos incorrectos: {incorrectos}")
    print(f"Errores: {errores}")
    print("Prueba: modifica un solo byte de un archivo y vuelve a ejecutar la verificación.")
    print("Aunque el cambio sea mínimo, el hash SHA-256 cambiará por completo.")


if __name__ == "__main__":
    main()