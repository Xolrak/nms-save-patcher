# Magic Number (identificador del bloque)
MAGIC_NUMBER: int = 0xFEEDA1E5

# Tamaño máximo del búfer sin comprimir por bloque (512 KB)
BLOCK_SIZE: int = 0x80000

# Tamaño de la cabecera de cada bloque en Bytes
HEADER_SIZE: int = 16

# Claves conocidas del número de versión en el JSON
VERSION_KEYS: tuple[str, ...] = ("Version", "F2P")