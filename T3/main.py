import sys
import os
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
                             QLineEdit, QScrollArea, QMessageBox)
from backend.consultas import (cargar_astronautas, cargar_naves, cargar_tripulaciones,
                               cargar_planetas, cargar_minerales, cargar_mision,
                               cargar_planeta_minerales, cargar_materiales_mision)


class VentanaEntrada(QWidget):

    senal_ir_a_principal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("DCCosmos — Ventana Entrada")
        self.init_gui()

    def init_gui(self):

        mensaje = QLabel("¡Bienvenid@!\n\nPresiona el botón para ir a la ventana principal.")
        self.boton = QPushButton("Ir a Ventana Principal")

        vbox = QVBoxLayout(self)
        vbox.addStretch(1)
        vbox.addWidget(mensaje)
        vbox.addWidget(self.boton)
        vbox.addStretch(1)

        self.boton.clicked.connect(self.abrir_principal)

    def abrir_principal(self):
        self.hide()
        self.senal_ir_a_principal.emit()


class VentanaPrincipal(QWidget):

    senal_ir_a_mapa = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("DCCosmos — Ventana Principal")
        self.init_gui()

    def init_gui(self):

        self.setWindowTitle("Ventana Principal")
        mensaje = QLabel("QFileDialog: Escribe la ruta de un archivo.")
        self.archivo = QLineEdit("", self)
        self.archivo.setPlaceholderText("Ej: data/out_S")
        boton_buscar = QPushButton("Buscar")
        boton_buscar.clicked.connect(self.buscar_archivo)

        self.ruta_valida = QLabel("¡Ruta Valida!")
        self.ruta_invalida = QLabel("¡Ruta Invalida!")

        # QFileDialog buscar archivo
        vbox = QVBoxLayout(self)
        vbox.addStretch(1)
        vbox.addWidget(mensaje)
        vbox.addWidget(self.archivo)
        vbox.addWidget(boton_buscar)
        vbox.addWidget(self.ruta_valida)
        vbox.addWidget(self.ruta_invalida)
        vbox.addStretch(1)

        self.ruta_valida.setVisible(False)
        self.ruta_invalida.setVisible(False)

        # Parte de input escondida hasta que se da ruta
        self.instruccion = QLabel(
            "Escribe la entidad a cargar y un filtro (opcional), sin espacios y separado por coma."
            )
        self.filtro_input = QLineEdit()
        self.filtro_input.setPlaceholderText("Ej1: Mineral,id_mineral=1      Ej2: Astronauta")
        self.boton_filtrar = QPushButton("Ejecutar Consulta")
        self.boton_filtrar.clicked.connect(self.filtrar_archivo)

        vbox.addWidget(self.instruccion)
        vbox.addWidget(self.filtro_input)
        vbox.addWidget(self.boton_filtrar)

        self.contenedor = QWidget()
        self.contenedor_l = QVBoxLayout(self.contenedor)

        # Scroll vertical muestra consultas
        scroll = QScrollArea()
        scroll.setWidget(self.contenedor)
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        vbox.addStretch(1)
        titulo = QLabel("Archivos disponibles en la carpeta data:")
        vbox.addWidget(titulo)
        vbox.addWidget(scroll)
        vbox.addStretch(1)

        self.boton_mapa = QPushButton("Ir a Ventana Mapa")  # CAMBIO
        self.boton_mapa.clicked.connect(self.abrir_mapa)     # CAMBIO
        vbox.addWidget(self.boton_mapa)

    def buscar_archivo(self):
        ruta = self.archivo.text()
        if os.path.exists(ruta):
            self.ruta_valida.setVisible(True)
            self.ruta_invalida.setVisible(False)
        else:
            QMessageBox.warning(self, "Archivo no encontrado",
                                f"No se encontró el archivo:\n{ruta}.")
            self.ruta_invalida.setVisible(True)
            self.ruta_valida.setVisible(False)
    """
    Info sobre QMessageBox sacada de:
    https://stackoverflow.com/questions/11204733/qmessagebox-warning-yellow-exclamation-mark-icon
    """
    def filtrar_archivo(self):
        ruta = self.archivo.text()
        filtro = self.filtro_input.text()

        if os.path.exists(ruta):
            elementos = []
            if filtro:
                partes_tmp = filtro.split(",")
                for p in partes_tmp:
                    if p != "":
                        elementos.append(p)

            if len(elementos) == 0:
                QMessageBox.warning(self, "Entrada inválida",
                                    "Debes escribir al menos la entidad.")
                return

            filtrados = self.hacer_consulta(elementos)
            while self.contenedor_l.count():
                item = self.contenedor_l.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
            if not filtrados:
                self.contenedor_l.addWidget(QLabel("Sin resultados."))
            else:
                for e in filtrados:
                    self.contenedor_l.addWidget(QLabel(str(e)))

        # deleteLater para ir borrando los widgets sacado de:
        # https://www.geeksforgeeks.org/python/deletelater-method-in-pyqt5/

        else:
            QMessageBox.warning(self, "Archivo no encontrado",
                                f"No se encontró el archivo:\n{ruta}. Revisa el filtro o ruta.")
            self.ruta_invalida.setVisible(True)
            self.ruta_valida.setVisible(False)
            return

    # Asumo que solo se revisa de a una entidad y que esta es el primer objeto dado.
    def hacer_consulta(self, lista):

        dict = {"Astronauta": cargar_astronautas, "Mineral": cargar_minerales,
                "Mision": cargar_mision, "MisionMineral": cargar_materiales_mision,
                "Nave": cargar_naves, "Planeta": cargar_planetas,
                "PlanetaMineral": cargar_planeta_minerales, "Tripulacion": cargar_tripulaciones}

        entidad = lista[0]
        funcion = dict.get(entidad, None)
        filtrados = []

        if funcion is None:
            QMessageBox.warning(self, "Entidad no válida",
                                f"La entidad '{entidad}' no existe.")
            return []

        base = self.archivo.text()
        ruta_csv = os.path.join(base, f"{entidad}.csv")
        if os.path.isdir(base) and os.path.exists(ruta_csv):
            origen_path = ruta_csv
        else:
            QMessageBox.warning(self, "Archivo no encontrado")
            return []
        lista_elementos = list(funcion(origen_path))
        if len(lista) == 1:
            filtrados = lista_elementos
        else:
            for f in lista[1:]:
                partes = f.split("=")
                propiedad = partes[0]
                valor = partes[1]
                if len(filtrados) == 0:
                    origen = lista_elementos
                else:
                    origen = filtrados
                nuevo_filtrado = []
                for ent in origen:
                    texto = str(ent)
                    if propiedad in texto and valor in texto:
                        nuevo_filtrado.append(ent)

                filtrados = nuevo_filtrado

        return filtrados

    def abrir_mapa(self):
        self.senal_ir_a_mapa.emit()


class VentanaMapa(QWidget):
    senal_ir_a_principal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("DCCosmos — Ventana Mapa")
        self.init_gui()

    def init_gui(self):
        v = QVBoxLayout(self)
        v.addStretch(1)
        v.addWidget(QLabel("Ventana Mapa"))
        self.boton_principal = QPushButton("Volver a Ventana Principal")
        v.addWidget(self.boton_principal)
        v.addStretch(1)
        self.boton_principal.clicked.connect(self.volver_a_principal)

    def volver_a_principal(self):
        self.hide()
        self.senal_ir_a_principal.emit()


if __name__ == '__main__':
    def hook(type, value, traceback) -> None:
        print(type)
        print(traceback)

    sys.__excepthook__ = hook

    app = QApplication([])
    ventana_entrada = VentanaEntrada()
    ventana_principal = VentanaPrincipal()
    ventana_mapa = VentanaMapa()

    ventana_entrada.senal_ir_a_principal.connect(ventana_principal.show)
    ventana_principal.senal_ir_a_mapa.connect(ventana_mapa.show)
    ventana_mapa.senal_ir_a_principal.connect(ventana_principal.show)

    ventana_entrada.show()
    sys.exit(app.exec_())
