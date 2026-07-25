from DCCartas import CartaTropa, CartaEstructura
from jugadores import IA
import random
import os


# Da al azar una seleccion inicial de carta. Obliga a elegir al menos 1
def selección_inicial(cartas):

    seleccion_azar = random.sample(cartas, 5)
    mazo = []

    print(f"""
    ---------------------------------
            SELECCIÓN INICIAL
    ---------------------------------\n
    [1] {seleccion_azar[0]}
    [2] {seleccion_azar[1]}
    [3] {seleccion_azar[2]}
    [4] {seleccion_azar[3]}
    [5] {seleccion_azar[4]}
    [6] Continuar al Menú Principal.\n\n

    Seleccione desde 1 a 5 cartas para su mazo:""")

    opciones = ["1", "2", "3", "4", "5"]

    while True:
        choice = input("\n--> ")
        if choice == "6":
            if len(mazo) < 1:
                print("\nDebe elegir al menos una carta para continuar.")
            else:
                print("\nContinuando al Menú principal...\n")
                return mazo
        elif choice in opciones and seleccion_azar[int(choice)-1] not in mazo:
            mazo.append(seleccion_azar[int(choice)-1])
            print(f"\nCarta '{seleccion_azar[int(choice)-1].nombre}' añadida exitosamente!")
            print(f"Mazo actual = {mazo}")
        elif choice in opciones and seleccion_azar[int(choice)-1] in mazo:
            print(f"\n La carta {seleccion_azar[int(choice)-1].nombre} ya se encuentra en tu mazo")
        else:
            print("\nIngrese una opción valida")


# Muestra y ejecuta el menu principal
def mostrar_menu_principal(jugador, ronda, ia):
    print(f"""\n
        -----------------------------
                MENÚ PRINCIPAL
        -----------------------------\n
        Dinero disponible: {jugador.dinero} G
        Ronda Actual: {ronda}
        IA enemiga: {ia.nombre} (vida: {ia.vida:.2f})\n
        [1] Entrar en combate
        [2] Inventario (gestionar mazo)
        [3] Tienda
        [4] Espiar a la IA
        [0] Salir del juego\n
        Indique su opción:""")

    opciones = ["0", "1", "2", "3", "4"]

    while True:
        choice = input("\n--> ")
        if choice not in opciones:
            print("\nIngrese una opción valida")
        elif choice in opciones:
            return choice


def coleccion(jugador):

    while True:

        ordenadas = []
        opciones_mazo = []
        i = 1
        print("""\n
        -----------------------------
                COLECCIÓN
        -----------------------------

        Cartas en Mazo actual:\n""")
        for carta in jugador.cartas:
            print(f"        [{i}] {carta}")
            opciones_mazo.append(f"{i}")
            ordenadas.append(carta)
            i += 1
        print("\n        Cartas en la colección:\n")

        opciones_coleccion = []
        for carta in jugador.coleccion:
            if carta not in jugador.cartas and carta.vida > 0:
                print(f"        [{i}] {carta}")
                opciones_coleccion.append(f"{i}")
                ordenadas.append(carta)
                i += 1

        print(f"\n        [{i}] Volver al menu principal\n")

        choice = input("\n--> ")

        while True:
            if choice in opciones_mazo:
                print("\nCarta seleccionada:")
                print(f"\n[{choice}] {ordenadas[int(choice)-1]}\n")
                print("\n[1] Quitar del mazo\n[2] Volver atras\n")

                while True:
                    choice_mazo = input("\n-->")
                    if choice_mazo == "1":
                        if len(jugador.cartas) > 1:
                            print(f"\n{ordenadas[int(choice)-1].nombre} fue quitada del mazo.")
                            jugador.cartas.remove(ordenadas[int(choice)-1])

                            print("cartas:", jugador.cartas)
                            print("coleccion:", jugador.coleccion)
                            opciones_mazo = ["1"]
                            opciones_coleccion = []
                            i = 1

                            break
                        else:
                            print("\nDebes tener al menos una carta en tu mazo actual")
                            print("La carta no ha sido quitada de tu mazo.")
                            break
                    elif choice_mazo == "2":
                        break
                    else:
                        print("\nPor favor ingrese una opción válida")
                        choice = input("\n--> ")
                break

            elif choice in opciones_coleccion:
                print("\nCarta seleccionada:")
                print(f"\n[{choice}] {ordenadas[int(choice)-1]}\n")
                print("\n[1] Agregar al mazo\n[2] Volver atras")
                choice_coleccion = input("\n-->")
                while True:
                    if choice_coleccion == "1":
                        if len(jugador.cartas) < 5:
                            jugador.cartas.append(ordenadas[int(choice)-1])
                            opciones_mazo = ["1"]
                            opciones_coleccion = []
                            i = 1
                            break
                        else:
                            print("\nNo puedes tener mas de 5 cartas a la vez."
                                  " Quita una para agregar otra.\n")
                            break

                    if choice_coleccion == "2":
                        break
                break

            elif choice == f"{i}":
                print("\nVolviendo al menu principal\n")
                return None

            else:
                print("ingrese una opción válida")
                choice = input("\n-->")


