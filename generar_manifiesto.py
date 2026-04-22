from __future__ import annotations

import argparse
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


def procesar_archivos(lista_archivos: list[str]) -> list[str]:
    if len(lista_archivos) < 5:
        raise ValueError("Se requieren al menos 5 archivos para generar el manifiesto.")

    lineas = []
    for archivo in lista_archivos:
        ruta = Path(archivo)
        try:
            hash_hex = calcular_sha256(ruta)
            lineas.append(f"{hash_hex} {ruta.name}")
        except FileNotFoundError:
            print(f"[ERROR] {archivo} (no encontrado)")
        except PermissionError:
            print(f"[ERROR] {archivo} (sin permisos)")

    return lineas


def escribir_manifiesto(lineas: list[str]) -> None:
    if not lineas:
        return

    with open(MANIFEST_NAME, "a", encoding="utf-8") as manifiesto:
        for linea in lineas:
            manifiesto.write(f"{linea}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Genera SHA256SUMS.txt para varios archivos.")
    parser.add_argument("archivos", nargs="*", help="Lista de archivos a incluir en el manifiesto")
    args = parser.parse_args()

    if len(args.archivos) < 5:
        print("Debes proporcionar al menos 5 archivos.")
        return

    lineas = procesar_archivos(args.archivos)
    escribir_manifiesto(lineas)
    print(f"Manifiesto actualizado: {MANIFEST_NAME}")
    print("Prueba: modifica un solo byte en cualquiera de los archivos y vuelve a ejecutar el script.")
    print("El hash cambiará por completo, lo que demuestra la sensibilidad del SHA-256 a cambios mínimos.")


if __name__ == "__main__":
    main()