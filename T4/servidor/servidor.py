import json
from thread_cliente import ThreadCliente
import parametros as p
from typing import Dict, List


class Servidor:

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

        import socket
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.clientes: Dict[int, ThreadCliente] = {}
        self.nombres_conectados: set[str] = set()

        self.usuarios: Dict[str, Dict[str, int]] = self.cargar_usuarios()
        self.historial_global: List[str] = []

        self.id_correlativo = 0

    def cargar_usuarios(self):
        try:
            with open(p.RUTA_ARCHIVO_USUARIOS, "r", encoding="utf-8") as f:
                data = json.load(f)
            print("[SERVIDOR] Usuarios cargados:", list(data.keys()))
            return data
        except (FileNotFoundError, json.JSONDecodeError):
            print("[SERVIDOR] No se pudo leer usuarios.json, se usara diccionario vacio.")
            return {}

    def guardar_usuarios(self):
        try:
            with open(p.RUTA_ARCHIVO_USUARIOS, "w", encoding="utf-8") as f:
                json.dump(self.usuarios, f, indent=4, ensure_ascii=False)
        except OSError as e:
            print("[SERVIDOR] Error al guardar usuarios:", e)

    def bind_listen(self):
        self.socket_server.bind((self.host, self.port))
        self.socket_server.listen()
        print(f"[SERVIDOR] Escuchando en {self.host}:{self.port}")

    def aceptar_conexiones(self):
        while True:
            try:
                socket_cliente, address = self.socket_server.accept()
            except OSError:
                break

            print(f"[SERVIDOR] Nuevo cliente desde {address}")

            id_cliente = self.id_correlativo
            self.id_correlativo += 1

            thread = ThreadCliente(id_cliente, socket_cliente, self)
            self.clientes[id_cliente] = thread
            thread.start()

    def manejar_login(self, nombre: str, id_cliente: int):
        print(f"[SERVIDOR] Login solicitado por '{nombre}' (cliente {id_cliente})")

        if nombre in self.nombres_conectados:
            razon = "El nombre ya está siendo usado."
            return False, {"razon": razon}

        if nombre not in self.usuarios:
            self.usuarios[nombre] = {"saldo": p.SALDO_INICIAL}
            self.guardar_usuarios()
            print(f"[SERVIDOR] Usuario nuevo: {nombre}")

        saldo = self.usuarios[nombre]["saldo"]
        self.nombres_conectados.add(nombre)

        data = {
            "nombre": nombre,
            "saldo": saldo,
            "historial": self.historial_global[-p.MAX_HISTORIAL:],
        }
        return True, data

    def avisar_desconexion(self, id_cliente: int, nombre: str | None):
        print(f"[SERVIDOR] Cliente {id_cliente} desconectado.")
        self.clientes.pop(id_cliente, None)
        if nombre and nombre in self.nombres_conectados:
            self.nombres_conectados.remove(nombre)

    def actualizar_saldo(self, nombre: str, saldo: int):
        if nombre in self.usuarios:
            self.usuarios[nombre]["saldo"] = saldo
            self.guardar_usuarios()

    def agregar_registro_historial(self, texto: str):
        self.historial_global.append(texto)

    def procesar_cargar_dinero(self, nombre: str, monto: int):
        if nombre not in self.usuarios:
            self.usuarios[nombre] = {"saldo": p.SALDO_INICIAL}
        saldo_actual = self.usuarios[nombre]["saldo"]
        nuevo_saldo = saldo_actual + max(monto, 0)
        self.usuarios[nombre]["saldo"] = nuevo_saldo
        self.guardar_usuarios()
        texto = f"{nombre} cargó ${monto}. Nuevo saldo: ${nuevo_saldo}."
        self.agregar_registro_historial(texto)

        historial = self.historial_global[-p.MAX_HISTORIAL:]
        return nuevo_saldo, historial
