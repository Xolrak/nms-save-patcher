from engine import process_save_file
from engine.decompressor import decompress_save_bytes, get_save_version


def cli_user_interaction(current_version: int | None) -> int:
    banner = r"""
      _  _ __  __ ___   ___                  ___      _         _             
     | \| |  \/  / __| / __| __ ___ _____   | _ \__ _| |_  __ _| |_  ___ _ _  
     | .` | |\/| \__ \ \__ \/ _` \ V / -_)  |  _/ _` |  _|/ _| ' \/ -_) '_| 
     |_|\_|_|  |_|___/ |___/\__,_|\_/\___|  |_| \__,_|\__|\__|_||_\___|_|   
    """
    print(banner)
    print("=" * 72)
    print("No Man's Sky Save Patcher".center(72))
    print("=" * 72)
    
    if current_version is not None:
        print(f"\n[+] Versión actual detectada en la partida: {current_version}")
    else:
        print("\n[!] No se pudo detectar la versión actual automáticamente.")

    prompt = "Inserta la versión del juego a la que quieras bajar/cambiar: "
    while True:
        try:
            version_solicitada = int(input(prompt).strip())
            return version_solicitada
        except ValueError:
            print("[!] Por favor, introduce un número entero válido.")


def main():
    save_input_path = "save.hg"
    save_output_path = "save_modificado.hg"

    # 1. Lee el archivo binario original de Steam
    try:
        with open(save_input_path, "rb") as f:
            input_bytes = f.read()
    except FileNotFoundError:
        print(f"[ERROR] No se encontró el archivo '{save_input_path}' en el directorio actual.")
        return

    # 2. Inspecciona la versión actual antes de pedir el cambio
    json_text = decompress_save_bytes(input_bytes)
    current_ver = get_save_version(json_text)

    # 3. Solicita la nueva versión por consola
    target_version = cli_user_interaction(current_ver)

    print(f"\n[1/2] Procesando {save_input_path} hacia versión {target_version}...")

    # 4. Ejecuta todo el pipeline a través del engine
    fixed_bytes, report = process_save_file(input_bytes, target_version)

    print(f"[OK] {report}")

    # 5. Guarda el nuevo archivo binario listo para la consola
    with open(save_output_path, "wb") as f:
        f.write(fixed_bytes)

    print(f"[2/2] Archivo '{save_output_path}' generado con éxito.")


if __name__ == "__main__":
    main()