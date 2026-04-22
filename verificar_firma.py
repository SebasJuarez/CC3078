from __future__ import annotations

import sys


def cargar_clave_publica(path: str):
    try:
        from Crypto.PublicKey import RSA
    except ImportError:
        print("[ERROR] No se pudo importar pycryptodome.")
        print("Instala la libreria con: pip install pycryptodome")
        return None

    try:
        with open(path, "rb") as archivo:
            datos = archivo.read()
        return RSA.import_key(datos)
    except FileNotFoundError:
        print(f"[ERROR] Archivo no encontrado: {path}")
        return None
    except (ValueError, IndexError, TypeError) as error:
        print(f"[ERROR] Clave publica invalida en {path}: {error}")
        return None
    except OSError as error:
        print(f"[ERROR] Error al leer {path}: {error}")
        return None


def leer_archivo_binario(path: str):
    try:
        with open(path, "rb") as archivo:
            return archivo.read()
    except FileNotFoundError:
        print(f"[ERROR] Archivo no encontrado: {path}")
        return None
    except OSError as error:
        print(f"[ERROR] Error al leer {path}: {error}")
        return None


def verificar_firma(
    public_key_path: str = "medisoft_pub.pem",
    manifest_path: str = "SHA256SUMS.txt",
    signature_path: str = "SHA256SUMS.sig",
) -> bool:
    try:
        from Crypto.Hash import SHA256
        from Crypto.Signature import pkcs1_15
    except ImportError:
        print("[ERROR] No se pudo importar pycryptodome para verificar.")
        return False

    clave_publica = cargar_clave_publica(public_key_path)
    if clave_publica is None:
        return False

    manifiesto = leer_archivo_binario(manifest_path)
    if manifiesto is None:
        return False

    firma = leer_archivo_binario(signature_path)
    if firma is None:
        return False

    resumen = SHA256.new(manifiesto)

    try:
        # Se usa PKCS#1 v1.5 para mantener compatibilidad con el proceso de firmado.
        pkcs1_15.new(clave_publica).verify(resumen, firma)
        print("[OK] Firma valida: SHA256SUMS.txt es autentico y no fue modificado.")
        return True
    except (ValueError, TypeError):
        print("[FAIL] Firma invalida: SHA256SUMS.txt fue alterado o la firma no corresponde.")
        return False


def main() -> None:
    exito = verificar_firma(
        public_key_path="medisoft_pub.pem",
        manifest_path="SHA256SUMS.txt",
        signature_path="SHA256SUMS.sig",
    )

    sys.exit(0 if exito else 1)


if __name__ == "__main__":
    main()