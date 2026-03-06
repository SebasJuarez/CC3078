from pathlib import Path
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from generacion_llaves import generate_aes_key, generate_iv


def split_bmp_header(data: bytes) -> tuple[bytes, bytes]:
    if len(data) < 54 or data[:2] != b"BM":
        raise ValueError("Se esperaba un archivo BMP valido")
    pixel_offset = int.from_bytes(data[10:14], "little")
    if pixel_offset <= 0 or pixel_offset >= len(data):
        raise ValueError("Header BMP invalido")
    return data[:pixel_offset], data[pixel_offset:]


def trim_to_original_size(header: bytes, encrypted_pixels: bytes, original_pixels_len: int) -> bytes:
    return header + encrypted_pixels[:original_pixels_len]


def encrypt_bmp_with_aes_modes(input_bmp: str, output_ecb: str, output_cbc: str, key: bytes | None = None):
    src = Path(input_bmp)
    raw = src.read_bytes()
    header, pixels = split_bmp_header(raw)

    aes_key = key or generate_aes_key(256)
    if len(aes_key) != 32:
        raise ValueError("La clave AES-256 debe ser de 32 bytes")

    ecb_cipher = AES.new(aes_key, AES.MODE_ECB)
    cbc_iv = generate_iv(AES.block_size)
    cbc_cipher = AES.new(aes_key, AES.MODE_CBC, iv=cbc_iv)

    padded_pixels = pad(pixels, AES.block_size)
    ecb_encrypted = ecb_cipher.encrypt(padded_pixels)
    cbc_encrypted = cbc_cipher.encrypt(padded_pixels)

    Path(output_ecb).write_bytes(trim_to_original_size(header, ecb_encrypted, len(pixels)))
    Path(output_cbc).write_bytes(trim_to_original_size(header, cbc_encrypted, len(pixels)))

    return aes_key, cbc_iv


if __name__ == "__main__":
    base = Path(".")
    input_image = base / "original.bmp"
    out_ecb = base / "encrypted_ecb.bmp"
    out_cbc = base / "encrypted_cbc.bmp"

    if not input_image.exists():
        print("No se encontro original.bmp.")
    else:
        key, iv = encrypt_bmp_with_aes_modes(str(input_image), str(out_ecb), str(out_cbc))
        print("AES-256 key (hex):", key.hex())
        print("CBC IV (hex):", iv.hex())
        print("Imagen ECB guardada en:", out_ecb)
        print("Imagen CBC guardada en:", out_cbc)
