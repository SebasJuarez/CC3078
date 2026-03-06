# Laboratorio Block Ciphers - CC3078

Implementacion de DES, 3DES y AES para comparar modos de operacion.

## Estructura del proyecto

- manual_padding.py: implementación manual de pkcs7_pad y pkcs7_unpad
- generacion_llaves.py: generación de llaves DES/3DES/AES e IV
- des_ecb.py: cifrado/descifrado DES en modo ECB usando padding manual
- 3des.py: cifrado/descifrado 3DES en CBC usando libreria de padding
- imageComparations.py: cifrado de imagen BMP en AES-ECB y AES-CBC manteniendo header

## Librerias

Para instalar la libreria de crypto usa:

```bash
pip install pycryptodome
```

## Ejecucion

### 1) DES ECB (padding manual)

```bash
python3 des_ecb.py
```

### 2) 3DES CBC

```bash
python3 3des.py
```

### 3) AES ECB vs CBC en imagen

1. Colocar una imagen BMP llamada original.bmp en la raiz del proyecto.
2. Ejecutar:

```bash
python3 imageComparations.py
```

Esto genera:
- encrypted_ecb.bmp
- encrypted_cbc.bmp


### 4) Experimentos de analisis

```bash
python3 analysis_demos.py
```

Incluye:
- bloques repetidos en ECB vs CBC
- reutilizacion vs aleatoriedad de IV en CBC
- padding para mensajes de 5, 8 y 10 bytes

## Respuestas de analisis (Parte 2)

## 2.1 Tamano de clave

- DES: 8 bytes (64 bits nominales, 56 bits efectivos de seguridad)
- 3DES: 16 bytes (2-key) o 24 bytes (3-key)
- AES: 32 bytes para AES-256

DES es inseguro por su espacio de clave pequeno (2^56), vulnerable a fuerza bruta con hardware moderno.

Snippet de generacion:

```python
from generacion_llaves import generate_des_key, generate_3des_key, generate_aes_key
print(len(generate_des_key()))      # 8
print(len(generate_3des_key(2)))    # 16
print(len(generate_3des_key(3)))    # 24
print(len(generate_aes_key(256)))   # 32
```

## 2.2 ECB vs CBC

- DES implementado en ECB (`des_ecb.py`)
- 3DES implementado en CBC (`3des.py`)
- AES implementado en ECB y CBC para imagen (`aes_image_modes.py`)

Diferencias:
- ECB cifra cada bloque igual de forma independiente.
- CBC encadena bloques usando XOR con bloque previo e IV.
- En imagenes, ECB conserva patrones visibles; CBC los difumina.

## 2.3 Vulnerabilidad de ECB

No debe usarse en datos sensibles porque bloques de texto iguales producen bloques cifrados iguales, filtrando estructura.

Demostracion:
- ejecutar `python3 analysis_demos.py`
- en seccion `ECB vs CBC con bloques repetidos`, observar repeticion de bloques hex en ECB y no en CBC.

## 2.4 IV en CBC

IV = vector de inicializacion aleatorio del tamano de bloque.

- Necesario en CBC para romper igualdad deterministica del primer bloque.
- No se usa en ECB (pero ECB ya no es recomendado).

Experimento:
- `analysis_demos.py` muestra que con mismo IV y mismo mensaje: ciphertext igual.
- con IV distintos: ciphertext diferente.

## 2.5 Padding

Padding es necesario cuando el mensaje no es multiplo del tamano de bloque.

Casos demostrados en `analysis_demos.py`:
- 5 bytes: agrega `03 03 03` (si block=8 y faltan 3)
- 8 bytes: agrega bloque completo `08` repetido 8 veces
- 10 bytes: agrega 6 bytes `06`

Luego `pkcs7_unpad` recupera el mensaje original.

## 2.6 Recomendaciones de uso

| Modo | Recomendado para | Desventajas |
|---|---|---|
| ECB | Practica academica, nunca datos reales | Filtra patrones |
| CBC | Compatibilidad heredada con IV aleatorio unico | Requiere padding, no autentica |
| CTR | Streaming y paralelizacion | Requiere nonce/contador unico |
| GCM (AEAD) | Produccion moderna (confidencialidad + integridad) | Implementacion incorrecta con nonce repetido rompe seguridad |

Ejemplo modo seguro:
- Python: `AES.new(key, AES.MODE_GCM)`
- Java: `Cipher.getInstance("AES/GCM/NoPadding")`
