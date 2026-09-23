import io
import lz4.block
from .constants import MAGIC_NUMBER, BLOCK_SIZE

def compress_save_string(json_str: str) -> bytes:

    # Codifica la cadena de JSON a bytes en formato UTF-8
    raw_bytes = json_str.encode("utf-8")

    # Se asegura que los datos terminen en byte nulo
    if not raw_bytes.endswith(b"\x00"):
        raw_bytes += b"\x00"

    # Se envuelve los bytes en un stream de memoria
    stream = io.BytesIO(raw_bytes)

    # Tamaño total sin comprimir
    total_size = len(raw_bytes)

    # Array de bytes donde se empaquetará las cabeceras y los bloques
    output = bytearray()

    # Bucle que corta y comprime el JSON en bloques de máximo 512 KB
    while stream.tell() < total_size:

        # Calcula el tamaño
        chunk_size = min(BLOCK_SIZE, total_size - stream.tell())

        # Lee el fragmento sin comprimir
        chunk = stream.read(chunk_size)

        # Comprime el bloque con LZ4 sin almacenar metadatos adicionales
        compressed_block = lz4.block.compress(chunk, store_size=False)

        # Escribe los 4 bytes del número mágico
        output += MAGIC_NUMBER.to_bytes(4, "little")

        # Escribe los 4 bytes con el tamaño del bloque comprimido
        output += len(compressed_block).to_bytes(4, "little")

        # Escribe los 4 bytes con el tamaño del bloque sin comprimir
        output += chunk_size.to_bytes(4, "little")

        # Escribe los 4 bytes de relleno (padding) a ceros
        output += (0).to_bytes(4, "little")

        # Añade el bloque de datos comprimido a continuación a la cabecera
        output += compressed_block

    # Convierte el array mutable a bytes inmutables para el retorno
    return bytes(output)
