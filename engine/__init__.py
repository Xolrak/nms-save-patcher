from .compressor import compress_save_string
from .decompressor import decompress_save_bytes
from .modifier import patch_version

def process_save_file(
        file_bytes: bytes, target_version: int
) -> tuple[bytes, dict]:

    # Descomprime los bloques binarios a texto JSON
    json_text = decompress_save_bytes(file_bytes)

    # Modifica el campo de version dentro del JSON
    pathed_version, report = patch_version(json_text, target_version)

    # Reempaqueta el texto en la estructura de bloquews binaruios LZ4
    output_bytes = compress_save_string(pathed_version)

    # Devuelve el archivo ninario listo para guardar y el reporte de cambios
    return output_bytes, report