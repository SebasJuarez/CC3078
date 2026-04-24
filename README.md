# Proyecto 1
 Sebastian Juarez - 21471

## Introduccion

En este proyecto se resolvio un CTF dentro de contenedores de Docker. Cada reto estaba ambientado en el mundo de *One Piece* y consistia en explorar una estructura de carpetas llamada `ONEPIECE`, buscar archivos `flag.txt`, descifrar flags y utilizar esas flags como contrasenas para abrir archivos `.zip`.

Dentro de algunos zips aparecian imagenes falsas, pero en otros se encontraba un archivo llamado `poneglyph.jpeg`. Al revisar sus metadatos o cadenas internas, se obtenian fragmentos de historia relacionados con los Poneglyphs.

Todo el recorido de lo que se hizo se encuentra en los `.txt` de cada reto, pero a continuacion se presenta un resumen de los pasos mas importantes y las flags obtenidas.

---

## Challenge: Luffy

Primero entre al contenedor del reto de Luffy como usuario `root`:

```bash
docker exec -u root -it luffy_challenge bash
```

Dentro del contenedor encontre la carpeta principal:

```bash
ls
cd ONEPIECE
```

La estructura contenia varias islas:

```text
Alabasta
Dressrosa
Fishman_Island
Pirate_Island
Skypiea
```

Comence explorando `Alabasta`. En la ruta `Alabasta/Katorea/Casa_de_Toto` encontre un primer archivo `flag.txt`:

```bash
cat Alabasta/Katorea/Casa_de_Toto/flag.txt
```

El contenido era:

```text
Has encontrado un amigo y han decidido viajar juntos
```

Luego encontre un zip en:

```text
Alabasta/Rainbase/Casa_de_Vivi/data_622c67a66d94.zip
```

Lo extraje usando Python con la contrasena `onepiece`:

```bash
python3 -c "import zipfile; z=zipfile.ZipFile('Alabasta/Rainbase/Casa_de_Vivi/data_622c67a66d94.zip'); z.extractall('luffy_zip', pwd=b'onepiece'); print(z.namelist())"
```

El archivo extraido no era el Poneglyph correcto. Al revisarlo con `strings`, mostraba:

```text
Este poneglyph no es el que buscas
```

Continue explorando `Dressrosa`. En `Dressrosa/Acacia/Casa_de_Viola` encontre otro zip:

```text
Dressrosa/Acacia/Casa_de_Viola/data_35caf2817372.zip
```

Tambien lo extraje con la contrasena `onepiece`, pero nuevamente era un Poneglyph falso:

```text
Este poneglyph no es el que buscas
```

Despues, en la ruta:

```text
Dressrosa/Corrida_Colosseum/Casa_de_Rebecca/flag.txt
```

aparecio una flag cifrada en hexadecimal:

```text
747d75706e540155535003540d06500b03040607500451015351535702015752020f540708
```

Para descifrarla use XOR con mi carne `21471` como llave:

```python
flag_hex = "747d75706e540155535003540d06500b03040607500451015351535702015752020f540708"
key = "21471".encode()
data = bytes.fromhex(flag_hex)
out = bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])
print(out.decode())
```

El resultado fue:

```text
FLAG_f0ada1e91a92016b5e6bcbc50ec68e59
```

Mas adelante encontre el zip correcto en:

```text
Dressrosa/Royal_Palace/Casa_de_Riku_Dold_III/data_e1611bd1687d.zip
```

Al extraerlo con la contrasena `onepiece`, aparecio:

```text
poneglyph.jpeg
```

Al revisar la imagen con `strings`, encontre un texto hexadecimal en sus metadatos:

```text
665951174357425156435159514542125e5a177e5a504656115654575e55575514435e12424042554b11405f545b43145e425e505a5316411164585f5756584e415a115d5911535f145645465459474512455b17555b4257584757431443595711595e4241585a50115a5847435e404814585712455c5211455e465b551c
```

Tambien estaba cifrado con XOR usando la llave `21471`. Al descifrarlo, obtuve el fragmento de historia:

```text
The researchers on Ohara decided to study their island's Poneglyph in an attempt to discover the missing history of the world.
```

---

## Challenge: Zoro

Entre al contenedor del reto de Zoro:

```bash
docker exec -u root -it zoro_challenge bash
```

Busque todos los archivos `flag.txt` dentro del reto:

```bash
find / -name "flag.txt" 2>/dev/null
```

Entre las pistas importantes aparecieron varias referencias a `Gyoncorde_Plaza`, por ejemplo:

```text
Has encontrado un lugar lleno de secretos y misterios que apuntan a Gyoncorde_Plaza
Has encontrado un tesoro que apunta a Gyoncorde_Plaza
Has encontrado un mapa que apunta a Gyoncorde_Plaza
```

