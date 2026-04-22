from __future__ import annotations

from pathlib import Path
import sys


def generar_par_claves(bits: int = 2048):
    try:
        from Crypto.PublicKey import RSA
    except ImportError:
        print("[ERROR] No se pudo importar pycryptodome.")
        print("Instala la libreria con: pip install pycryptodome")
        return None, None

    try:
        clave_privada = RSA.generate(bits)
        clave_publica = clave_privada.publickey()
        return clave_privada, clave_publica
    except Exception as error:
        print(f"[ERROR] No se pudo generar el par de claves: {error}")
        return None, None


def guardar_claves(clave_privada, clave_publica) -> bool:
    if clave_privada is None or clave_publica is None:
        return False

    try:
        privada_pem = clave_privada.export_key()
        publica_pem = clave_publica.export_key()

        with open("medisoft_priv.pem", "wb") as archivo_privado:
            archivo_privado.write(privada_pem)

        with open("medisoft_pub.pem", "wb") as archivo_publico:
            archivo_publico.write(publica_pem)

        # La clave privada no debe compartirse
        print("Clave privada generada: medisoft_priv.pem")
        # La clave publica si puede distribuirse
        print("Clave publica generada: medisoft_pub.pem")
        return True
    except OSError as error:
        print(f"[ERROR] No se pudieron guardar las claves: {error}")
        return False


def firmar_manifiesto(clave_privada, manifiesto: str = "SHA256SUMS.txt") -> bool:
    if clave_privada is None:
        return False

    ruta_manifiesto = Path(manifiesto)
    if not ruta_manifiesto.exists():
        print(f"[ERROR] No se encontro {manifiesto}")
        return False

    try:
        from Crypto.Hash import SHA256
        from Crypto.Signature import pkcs1_15
    except ImportError:
        print("[ERROR] No se pudo importar pycryptodome para firmar.")
        return False

    try:
        contenido = ruta_manifiesto.read_bytes()
        resumen = SHA256.new(contenido)
        firma = pkcs1_15.new(clave_privada).sign(resumen)

        with open("SHA256SUMS.sig", "wb") as archivo_firma:
            archivo_firma.write(firma)

        print("Manifiesto firmado correctamente")
        print("Firma guardada en SHA256SUMS.sig")
        return True
    except OSError as error:
        print(f"[ERROR] No se pudo leer/escribir archivos de firma: {error}")
        return False
    except (ValueError, TypeError) as error:
        print(f"[ERROR] Fallo criptografico al firmar: {error}")
        return False


def main() -> None:
    clave_privada, clave_publica = generar_par_claves(bits=2048)
    if clave_privada is None or clave_publica is None:
        sys.exit(1)

    if not guardar_claves(clave_privada, clave_publica):
        sys.exit(1)

    if not firmar_manifiesto(clave_privada, manifiesto="SHA256SUMS.txt"):
        sys.exit(1)


if __name__ == "__main__":
    main()