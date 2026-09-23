import io
import lz4.block
from .constants import MAGIC_NUMBER

def decompress_save_bytes(binary_data: bytes) -> str:

    # Envuelve los datos de entrada en un objeto
    stream = io.BytesIO(binary_data)

    # Calcula el tamaño total en bytes del archivo comprimido
    total_size = len(binary_data)

    # Array de bytes donde se guardarán los trozos del JSON
    decompressed_chunks = bytearray()

    # Bucle que se ejecuta mientras quede archivo por leer
    while stream.tell() < total_size:

        magic = int.from_bytes(stream.read(4), "little")

        # Comprobación de que el número mágico es idéntico
        if (magic != MAGIC_NUMBER):
            raise ValueError(
                f"Bloque inválido en offset {stream.tell() - 4}. "
                f"Esperado: 0x{MAGIC_NUMBER:08X}, encontrado: 0x{magic:08X}"
            )

        # Lee el tamaño en bytes que ocupa el bloque comprimido actual
        compressed_size = int.from_bytes(stream.read(4), "little")

        # Lee el tamaño esperado en bytes una vez descomprimido el bloque
        uncompressed_size = int.from_bytes(stream.read(4), "little")

        stream.seek(4, io.SEEK_CUR) # Salto de padding (bytes de relleno)

        # Lee la cantidad de bytes indicada
        compressed_block = stream.read(compressed_size)

        # Pasa el fragmento comprimido a la librería LZ4
        raw_block = lz4.block.decompress(compressed_block, uncompressed_size=uncompressed_size)

        # Se añade los bytes descomprimidos al final del array
        decompressed_chunks += raw_block

    # Limpia bytes nulos al final y decodifica a texto UTF-8
    return decompressed_chunks.rstrip(b"\x00").decode("utf-8", errors="replace")
