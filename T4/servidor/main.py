import json
import sys
from servidor import Servidor


def cargar_configuracion():
    with open("conexion.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["host"], data["puerto"]


if __name__ == "__main__":
    host, puerto = cargar_configuracion()

    if len(sys.argv) >= 2:
        puerto = int(sys.argv[1])
    if len(sys.argv) >= 3:
        host = sys.argv[2]

    server = Servidor(host, puerto)
    server.bind_listen()

    print("[SERVIDOR] Presione Ctrl+C para detener el servidor.")
    try:
        server.aceptar_conexiones()
    except KeyboardInterrupt:
        print("\n[SERVIDOR] Cerrando servidor...")
        try:
            server.socket_server.close()
        except OSError:
            pass
