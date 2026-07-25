from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout
)

import parametros as p


class VentanaInicio(QWidget):

    senal_intentar_login = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.init_gui()

    def init_gui(self):
        self.setWindowTitle(p.TITULO_PROGRAMA)
        self.setGeometry(300, 300, p.ANCHO_VENTANA_INICIO, p.ALTO_VENTANA_INICIO)

        self.label_titulo = QLabel(p.TITULO_PROGRAMA)
        self.label_nombre = QLabel("Nombre:")
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Ingresa tu nombre de jugador")

        self.boton_ingresar = QPushButton("Ingresar")
        self.label_estado = QLabel("")

        layout_nombre = QHBoxLayout()
        layout_nombre.addWidget(self.label_nombre)
        layout_nombre.addWidget(self.input_nombre)

        layout_principal = QVBoxLayout()
        layout_principal.addWidget(self.label_titulo)
        layout_principal.addSpacing(10)
        layout_principal.addLayout(layout_nombre)
        layout_principal.addSpacing(10)
        layout_principal.addWidget(self.boton_ingresar)
        layout_principal.addSpacing(10)
        layout_principal.addWidget(self.label_estado)
        layout_principal.addStretch()

        self.setLayout(layout_principal)

        self.boton_ingresar.clicked.connect(self.ingresar)
        self.input_nombre.returnPressed.connect(self.ingresar)

    def ingresar(self):
        nombre = self.input_nombre.text().strip()

        if not nombre:
            self.mostrar_mensaje(p.MENSAJE_NOMBRE_VACIO, es_error=True)
            return

        self.mostrar_mensaje(p.MENSAJE_CONECTANDO, es_error=False)
        self.senal_intentar_login.emit(nombre)

    def mostrar_mensaje(self, texto: str, es_error: bool = True):
        if es_error:
            self.label_estado.setStyleSheet("color: red;")
        else:
            self.label_estado.setStyleSheet("color: green;")
        self.label_estado.setText(texto)
