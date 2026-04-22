#!/usr/bin/env python3
"""Compara varios algoritmos hash para dos textos casi iguales."""

import hashlib


def calcular_hash(texto: str, constructor_hash) -> str:
    """Devuelve el hash hexadecimal de un texto usando el algoritmo indicado."""
    return constructor_hash(texto.encode("utf-8")).hexdigest()


def obtener_longitud_bits(constructor_hash) -> int:
    """Obtiene la longitud del hash en bits a partir del digest del algoritmo."""
    return constructor_hash().digest_size * 8


def contar_bits_distintos(hash_hex_1: str, hash_hex_2: str) -> int:
    """Cuenta cuántos bits difieren entre dos hashes hexadecimales usando XOR."""
    valor_1 = int(hash_hex_1, 16)
    valor_2 = int(hash_hex_2, 16)
    xor_resultado = valor_1 ^ valor_2
    # Compatible con versiones que no implementan int.bit_count().
    return bin(xor_resultado).count("1")


def imprimir_tabla(textos: list[str], algoritmos: list[tuple[str, callable]]) -> None:
    """Imprime una tabla con los hashes agrupados por algoritmo."""
    ancho_texto = max(len("Texto"), *(len(texto) for texto in textos))
    encabezado = (
        f"{'Texto':<{ancho_texto}}  "
        f"{'Algoritmo':<10}  "
        f"{'Longitud en bits':>16}  "
        f"{'Longitud hexadecimal':>20}  "
        f"Valor del hash"
    )

    print(encabezado)
    print("-" * len(encabezado))

    # Se imprimen dos filas por algoritmo para comparar fácil entre textos.
    for nombre_algoritmo, constructor in algoritmos:
        for texto in textos:
            hash_hex = calcular_hash(texto, constructor)
            longitud_bits = obtener_longitud_bits(constructor)
            longitud_hex = len(hash_hex)
            print(
                f"{texto:<{ancho_texto}}  "
                f"{nombre_algoritmo:<10}  "
                f"{longitud_bits:>16}  "
                f"{longitud_hex:>20}  "
                f"{hash_hex}"
            )
        print()


def main() -> None:
    """Punto de entrada principal del script."""
    textos = ["MediSoft-v2.1.0", "medisoft-v2.1.0"]

    algoritmos = [
        ("MD5", hashlib.md5),
        ("SHA-1", hashlib.sha1),
        ("SHA-256", hashlib.sha256),
        ("SHA3-256", hashlib.sha3_256),
    ]

    imprimir_tabla(textos, algoritmos)

    sha256_texto_1 = calcular_hash(textos[0], hashlib.sha256)
    sha256_texto_2 = calcular_hash(textos[1], hashlib.sha256)
    bits_distintos = contar_bits_distintos(sha256_texto_1, sha256_texto_2)


if __name__ == "__main__":
    main()