La flag cifrada estaba en:

```text
/home/zoro/ONEPIECE/Fishman_Island/Gyoncorde_Plaza/Casa_de_Shirahoshi/flag.txt
```

Su contenido era:

```text
1ec06e284e33ba8964548532262ca1e2fd3c3835c83dc083bb6b9201142229746744d845a6
```

Para descifrarla use RC4 con mi carne `21471` como llave. El descifrado produjo:

```text
FLAG_2c4ffb7acddea707305e0e0cca7c74c1
```

Luego busque los archivos `.zip` disponibles:

```bash
find / -name "*.zip" 2>/dev/null
```

Use la flag obtenida en Luffy como contrasena para probar los zips:

```text
FLAG_f0ada1e91a92016b5e6bcbc50ec68e59
```

Varios zips contenian imagenes falsas con el mensaje:

```text
Este poneglyph no es el que buscas
```

El zip correcto fue:

```text
/home/zoro/ONEPIECE/Dressrosa/Royal_Palace/Casa_de_Rebecca/data_44629a977407.zip
```

Al extraerlo aparecio:

```text
poneglyph.jpeg
```

Al revisar sus cadenas internas, encontre este texto cifrado:

```text
7a5e43524757431817455a544d1746574351175d5b5c5d43545611564e115e50575c115d571456525154474411465e14565f56115f595e455d51535657115b5111465951175e4659514511625e5a52565e48445f421e1155595512455c42421242515945125e414311405447525040525c5243411140581154585a53115f5e4652115b5f5258435f50405e5e5c115b59114659515a1d125a5a58465b5f5317455a5414444547554d175e5411405f5412615b5954555d4d475941114356421258585b5455505819
```

Al descifrarlo con XOR y llave `21471`, obtuve:

```text
However, they were limited by lack of access to and knowledge of the other Poneglyphs, and thus sent out researchers to find more information on them, knowing the study of the Poneglyphs was illegal.
```

---

## Challenge: Usopp

Entre al contenedor de Usopp:

```bash
docker exec -u root -it usopp_challenge bash
```

Busque los archivos `flag.txt`:

```bash
find / -name "flag.txt" 2>/dev/null
```

Las pistas apuntaban principalmente hacia `Rainbase`. Algunas de las pistas encontradas fueron:

```text
Has encontrado un lugar lleno de secretos y misterios que apuntan a Rainbase
Has encontrado un lugar seguro
Has encontrado un lugar abandonado
```

La flag cifrada estaba en:

```text
/home/usopp/ONEPIECE/Alabasta/Rainbase/Casa_de_Igaram/flag.txt
```

Su contenido era:

```text
a77742694e4902d34c6e3e6e84cfdf7c483902319b4e45d8144f71bf11ac9382bf4e5f8b3c
```

El cifrado de Usopp usaba un generador pseudoaleatorio con semilla. Use la semilla `1234` para generar el keystream y hacer XOR contra el texto cifrado:

```python
import random

cipher_hex = "a77742694e4902d34c6e3e6e84cfdf7c483902319b4e45d8144f71bf11ac9382bf4e5f8b3c"
seed = 1234

def generate_keystream(seed, length):
    random.seed(seed)
    return bytes([random.randint(0, 255) for _ in range(length)])

cipherbytes = bytes.fromhex(cipher_hex)
keystream = generate_keystream(seed, len(cipherbytes))
plaintext = bytes([c ^ k for c, k in zip(cipherbytes, keystream)])

print(plaintext.decode())
```

El resultado fue:

```text
FLAG_c0f5f1f5820fd86b1d67bf516e7719c5
```

Despues busque todos los zips:

```bash
find / -name "*.zip" 2>/dev/null
```

Para extraerlos use la flag obtenida en Zoro como contrasena:

```text
FLAG_2c4ffb7acddea707305e0e0cca7c74c1
```

El zip correcto fue:

```text
/home/usopp/ONEPIECE/Dressrosa/Toy_House/Casa_de_Doflamingo/data_202f588c2236.zip
```

Este contenia:

```text
poneglyph.jpeg
```

Al revisar la imagen, encontre el texto hexadecimal:

```text
7c585758117d5d425e501e11555b5e5c5614405846591443595b43404e1c4659465254125e405f5440115545525a5051585d5d565d4445411d14445446115b424512455b174257501a17625355584e1d12455c52584011554345575c44431154505d5b54561d14565f5611405f544b1143524357115d5945574357524146545017534b11405f54127c5545585c54471b115e545741585c5614785d44585517504111405f5412425b5b5412424145475b475b451f12
```

