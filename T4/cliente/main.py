from PyQt5.QtWidgets import QApplication, QInputDialog
from frontend.ventana_inicio import VentanaInicio
from frontend.ventana_principal import VentanaPrincipal
from backend.casino import Casino
import json
import sys


def cargar_configuracion() -> tuple[str, int]:

    with open("conexion.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    host = data["host"]
    puerto = data["puerto"]
    return host, puerto


class DCCasinoApp:

    def __init__(self):
        host, puerto = cargar_configuracion()

        self.ventana_inicio = VentanaInicio()
        self.ventana_principal = VentanaPrincipal()
        self.backend = Casino(host, puerto)

        self._conectar_senales()

    def _conectar_senales(self):

        self.ventana_inicio.senal_intentar_login.connect(self.backend.intentar_login)

        self.backend.senal_mensaje_inicio.connect(self._mostrar_mensaje_inicio)
        self.backend.senal_login_exitoso.connect(self._login_exitoso)
        self.backend.senal_login_fallido.connect(lambda _: None)
        self.backend.senal_actualizar_saldo.connect(self.ventana_principal.actualizar_saldo)
        self.backend.senal_actualizar_historial.connect(
            self.ventana_principal.actualizar_historial
        )
        self.ventana_principal.senal_cargar_dinero.connect(self._manejar_cargar_dinero)
        self.ventana_principal.senal_ir_blackjack.connect(self.backend.ir_a_blackjack)
        self.ventana_principal.senal_ir_aviator.connect(self.backend.ir_a_aviator)
        self.ventana_principal.senal_ir_ruleta.connect(self.backend.ir_a_ruleta)
        self.ventana_principal.senal_salir_casino.connect(self.backend.salir_casino)

        self.backend.senal_cerrar_aplicacion.connect(self._cerrar_todo)

    def _mostrar_mensaje_inicio(self, texto: str, es_error: bool):
        self.ventana_inicio.mostrar_mensaje(texto, es_error)

    def _login_exitoso(self, nombre: str, saldo: int, historial: list):
        self.ventana_principal.configurar_usuario(nombre, saldo)
        self.ventana_principal.actualizar_historial(historial)
        self.ventana_inicio.hide()
        self.ventana_principal.show()

    def _manejar_cargar_dinero(self):
        monto, ok = QInputDialog.getInt(
            self.ventana_principal,
            "Cargar dinero",
            "Ingresa el monto:",
            value=1000,
            min=1,
        )
        if not ok:
            return
        self.backend.cargar_dinero(monto)

    def _cerrar_todo(self):
        self.ventana_inicio.close()
        self.ventana_principal.close()

    def iniciar(self):
        self.ventana_inicio.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    dccasino_app = DCCasinoApp()
    dccasino_app.iniciar()

    sys.exit(app.exec_())
