import json
import threading
from socket import socket

from parametros import MAX_HISTORIAL


class ThreadCliente(threading.Thread):

    def __init__(self, id_cliente: int, socket_cliente: socket, servidor):
        super().__init__(daemon=True)
        self.id_cliente = id_cliente
        self.socket = socket_cliente
        self.servidor = servidor
        self.chunk_size = 2 ** 16
        self.nombre = None

    def recibir_bytes(self, n: int) -> bytes:
        datos = bytearray()
        while len(datos) < n:
            parte = self.socket.recv(n - len(datos))
            if not parte:
                return b""
            datos.extend(parte)
        return bytes(datos)

    def _enviar_mensaje(self, mensaje: dict):
        try:
            bytes_mensaje = json.dumps(mensaje).encode("utf-8")
            largo = len(bytes_mensaje).to_bytes(4, "big")
            self.socket.sendall(largo + bytes_mensaje)
            print(f"[Cliente {self.id_cliente}] Enviando: {mensaje}")
        except OSError as e:
            print(f"[Cliente {self.id_cliente}] Error al enviar:", e)

    def run(self):
        print(f"[Cliente {self.id_cliente}] Hilo iniciado.")
        while True:
            try:
                largo_bytes = self.recibir_bytes(4)
                if not largo_bytes:
                    break
                largo = int.from_bytes(largo_bytes, "big")
                if largo == 0:
                    break
                mensaje_bytes = self.recibir_bytes(largo)
                if not mensaje_bytes:
                    break
                mensaje = json.loads(mensaje_bytes.decode("utf-8"))
                print(f"[Cliente {self.id_cliente}] Recibido: {mensaje}")
                self._procesar_mensaje(mensaje)
            except (ConnectionError, OSError, json.JSONDecodeError) as e:
                print(f"[Cliente {self.id_cliente}] Error:", e)
                break

        try:
            self.socket.close()
        except OSError:
            pass
        self.servidor.avisar_desconexion(self.id_cliente, self.nombre)

    def _procesar_mensaje(self, mensaje: dict):
        comando = mensaje.get("comando", "")

        if comando == "login":
            self._procesar_login(mensaje)
        elif comando == "cargar-dinero":
            self._procesar_cargar_dinero(mensaje)
        else:
            print(f"[Cliente {self.id_cliente}] Comando desconocido: {comando}")

    def _procesar_login(self, mensaje: dict):
        data = mensaje.get("data", {})
        nombre = data.get("nombre", "").strip()

        if not nombre:
            resp = {"comando": "login-error", "razon": "Nombre vacío."}
            self._enviar_mensaje(resp)
            return

        resultado_login = self.servidor.manejar_login(nombre, self.id_cliente)
        ok = resultado_login[0]
        respuesta = resultado_login[1]

        if not ok:
            resp = {"comando": "login-error", "razon": respuesta.get("razon", "")}
            self._enviar_mensaje(resp)
            return

        self.nombre = respuesta["nombre"]
        saldo = respuesta["saldo"]
        historial = respuesta["historial"][-MAX_HISTORIAL:]

        resp = {
            "comando": "login-ok",
            "data": {
                "nombre": self.nombre,
                "saldo": saldo,
                "historial": historial,
            },
        }
        self._enviar_mensaje(resp)

    def _procesar_cargar_dinero(self, mensaje: dict):
        data = mensaje.get("data", {})
        nombre_msg = data.get("nombre", "").strip()
        monto = int(data.get("monto", 0))

        nombre = nombre_msg or self.nombre

        if not nombre or monto <= 0:
            print(f"[Cliente {self.id_cliente}] cargar-dinero inválido: {mensaje}")
            return

        nuevo_saldo, historial = self.servidor.procesar_cargar_dinero(nombre, monto)

        resp_saldo = {"comando": "actualizar-saldo", "data": nuevo_saldo}
        self._enviar_mensaje(resp_saldo)

        resp_historial = {"comando": "actualizar-historial", "data": historial}
        self._enviar_mensaje(resp_historial)
