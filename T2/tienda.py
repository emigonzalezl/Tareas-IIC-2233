import random
from parametros import COSTO_CURAR, COSTO_REROLL, COSTO_REVIVIR, COSTO_COMBINACION
from DCCartas import CartaMixta


class Tienda():
    def __init__(self):
        self.cartas_tienda = []


# Pool cartas totales
def generar_pool(jugador, tienda, pool_cartas):

    pool_tienda = []

    for carta in pool_cartas:
        if carta not in jugador.coleccion:
            pool_tienda.append(carta)

    cantidad = random.randint(3, 5)
    tienda.cartas_tienda = random.sample(pool_tienda, cantidad)

    return None


def mostrar_tienda(jugador, tienda, pool_cartas):

    opciones = ["1", "2", "3", "4", "5"]
    opciones_cartas = []
    while True:

        print(f"""\n
        -----------------------------
                    TIENDA
        -----------------------------\n
        Dinero disponible: {jugador.dinero} G
            """)
        print(f"""
        [1] Curar carta 🚑
        [2] Revivir carta del cementerio 🪦
        [3] Reroll catálogo : {COSTO_REROLL} G
        [4] Taller ⚒️
        [5] Volver al Menú principal

        Cartas disponibles:\n""")

        i = 5
        if len(tienda.cartas_tienda) >= 1:
            for carta in tienda.cartas_tienda:
                i += 1
                opciones_cartas.append(f"{i}")
                print(f"        [{i}] {carta.nombre}"
                      f" -- {carta.precio} G")
        else:
            print("\n        [Tienda Vacia]\n")

        print("\nIndique su opción:")

        while True:
            choice = input("\n--> ")

            if choice in opciones:
                if choice == "1":
                    curables = []
                    for carta in jugador.coleccion:
                        if 0 < carta.vida < carta.vida_maxima:
                            curables.append(carta)

                    print("""
        -----------------------------
                 CURAR CARTAS
        -----------------------------
                        """)
                    i = 1
                    opciones_curar = []
                    if len(curables) >= 1:
                        for carta in curables:
                            print(f"        [{i}] Curar {carta.nombre}: {carta.vida:.2f}/"
                                  f"{carta.vida_maxima}")
                            opciones_curar.append(f"{i}")
                            i += 1
                    print(f"""\n
        [{i}] Volver atras

        Elige una opción:""")

                    while True:
                        choice_curar = input("\n--> ")
                        if choice_curar == f"{i}":
                            break
                        elif choice_curar in opciones_curar:
                            if jugador.dinero >= COSTO_CURAR:
                                indx_ = int(choice_curar)-1
                                curables[indx_].vida = curables[indx_].vida_maxima
                                print(f"\nSe ha curado la carta {curables[indx_].nombre}")
                                print(f"{curables[indx_].vida}/{curables[indx_].vida_maxima}")
                                jugador.dinero -= COSTO_CURAR
                                break
                            else:
                                print("\nNo tienes suficiente oro para curar esta carta :(")
                                break

                        else:
                            print("\nPorfavor ingrese una opción valida")
                    break

                elif choice == "2":
                    revivibles = []
                    for carta in jugador.coleccion:
                        if carta.vida <= 0:
                            revivibles.append(carta)

                    print("""
            -----------------------------
                    REVIVIR CARTAS
            -----------------------------
                          """)
                    i = 1
                    opciones_revivir = ["1"]
                    for carta in revivibles:
                        print(f"[{i}] {carta}")
                        i += 1
                        opciones_revivir.append(f"{i}")
                    print(f"        [{i}] Volver atras\n")
                    print("\n     Elige una opción:")

                    while True:
                        choice_revivir = input("\n--> ")
                        if choice_revivir == f"{i}":
                            break
                        elif choice_revivir in opciones_revivir:
                            if jugador.dinero >= COSTO_REVIVIR:
                                indx__ = int(choice_revivir) - 1
                                revivibles[indx__].vida = revivibles[indx__].vida_maxima
                                print(f"Se ha curado la carta {revivibles[indx__]}")
                                jugador.dinero -= COSTO_REVIVIR
                                break
                            else:
                                print("\nNo tienes suficiente dinero para revivir esta carta :(")
                                break
                        else:
                            print("\nIngresa una opción válida.")

                    break

                elif choice == "3":
                    if jugador.dinero >= COSTO_REROLL:
                        generar_pool(jugador, tienda, pool_cartas)
                        opciones_cartas = []
                        print("\nSe han reiniciado las cartas de la tienda.")
                        jugador.dinero -= COSTO_REROLL
                    else:
                        print("\nNo tienes suficiente dinero para hacer un reroll.")

                    break

                elif choice == "4":
                    mostrar_taller(jugador)
                    break

                elif choice == "5":
                    print("\n\nVolviendo al menu principal ...\n")
                    return None

            elif choice in opciones_cartas:
                indx = int(choice) - 6
                print(f"\n¿Comprar carta >> {tienda.cartas_tienda[indx]} << por "
                      f"{tienda.cartas_tienda[indx].precio} G?")
                print("[1] Si \n[2] No")

                while True:
                    yes_no = input("\n--> ")
                    if yes_no == "1":
                        if jugador.dinero >= tienda.cartas_tienda[indx].precio:
                            jugador.coleccion.append(tienda.cartas_tienda[indx])
                            jugador.dinero -= tienda.cartas_tienda[indx].precio
                            print(f"\n¡La carta {tienda.cartas_tienda[indx]} ha sido "
                                  "añadida a tu colección!")
                            tienda.cartas_tienda.pop(indx)
                            opciones_cartas = []
                        else:
                            print("\nNo tienes suficiente dinero para comprar esta carta :(")
                        break
                    elif yes_no == "2":
                        break
                    else:
                        print("\nPorfavor ingrese una opción valida p")

                break
            else:
                print("\nIngrese una opción valida")


