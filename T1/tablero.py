from visualizador import imprimir_tablero


class Tablero:

    def __init__(self) -> None:
        self.tablero = []
        self.movimientos = 0
        self.estado = False  # bool de estado: resuelto o no

# Asumo que el archivo termina en txt
    def cargar_tablero(self, archivo: str):

        self.tablero = []
        with open(f"config/{archivo}") as f:
            coords = f.readline()
            coords = coords.strip()
            coords = coords.split(" ")

            for i in range(int(coords[0])+1):
                fila = f.readline()
                fila = fila.strip()
                fila = fila.split(" ")
                self.tablero.append(fila)
    # Los carga como str

    # Asumo que el tablero es valido
    def mostrar_tablero(self):
        imprimir_tablero(self.tablero)  # cambiar sos ??

    # Modifica correctamente la casilla del tablero actual.
    # Asumo que a la función se le dara un parametro de fila y columna.
    def modificar_casilla(self, fila, columna):

        max_ind_fil = len(self.tablero)-2
        max_ind_col = len(self.tablero[0])-2

        if fila == len(self.tablero)-1 or columna == len(self.tablero[0])-1:
            return False

        # En caso de que fila y columna sean ints
        if type(fila) is int and type(columna) is int:

            if 0 <= fila <= max_ind_fil and 0 <= columna <= max_ind_col:

                casilla = self.tablero[fila][columna]
                ult_fil = len(self.tablero)-1
                ult_col = len(self.tablero[0])-1

                if fila == ult_fil or columna == ult_col:
                    return False

                elif casilla == ".":
                    return False
                elif casilla.isdigit() is False and casilla != ".":
                    casilla = list(casilla)
                    self.tablero[fila][columna] = "".join(casilla[1:])
                    self.movimientos += 1
                    return True
                else:
                    num = casilla
                    self.tablero[fila][columna] = f"X{num}"
                    self.movimientos += 1
                    return True

            else:
                return False

        # En caso de que fila y columna sean strings
        elif type(fila) is str and type(columna) is str:
            if fila.isdigit() and columna.isdigit():

                fila = int(fila)
                columna = int(columna)

                if 0 <= fila <= max_ind_fil and 0 <= columna <= max_ind_col:
                    casilla = self.tablero[fila][columna]
                    ult_fil = len(self.tablero)-1
                    ult_col = len(self.tablero[0])-1

                    if fila == ult_fil or columna == ult_col:
                        return False
                    elif casilla == ".":
                        return False
                    elif casilla.isdigit() is False and casilla != ".":
                        casilla = list(casilla)
                        self.tablero[fila][columna] = "".join(casilla[1:])
                        self.movimientos += 1
                        return True
                    else:
                        num = casilla
                        self.tablero[fila][columna] = f"X{num}"
                        self.movimientos += 1
                        return True
                else:
                    return False
            else:
                return False
        else:
            return False

    # Devuelve True si es que el estado actual es solución.
    def validar(self):

        # Validar filas
        for i in range(len(self.tablero)-1):  # Por cada fila
            fila = 0
            for k in range(len(self.tablero[0])-1):  # Por cada col
                if self.tablero[i][k] != "." and "X" not in self.tablero[i][k]:
                    fila += int(self.tablero[i][k])

            if self.tablero[i][-1] == ".":
                continue
            elif fila == int(self.tablero[i][-1]):
                continue
            elif fila != int(self.tablero[i][-1]):
                self.estado = False
                return False
        # Validar columnas
        for k in range(len(self.tablero[0])-1):
            columna = 0
            for i in range(len(self.tablero)-1):
                if self.tablero[i][k] != "." and "X" not in self.tablero[i][k]:
                    columna += int(self.tablero[i][k])

            if self.tablero[-1][k] == ".":
                continue
            elif columna == int(self.tablero[-1][k]):
                continue
            elif columna != int(self.tablero[-1][k]):
                self.estado = False
                return False

        self.estado = True
        return True

    def encontrar_solucion(self):

        # No logrado a tiempo :(

        return None
