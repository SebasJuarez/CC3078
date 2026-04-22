from __future__ import annotations

import hashlib
import ssl
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


PASSWORDS = ["admin", "123456", "hospital", "medisoft2024"]
HIBP_URL = "https://api.pwnedpasswords.com/range/{prefix}"
USER_AGENT = "python-hash-lab"
REQUEST_TIMEOUT_SECONDS = 10


def sha256_hex(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def sha1_hex(password: str) -> str:
    return hashlib.sha1(password.encode("utf-8")).hexdigest()


def consultar_hibp(prefix: str) -> str:
    url = HIBP_URL.format(prefix=prefix)
    request = Request(url, headers={"User-Agent": USER_AGENT})

    # El contexto SSL por defecto evita depender de certificados externos.
    with urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS, context=ssl.create_default_context()) as response:
        return response.read().decode("utf-8")


def procesar_respuesta_hibp(respuesta: str, suffix: str) -> int:
    if not respuesta.strip():
        return 0

    for linea in respuesta.splitlines():
        if ":" not in linea:
            continue
        sufijo_api, count = linea.split(":", 1)
        if sufijo_api.strip().upper() == suffix.upper():
            try:
                return int(count.strip())
            except ValueError:
                return 0
    return 0


def evaluar_password(password: str) -> tuple[str, str, str, int, str]:
    hash_sha256 = sha256_hex(password)
    hash_sha1 = sha1_hex(password)
    prefix = hash_sha1[:5].upper()
    suffix = hash_sha1[5:].upper()

    try:
        respuesta = consultar_hibp(prefix)
        filtraciones = procesar_respuesta_hibp(respuesta, suffix)
        estado = "ok"
    except HTTPError as error:
        filtraciones = 0
        estado = f"error HTTP {error.code}"
    except URLError:
        filtraciones = 0
        estado = "error de conexión"
    except TimeoutError:
        filtraciones = 0
        estado = "timeout"
    except Exception:
        filtraciones = 0
        estado = "error inesperado"

    return password, hash_sha256, hash_sha1, filtraciones, estado


def imprimir_tabla(resultados: Iterable[tuple[str, str, str, int, str]]) -> None:
    filas = list(resultados)
    ancho_password = max(len("Contraseña"), *(len(fila[0]) for fila in filas))
    ancho_sha256 = len("SHA-256")
    ancho_sha1 = len("SHA-1")
    ancho_filtraciones = len("Filtraciones")
    ancho_estado = max(len("Estado"), *(len(fila[4]) for fila in filas))

    encabezado = (
        f"{'Contraseña':<{ancho_password}}  "
        f"{'SHA-256':<{ancho_sha256}}  "
        f"{'SHA-1':<{ancho_sha1}}  "
        f"{'Filtraciones':>{ancho_filtraciones}}  "
        f"{'Estado':<{ancho_estado}}"
    )
    print(encabezado)
    print("-" * len(encabezado))

    for password, hash_sha256, hash_sha1, filtraciones, estado in filas:
        print(
            f"{password:<{ancho_password}}  "
            f"{hash_sha256:<{ancho_sha256}}  "
            f"{hash_sha1:<{ancho_sha1}}  "
            f"{filtraciones:>{ancho_filtraciones}}  "
            f"{estado:<{ancho_estado}}"
        )


def main() -> None:
    resultados = [evaluar_password(password) for password in PASSWORDS]

    imprimir_tabla(resultados)
    print()
    print("k-anonymity consiste en enviar solo un prefijo del hash para reducir la exposición del valor completo.")
    print("No se envía el hash completo porque eso revelaría demasiada información sobre la contraseña consultada.")
    print("Usar SHA-256 directo para contraseñas es inseguro porque es un hash rápido y no incorpora sal ni costo computacional.")


if __name__ == "__main__":
    main()