from herramientas import selección_inicial, cargar_cartas, cargar_IAs, mostrar_menu_principal, \
                         coleccion
from tienda import Tienda, mostrar_tienda, generar_pool
from DCCombate import combate
from jugadores import Jugador
from parametros import ARCHIVO_IAS_FACIL, ARCHIVO_IAS_NORMAL, ARCHIVO_IAS_DIFICIL, \
                       ARCHIVO_MULTIPLICADORES, DINERO_INICIAL_FACIL, DINERO_INICIAL_NORMAL, \
                       DINERO_INICIAL_DIFICIL, ORO_POR_VICTORIA


def pedir_nombre():

    print("¡Hola Jugador!¡Vamos a enfrentarnos a DCCatastrofe!\n")
    nombre = input("¿Cual es tu nombre?\n\n--> ")
    while nombre == "" or nombre == " ":
        print("\nIngresa un nombre que no sea un string vacio o solo un espacio.")
        nombre = input("\n--> ")

    print(f"\nMucho gusto, '{nombre}'. Elige una dificultad para la batalla:\n")
    print("[1] facil\n[2] Normal\n[3] Difícil")
    choices = ["1", "2", "3"]

    dificultad = input("\n--> ")

    while dificultad not in choices:
        print("\nIngresa una opción válida")
        dificultad = input("\n--> ")

    return nombre, int(dificultad)-1


# instanciar jugador
def main():

    cartas = cargar_cartas("data/cartas.csv")
    mazo = selección_inicial(cartas)
    nombre = pedir_nombre()

    dificultad = nombre[1]
    nombre = nombre[0]

    dificultades = [ARCHIVO_IAS_FACIL, ARCHIVO_IAS_NORMAL, ARCHIVO_IAS_DIFICIL]
    ia = cargar_IAs(dificultades[dificultad], ARCHIVO_MULTIPLICADORES)

    dineros = [DINERO_INICIAL_FACIL, DINERO_INICIAL_NORMAL, DINERO_INICIAL_DIFICIL]
    jugador = Jugador(nombre, dineros[dificultad], len(ia))

    jugador.cartas = []
    jugador.coleccion = []

    for carta in mazo:
        jugador.cartas.append(carta)
        jugador.coleccion.append(carta)

    tienda = Tienda()
    generar_pool(jugador, tienda, cartas)

    while True:

        choice = mostrar_menu_principal(jugador, jugador.rondas, ia[0])

        if choice == "1":
            resultados = combate(jugador, ia[0])
            if resultados is True:
                if len(ia) > 1 and len(ia) != 2:
                    print(f"\nHas derrotado a {ia[0].nombre}...\n¡Pero {ia[1].nombre} te espera!")
                    ia.pop(0)
                    jugador.dinero += ORO_POR_VICTORIA
                    jugador.ias_derrotadas += 1
                    for carta in jugador.coleccion:
                        carta.vida = carta.vida_maxima
                    generar_pool(jugador, tienda, cartas)
                elif len(ia) == 2:
                    print(f"Tras derrotar a {ia[0].nombre}, te encuentras al jefe final ..."
                          f" {ia[1].nombre}")
                    jugador.dinero += ORO_POR_VICTORIA
                    jugador.ias_derrotadas += 1
                    for carta in jugador.coleccion:
                        carta.vida = carta.vida_maxima
                    generar_pool(jugador, tienda, cartas)
                    ia.pop(0)
                elif len(ia) == 1:
                    print("¡Ji ji ji ja!\n¡Has derrotado a la ultima IA! Has vencido a "
                          "DCCatastrofe.")
                    jugador.dinero += ORO_POR_VICTORIA
                    jugador.ias_derrotadas += 1
                    for carta in jugador.coleccion:
                        carta.vida = carta.vida_maxima
                    generar_pool(jugador, tienda, cartas)
                    print("\n\n--- << ¡VICTORIA CAMPAL! >> ---\n\n")
                    return True
            elif resultados is False:
                print("¡Has perdido! La IA derroto todas tus cartas")
                print("\n\n--- << FIN DEL JUEGO >> ---\n\n")
                return False

            pass
        elif choice == "2":
            coleccion(jugador)
            pass
        elif choice == "3":
            mostrar_tienda(jugador, tienda, cartas)
            pass
        elif choice == "4":
            print(f"\n{ia[0]}")
            pass
        elif choice == "0":
            print("¡Adios!")
            return None


main()