Al descifrarlo con XOR y llave `21471`, obtuve:

```text
Nico Olvia, along with thirty-three other archaeologists, set out to sea. Sadly, their attempt failed, and they were intercepted by the Marines, leaving Olvia as the sole survivor.
```

---

## Challenge: Nami

Finalmente entre al contenedor de Nami:

```bash
docker exec -u root -it nami_challenge bash
```

Busque todos los archivos `flag.txt`:

```bash
find / -name "flag.txt" 2>/dev/null
```

Varias pistas apuntaban hacia `Coral_Hill`, por ejemplo:

```text
Has encontrado un lugar lleno de secretos y misterios que apuntan a Coral_Hill
Has encontrado una pista que apunta a Coral_Hill
Has encontrado un tesoro que apunta a Coral_Hill
Has encontrado un mapa que apunta a Coral_Hill
```

La flag cifrada estaba en:

```text
/home/nami/ONEPIECE/Fishman_Island/Coral_Hill/Casa_de_Neptune/flag.txt
```

Su contenido era:

```text
ce557130ff2bf80ce4f716f632221348c23f2b0c434b1b9b30b17614dee35e0d32b7f6473e
```

Para descifrarla use ChaCha20 con mi carne `21471`. La llave y el nonce se derivaban repitiendo el carne:

```python
from Crypto.Cipher import ChaCha20

def generate_key_nonce(user_id):
    key = (user_id.encode() * 32)[:32]
    nonce = (user_id.encode() * 8)[:8]
    return key, nonce

def chacha20_decrypt(ciphertext, user_id):
    key, nonce = generate_key_nonce(user_id=user_id)
    cipher = ChaCha20.new(key=key, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext.decode()

hex_content = "ce557130ff2bf80ce4f716f632221348c23f2b0c434b1b9b30b17614dee35e0d32b7f6473e"
cipher_bytes = bytes.fromhex(hex_content)
print(chacha20_decrypt(cipher_bytes, "21471"))
```

El resultado fue:

```text
FLAG_0552761e1d4ca96aa445a82171c27e7e
```

Luego busque los zips disponibles:

```bash
find / -name "*.zip" 2>/dev/null
```

Para extraerlos use la flag obtenida en Usopp como contrasena:

```text
FLAG_c0f5f1f5820fd86b1d67bf516e7719c5
```

El zip correcto fue:

```text
/home/nami/ONEPIECE/Dressrosa/Royal_Palace/Casa_de_Riku_Dold_III/data_45e870e6966c.zip
```

Este contenia:

```text
poneglyph.jpeg
```

Al inspeccionar la imagen, encontre el texto hexadecimal:

```text
66595117665d43585311755e4252435c5c5159451259555311535d43564841115652545c114356434b115b5111465951175040525c56545d5d5b50584145471753575255424257115b51114659515e43125a5a58465e545050541e1156424512435144545343575f585c56144359571164585f5756584e415a42145a54535f4017455a544d1759535514565f12544c5444415414435e12505743115356555e5f4145144359575c1a
```

Al descifrarlo con XOR y llave `21471`, obtuve:

```text
The World Government had always been wary of the archaeologists because of their knowledge, but researching the Poneglyphs meant they had an excuse to act against them.
```

---

## Resumen de flags

| Challenge | Metodo de cifrado | Flag obtenida |
| --- | --- | --- |
| Luffy | XOR con llave `21471` | `FLAG_f0ada1e91a92016b5e6bcbc50ec68e59` |
| Zoro | RC4 con llave `21471` | `FLAG_2c4ffb7acddea707305e0e0cca7c74c1` |
| Usopp | XOR con PRNG y semilla `1234` | `FLAG_c0f5f1f5820fd86b1d67bf516e7719c5` |
| Nami | ChaCha20 con llave derivada de `21471` | `FLAG_0552761e1d4ca96aa445a82171c27e7e` |

## Resumen de Poneglyphs encontrados

| Challenge | Ubicacion del zip correcto | Contenido |
| --- | --- | --- |
| Luffy | `Dressrosa/Royal_Palace/Casa_de_Riku_Dold_III/data_e1611bd1687d.zip` | `poneglyph.jpeg` |
| Zoro | `Dressrosa/Royal_Palace/Casa_de_Rebecca/data_44629a977407.zip` | `poneglyph.jpeg` |
| Usopp | `Dressrosa/Toy_House/Casa_de_Doflamingo/data_202f588c2236.zip` | `poneglyph.jpeg` |
| Nami | `Dressrosa/Royal_Palace/Casa_de_Riku_Dold_III/data_45e870e6966c.zip` | `poneglyph.jpeg` |
