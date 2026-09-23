from engine import process_save_file

def cli_user_interaction():
    print("Inserta la versión del juego a la que quieras bajar: ")
    version_solicitada = int(input())
    return version_solicitada

def main():

    # Lee el archivo binario original de Steam
    with open("save.hg", "rb") as f:
        input_bytes = f.read()

    target_version = cli_user_interaction()

    print(f"[1/2] Procesando save.hg hacia versión {target_version}...")

    # Ejecuta todo el pipeline a través del engine
    fixed_bytes, report = process_save_file(input_bytes, target_version)

    print(f"[OK] Versión modificada: {report}")

    # Guarda el nuevo archivo binario listo para la consola
    with open("save_modificado.hg", "wb") as f:
        f.write(fixed_bytes)   

    print("[2/2] Archivo 'save_modificado.hg' generado con éxito.")


if __name__ == "__main__":
    main()