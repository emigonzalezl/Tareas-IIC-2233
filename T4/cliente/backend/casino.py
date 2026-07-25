from typing import List
from PyQt5.QtCore import QObject, pyqtSignal
from backend.networking import ClienteNetworking
import parametros as p


class Casino(QObject):

    senal_mensaje_inicio = pyqtSignal(str, bool)
    senal_login_exitoso = pyqtSignal(str, int, list)
    senal_login_fallido = pyqtSignal(str)
    senal_actualizar_saldo = pyqtSignal(int)
    senal_actualizar_historial = pyqtSignal(list)
    senal_cerrar_aplicacion = pyqtSignal()

    def __init__(self, host: str, puerto: int):
        super().__init__()

        self.nombre_jugador = ""
        self.saldo = 0
        self.historial: List[str] = []

        self.cliente = ClienteNetworking(host, puerto)
        self._conectar_senales_networking()

        self.conectado = self.cliente.conectar()
        if self.conectado:
            self.cliente.start()

    def _conectar_senales_networking(self):
        self.cliente.senal_error_conexion.connect(self._error_conexion)
        self.cliente.senal_respuesta_login.connect(self._respuesta_login)
        self.cliente.senal_actualizar_saldo.connect(self._actualizar_saldo_desde_server)
        self.cliente.senal_actualizar_historial.connect(
            self._actualizar_historial_desde_server
        )

    def intentar_login(self, nombre: str):
        if not self.conectado:
            self.senal_mensaje_inicio.emit(p.MENSAJE_ERROR_CONEXION, True)
            return

        self.nombre_jugador = nombre
        self.cliente.enviar_login(nombre)

    def _error_conexion(self, mensaje: str):
        self.senal_mensaje_inicio.emit(mensaje, True)

    def _respuesta_login(self, ok: bool, mensaje: str, nombre: str, saldo: int, historial: list):
        if not ok:
            self.senal_login_fallido.emit(mensaje)
            self.senal_mensaje_inicio.emit(mensaje, True)
            return

        self.nombre_jugador = nombre
        self.saldo = saldo
        self.historial = historial

        self.senal_mensaje_inicio.emit(mensaje, False)
        self.senal_login_exitoso.emit(nombre, saldo, historial)

    def _actualizar_saldo_desde_server(self, saldo: int):
        self.saldo = saldo
        self.senal_actualizar_saldo.emit(saldo)

    def _actualizar_historial_desde_server(self, historial: list):
        self.historial = historial
        self.senal_actualizar_historial.emit(historial)

    def cargar_dinero(self, monto: int):
        if monto <= 0:
            return
        self.cliente.enviar_cargar_dinero(self.nombre_jugador, monto)

    # No se alcanzaron a implementar los juegos
    def ir_a_blackjack(self):
        print("[BACKEND] Ir a Blackjack (no implementado).")

    def ir_a_aviator(self):
        print("[BACKEND] Ir a Aviator (no implementado).")

    def ir_a_ruleta(self):
        print("[BACKEND] Ir a Ruleta (no implementado).")

    def salir_casino(self):
        self.senal_cerrar_aplicacion.emit()