# Devuelve lista con cartas de estructura y tropa cargadas
def cargar_cartas(archivo_cartas):

    if os.path.exists(archivo_cartas):
        cartas = []
        with open(archivo_cartas) as f:

            # Ignoramos el header
            header = f.readline()
            linea = f.readline()

            while linea != "" and linea != "\n":
                # Se cargan las cartas a la lista
                linea = linea.strip()
                lista = []  # Aqui voy a armar el linea.split manual

                in_desc = False
                actual = ""

                for i in range(len(linea)):
                    if linea[i] == ',' and in_desc is False:
                        lista.append(actual)
                        actual = ""
                    elif linea[i] == '"' and in_desc is False:
                        in_desc = True
                    elif linea[i] == '"' and in_desc is True:
                        in_desc = False
                    else:
                        actual += linea[i]

                lista.append(actual)

                linea = lista

                if linea[1] == "tropa":
                    carta_tropa = CartaTropa(linea[0], linea[1], int(linea[2]), int(linea[2]),
                                             float(linea[3]), int(linea[4]), float(linea[5]),
                                             int(linea[6]), float(linea[7]), linea[8])

                    cartas.append(carta_tropa)

                if linea[1] == "estructura":
                    carta_estructura = CartaEstructura(linea[0], linea[1], int(linea[2]),
                                                       int(linea[2]), float(linea[3]),
                                                       int(linea[4]), float(linea[5]), linea[8])
                    cartas.append(carta_estructura)

                linea = f.readline()

        return cartas


#  Devuelve las cartas si el archivo existe
def cargar_IAs(archivo_ia, archivo_mult):

    if os.path.exists(archivo_ia) and os.path.exists(archivo_mult):

        ias = []

        with open(archivo_ia) as f:
            head = f.readline()  # header nom, vidmax, atq, des, prob, vel
            linea = f.readline()

            while linea != "" and linea != "\n":

                linea = linea.strip()
                lista = []  # Aqui voy a armar el linea.split manual

                in_desc = False
                actual = ""

                for i in range(len(linea)):
                    if linea[i] == ',' and in_desc is False:
                        lista.append(actual)
                        actual = ""
                    elif linea[i] == '"' and in_desc is False:
                        in_desc = True
                    elif linea[i] == '"' and in_desc is True:
                        in_desc = False
                    else:
                        actual += linea[i]

                lista.append(actual)

                linea = lista
                ia = IA(linea[0], int(linea[1]), int(linea[2]), float(linea[4]),
                        float(linea[5]), linea[3])
                ias.append(ia)

                linea = f.readline()

            for ia_actual in ias:
                # por cada ia sacar sus multiplicadores
                with open(archivo_mult) as s:
                    linea = s.readline()  # header
                    linea = s.readline()

                    while linea != "" and linea != "\n":
                        linea = linea.strip()
                        linea = linea.split(",")
                        if linea[0] == ia_actual.nombre:
                            ia_actual.multiplicadores_ataque.append(float(linea[2]))
                            ia_actual.multiplicadores_defensa.append(float(linea[3]))

                        linea = s.readline()
        return ias

    else:
        return False
