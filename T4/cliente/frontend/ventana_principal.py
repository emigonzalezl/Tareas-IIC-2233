from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QTextEdit,
    QVBoxLayout, QHBoxLayout, QGroupBox
)

import parametros as p


class VentanaPrincipal(QWidget):

    senal_ir_blackjack = pyqtSignal()
    senal_ir_aviator = pyqtSignal()
    senal_ir_ruleta = pyqtSignal()
    senal_cargar_dinero = pyqtSignal()
    senal_salir_casino = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.nombre_jugador = ""
        self.saldo_actual = 0
        self.init_gui()

    def init_gui(self):
        self.setWindowTitle(p.TITULO_VENTANA_PRINCIPAL)
        self.setGeometry(200, 200, p.ANCHO_VENTANA_PRINCIPAL, p.ALTO_VENTANA_PRINCIPAL)

        self.label_nombre = QLabel("Jugador: -")
        self.label_saldo = QLabel("Saldo: $0")

        box_usuario = QGroupBox("Jugador")
        layout_usuario = QVBoxLayout()
        layout_usuario.addWidget(self.label_nombre)
        layout_usuario.addWidget(self.label_saldo)
        box_usuario.setLayout(layout_usuario)

        self.text_historial = QTextEdit()
        self.text_historial.setReadOnly(True)
        self.text_historial.setText(p.TEXTO_HISTORIAL_VACIO)

        box_historial = QGroupBox("Historial global")
        layout_historial = QVBoxLayout()
        layout_historial.addWidget(self.text_historial)
        box_historial.setLayout(layout_historial)

        self.boton_blackjack = QPushButton(p.TEXTO_BOTON_BLACKJACK)
        self.boton_aviator = QPushButton(p.TEXTO_BOTON_AVIATOR)
        self.boton_ruleta = QPushButton(p.TEXTO_BOTON_RULETA)

        layout_juegos = QHBoxLayout()
        layout_juegos.addWidget(self.boton_blackjack)
        layout_juegos.addWidget(self.boton_aviator)
        layout_juegos.addWidget(self.boton_ruleta)

        box_juegos = QGroupBox("Juegos")
        box_juegos.setLayout(layout_juegos)

        self.boton_cargar = QPushButton(p.TEXTO_BOTON_CARGAR)
        self.boton_salir = QPushButton(p.TEXTO_BOTON_SALIR)

        layout_inferior = QHBoxLayout()
        layout_inferior.addWidget(self.boton_cargar)
        layout_inferior.addStretch()
        layout_inferior.addWidget(self.boton_salir)

        layout_principal = QVBoxLayout()
        layout_principal.addWidget(box_usuario)
        layout_principal.addWidget(box_juegos)
        layout_principal.addWidget(box_historial)
        layout_principal.addStretch()
        layout_principal.addLayout(layout_inferior)

        self.setLayout(layout_principal)

        self.boton_blackjack.clicked.connect(self.senal_ir_blackjack)
        self.boton_aviator.clicked.connect(self.senal_ir_aviator)
        self.boton_ruleta.clicked.connect(self.senal_ir_ruleta)
        self.boton_cargar.clicked.connect(self.senal_cargar_dinero)
        self.boton_salir.clicked.connect(self.senal_salir_casino)

    def configurar_usuario(self, nombre: str, saldo: int):
        self.nombre_jugador = nombre
        self.saldo_actual = saldo
        self.actualizar_texto_jg()

    def actualizar_saldo(self, saldo: int):
        self.saldo_actual = saldo
        self.actualizar_texto_jg()

    def actualizar_texto_jg(self):
        self.label_nombre.setText(f"Jugador: {self.nombre_jugador}")
        self.label_saldo.setText(f"Saldo: ${self.saldo_actual}")

    def actualizar_historial(self, registros):
        registros = list(registros)
        if not registros:
            self.text_historial.setText(p.TEXTO_HISTORIAL_VACIO)
        else:
            self.text_historial.setText("\n".join(registros))
