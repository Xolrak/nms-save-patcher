import json
from typing import Any
from .constants import VERSION_KEYS

"""Modifica el campo de versión dentro del JSON y lo devuelve"""
def patch_version(json_str: str, target_version: int) -> tuple[str, dict[str, Any]]:

    # Parsea la cadena JSON a un diccionario
    data: dict[str, Any] = json.loads(json_str)

    modified = False
    report = {}

    # Recorre las posibles claves que representan la version en el juego
    for key in VERSION_KEYS:
        # Comprueba si la clave existe y si su valor es númerico
        if key in data and isinstance(data[key], int):
            # Registra el cambio en el informe final
            report[key] = {"old": data[key], "new": target_version}
            # Sobrescribe la version con el valor
            data[key] = target_version
            modified = True

    # Si no se ha encontrado ninguna clave, se lanza error
    if not modified:
        raise KeyError(
            f"No se encontró ninguna clave de versión ({VERSION_KEYS})"
        )

    # Serializa de nuevo el diccionario a texto JSON minificado sin espacios
    patched_json_str = json.dumps(data,separators=(",", ":"), ensure_ascii=False)

    return patched_json_str, report