def curar_cartas():
    pass


def mostrar_taller(jugador):

    cartas_tropa = []
    cartas_estructura = []

    for carta in jugador.coleccion:
        if carta.tipo == "tropa":
            cartas_tropa.append(carta)
        elif carta.tipo == "estructura":
            cartas_estructura.append(carta)

    opciones_tropa = []
    opciones_estructura = []
    i = 1
    print(f"""\n
        -----------------------------
                    TALLER
        -----------------------------\n

        Escoge una carta tropa para fusionarla con una carta
        estructura. Costo: {COSTO_COMBINACION} G
        """)
    print("\n        Cartas Tropa disponibles:\n")
    for carta in cartas_tropa:
        print(f"        [{i}] {carta.nombre}")
        opciones_tropa.append(f"{i}")
        i += 1
    print("\n        Cartas Estructura disponibles\n")
    for carta in cartas_estructura:
        print(f"        -> {carta.nombre}")
        opciones_estructura.append(f"{i}")
        i += 1
    print("\n        [0] Volver atras")

    while True:
        choice = input("\n--> ")

        if choice == "0":
            print("\nVolviendo a la tienda ...\n")
            break

        elif choice in opciones_tropa:
            if jugador.dinero >= COSTO_COMBINACION:
                print(f"\nHas seleccionado: {cartas_tropa[int(choice)-1].nombre}.")
                print("\n¿Deseas fusionar esta carta con una estructura?")
                print("\n[1] Si --> Elegir carta\n[2] Volver")

                choice_fusion_t = input("\n--> ")

                while True:

                    if choice_fusion_t == "1":
                        print("\nEliige una carta estructura con la cual fusionarla:\n")
                        k = 1
                        opciones_k = []
                        for carta in cartas_estructura:
                            print(f"[{k}] {carta}")
                            opciones_k.append(f"{k}")
                            k += 1

                        choice_subfusion_t = input("\n--> ")
                        while True:
                            if choice_subfusion_t in opciones_k:
                                indx_1 = int(choice)-1
                                indx_2 = int(choice_subfusion_t)-1
                                carta = CartaMixta(cartas_tropa[indx_1], cartas_estructura[indx_2])

                                if cartas_tropa[indx_1] in jugador.cartas:
                                    jugador.cartas.remove(cartas_tropa[indx_1])
                                if cartas_estructura[indx_2] in jugador.cartas:
                                    jugador.cartas.remove(cartas_estructura[indx_2])

                                jugador.coleccion.remove(cartas_tropa[indx_1])
                                jugador.coleccion.remove(cartas_estructura[indx_2])

                                jugador.coleccion.append(carta)
                                jugador.dinero -= COSTO_COMBINACION

                                print(f"\n¡Carta mixta {carta.nombre} creada! Revisa "
                                      "tu coleccion.")

                                cartas_tropa = []
                                cartas_estructura = []
                                opciones_tropa = []
                                opciones_estructura = []
                                i = 1

                                break
                            else:
                                print("\nIngresa una opcion valida.")
                                choice_subfusion_t = input("\n--> ")

                        break

                    elif choice_fusion_t == "2":
                        break
                    else:
                        print("\nPorfavor elige una opción valida")
                    choice_fusion_t = input("\n--> ")

            else:
                print("\nNo tienes suficiente oro para combinar cartas.")
        else:
            print("\nIngresa una opción válida.")

        break
