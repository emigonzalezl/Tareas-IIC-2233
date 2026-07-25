import json
import socket
from PyQt5.QtCore import QThread, pyqtSignal


class ClienteNetworking(QThread):

    senal_error_conexion = pyqtSignal(str)

    senal_respuesta_login = pyqtSignal(bool, str, str, int, list)

    senal_actualizar_saldo = pyqtSignal(int)
    senal_actualizar_historial = pyqtSignal(list)

    def __init__(self, host: str, puerto: int, parent=None):
        super().__init__(parent)
        self.host = host
        self.puerto = puerto
        self.socket = None
        self.chunk_size = 2 ** 16
        self.conectado = False

    def conectar(self):

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.puerto))
            self.conectado = True
            print(f"[CLIENTE] Conectado a {self.host}:{self.puerto}")
            return True
        except OSError as e:
            print("[CLIENTE] Error al conectar:", e)
            self.senal_error_conexion.emit("No se pudo conectar al servidor.")
            self.conectado = False
            return False

    def run(self):

        if not self.conectado or self.socket is None:
            return

        while True:
            try:
                largo_bytes = self.recibir_bytes(4)
                if not largo_bytes:
                    break

                largo = int.from_bytes(largo_bytes, "big")
                mensaje_bytes = self.recibir_bytes(largo)
                if not mensaje_bytes:
                    break

                data = json.loads(mensaje_bytes.decode("utf-8"))
                print(f"[CLIENTE] Recibido: {data}")
                self._procesar_mensaje(data)

            except (ConnectionError, OSError) as e:
                print("[CLIENTE] Error de conexión:", e)
                break

        self.conectado = False
        if self.socket is not None:
            try:
                self.socket.close()
            except OSError:
                pass

    def recibir_bytes(self, n: int) -> bytes:
        datos = bytearray()
        while len(datos) < n:
            parte = self.socket.recv(n - len(datos))
            if not parte:
                return b""
            datos.extend(parte)
        return bytes(datos)

    def enviar_mensaje(self, mensaje: dict):
        if not self.conectado or self.socket is None:
            return
        try:
            bytes_mensaje = json.dumps(mensaje).encode("utf-8")
            largo = len(bytes_mensaje).to_bytes(4, "big")
            self.socket.sendall(largo + bytes_mensaje)
            print(f"[CLIENTE] Enviado: {mensaje}")
        except (ConnectionError, OSError) as e:
            print("[CLIENTE] Error al enviar mensaje:", e)

    def enviar_login(self, nombre: str):
        mensaje = {
            "comando": "login",
            "data": {"nombre": nombre},
        }
        self.enviar_mensaje(mensaje)

    def enviar_cargar_dinero(self, nombre: str, monto: int):
        mensaje = {
            "comando": "cargar-dinero",
            "data": {"nombre": nombre, "monto": monto},
        }
        self.enviar_mensaje(mensaje)

    def _procesar_mensaje(self, mensaje: dict):
        comando = mensaje.get("comando", "")

        if comando == "login-ok":
            data = mensaje.get("data", {})
            nombre = data.get("nombre", "")
            saldo = data.get("saldo", 0)
            historial = data.get("historial", [])
            self.senal_respuesta_login.emit(True, "Login exitoso", nombre, saldo, historial)

        elif comando == "login-error":
            razon = mensaje.get("razon", "Login rechazado.")
            self.senal_respuesta_login.emit(False, razon, "", 0, [])

        elif comando == "actualizar-saldo":
            saldo = int(mensaje.get("data", 0))
            self.senal_actualizar_saldo.emit(saldo)

        elif comando == "actualizar-historial":
            historial = mensaje.get("data", [])
            self.senal_actualizar_historial.emit(historial)
