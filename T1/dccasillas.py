from tablero import Tablero
import os
# Info de como usar os sacada de:
# https://www.freecodecamp.org/news/how-to-check-if-a-file-exists-in-python/


class DCCasillas:

    def __init__(self, usuario: str, config: str) -> None:
        self.usuario = usuario
        self.config = config
        self.puntaje = 0
        self.tablero_actual = None
        self.tableros = []  # instancias de tablero
        self.archivos = []  # archivos
        self.resueltos = []  # para el ptje

        with open(f"config/{self.config}") as f:

            n_tableros = f.readline()
            n_tableros = n_tableros.strip()

            for i in range(int(n_tableros)):
                linea = f.readline()
                linea = linea.strip()
                self.archivos.append(linea)
                tablero = Tablero()
                tablero.cargar_tablero(linea)
                self.tableros.append(tablero)

            self.tablero_actual = 0

    # Asumo que el tablero actual es valido y que se entregara un int.
    # Su principal funcion es usar visualizador. Comprueba que tablero exista.
    def abrir_tablero(self, num_tablero: int):
        if 0 <= num_tablero <= len(self.tableros)-1:
            self.tablero_actual = num_tablero

    # Guarda correctamente el estado
    def guardar_estado(self) -> bool:

        # Aqui se usa os para verificar que el archivo exista.
        # De lo contrario devuelve False.
        config_existe = os.path.exists(f"config/{self.config}")
        hay_tableros = len(self.tableros)

        # Verifica que el usuario existe, es decir que no sea un str vacio
        # y que haya al menos un tablero para guardar. Si no devuelve False.
        if self.usuario != "" and config_existe is True and hay_tableros >= 1:

            with open(f"data/{self.usuario}.txt", "w") as f:
                f.write(f"{len(self.tableros)}\n")

                for i in range(len(self.tableros)):
                    f.write(f"{self.tableros[i].movimientos}\n")
                    f.write(f"{len(self.tableros[i].tablero)-1} "
                            f"{len(self.tableros[i].tablero[0])-1}\n")
                    for j in range(len(self.tableros[i].tablero)):
                        for k in range(len(self.tableros[i].tablero[0])):
                            f.write(f"{self.tableros[i].tablero[j][k]} ")
                        f.write("\n")

            return True

        else:
            return False

    # Recupera correctamente el estado de un usuario si existe su archivo.
    def recuperar_estado(self) -> bool:

        archivo_existe = os.path.exists(f"data/{self.usuario}.txt")

        # Aqui se usa os para verificar que el archivo exista.
        # De lo contrario devuelve False.
        if archivo_existe is True and self.usuario != "":

            with open(f"data/{self.usuario}.txt") as f:

                n_tableros = f.readline()
                n_tableros = n_tableros.strip()

                if n_tableros.isdigit() is False:
                    return False

                for i in range(int(n_tableros)):  # para cada tablero

                    movs = f.readline()
                    movs = movs.strip()
                    tamaño = f.readline()
                    tamaño = tamaño.strip()
                    tamaño = tamaño.split()
                    n_filas = int(tamaño[0])

                    tablero = []
                    for j in range(n_filas+1):
                        fila = f.readline()
                        fila = fila.strip()
                        fila = fila.split(" ")
                        tablero.append(fila)

                    # Revisar validez:
                    letras = ["abcdefghijklmnopqrstuvwyz"]

                    for j in range(len(tablero)):
                        for k in range(len(tablero[0])):
                            casilla = tablero[j][k]
                            if "-" in casilla:
                                return False
                            if casilla.isdigit() is False:
                                for letra in casilla:
                                    if letra in letras:
                                        return False

                    self.tableros[i].movimientos = int(movs)
                    self.tableros[i].tablero = tablero
                    self.tableros[i].validar()
            return True

        else:
            return False

        # Recupera archivo nom usuario y txt. Si se recupera true si no false
