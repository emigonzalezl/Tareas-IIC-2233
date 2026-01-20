from dccasillas import DCCasillas
from herramientas import mostrar_menu_juego, mostrar_menu_acciones
import os
# Info de como usar os sacada de:
# https://www.freecodecamp.org/news/how-to-check-if-a-file-exists-in-python/

"""
Breve función que recibe dos parametros e inicializa DCCasillas
"""


def iniciar_juego(user, config):
    dccasillas = DCCasillas(user, config)
    return dccasillas  # lista con c/u


"""
Para simplificar la construccion del menu, la primera instancia del juego
se ejecuta en una funcion aparte, ya que al no estar definida la clase y
contar con mas restricciones facilita el manejo,
"""


def primer_juego():

    no_validas_aun = ["2", "3", "4"]
    choice = mostrar_menu_juego()

    while True:

        if choice == "1":

            print("\n<-- Iniciar Juego nuevo -->\n")

            user = input("Ingresa un usuario valido:\n* ¡No un str vacío!\n"
                         "\n--> ")
            while user == "":
                user = input("\nNombre invalido. Intenta de nuevo\n\n--> ")
            print(f"\nNombre de usuario actual: {user}")

            print("\nIngresa una configuración de tablero")
            print("* sin config/ previo ni .txt final.")
            config = input("\n--> ")

            while os.path.exists(f"config/{config}.txt") is not True:
                print("\nArchivo no encontrado. Intenta de nuevo.")
                config = input("\n--> ")

            print("¡Archivo encontrado!")
            return iniciar_juego(user, f"{config}.txt")

        elif choice in no_validas_aun:
            print("\n[ Defina un nombre de usuario y configuración "
                  "para acceder a estas funciones ]")
            choice = input("\n--> ")

        elif choice == "5":
            ("\n<-- Salir del programa -->")
            print("¡Adios!")
            return False
        else:
            print("ingresa una opción válida.")
            choice = input("\n--> ")


"""
Función principal donde se ejecuta y cicla todo el juego.
Esta separada en dos while, cada uno correspondiente a un menu.
Un qhile se encuentra dentro del otro a modo de poder alternar entre ellos
segun indique el input del usuario.
"""


def main():

    """
    Esta primera parte es el setup. Se corre la primera instancia de juego,
    se inicializa DCCasillas,
    """

    objetos = primer_juego()
    if objetos is False:
        return None

    dccasillas = objetos
    tablero = dccasillas.tableros[0]
    tablero.cargar_tablero(dccasillas.archivos[0])

    salir = False

    """
    El while principal itera sobre el menu de acciones
    Maneja las 5 opciones posibles y redirige al menu
    de juego de ser necesario
    """

    while True:

        # Ahora que esta dada una configuración y usuario, se pueden rellenar
        # los parametros pertenecienentes al juego actual en cada menu.
        choice = mostrar_menu_acciones(dccasillas.usuario, dccasillas.puntaje,
                                       dccasillas.tablero_actual+1,
                                       len(dccasillas.tableros),
                                       dccasillas.tableros[dccasillas.tablero_actual].movimientos)

        # Llama a la función de clase mostrar_tablero() de DCCasillas.
        if choice == "1":
            print("\n<-- Mostrar Tablero -->\n")
            dccasillas.tableros[dccasillas.tablero_actual].mostrar_tablero()

        # Llama a la función modificar_casilla() de la instancia de tablero
        # para el tablero actual.
        elif choice == "2":
            print("\n<-- Habilitar/Deshabilitar Casillas -->\n")
            print("[ Ingresa una coordenada de casilla para modificar ]\n")
            print("* Las casillas vacias NO son modificables.\n"
                  "* Usa coordenadas numericas por index (desde el 0) y "
                  "asegurate de que esten separadas por coma sin espacio."
                  " Ej: (0,3)\n* No usar valores negativos.")
            print("* Recuerda que la ultima fila y columna NO forman parte"
                  " del tablero editable.")

            coords = False

            # While itera hasta recibir un parametro valido.
            while coords is False:

                coords = input("\n--> ")
                if "," in coords:
                    coords = coords.split(",")
                    tablero = dccasillas.tableros[dccasillas.tablero_actual]
                    if tablero.modificar_casilla(coords[0], coords[1]) is True:
                        print("\nCasilla modificada exitosamente.\nElija la "
                              "opción 'Mostrar Tablero' en el Menu de Acciones"
                              " para ver sus cambios")
                        coords = True
                    else:
                        print("\nIngrese coordenadas validas")
                        coords = False
                else:
                    print("\nIngrese coordenadas validas")
                    coords = False
            # Mediante el uso de true y false, lo que no se controla desde el
            # menu se controla con el return de la función modificar_casilla.

        # Llama a la función validar() dentro de la instancia de Tablero para
        # el tablero actual
        elif choice == "3":
            print("\n<-- Verificar Solución -->")
            validacion = tablero.validar()

            # Alterna entre ambos prints dependiendo de la validez del tablero.
            if validacion is True:

                print("\n~~~ ¡La solución es válida! :D ~~~")
                tab = dccasillas.tableros[dccasillas.tablero_actual].tablero

                if dccasillas.tablero_actual not in dccasillas.resueltos:
                    dccasillas.resueltos.append(dccasillas.tablero_actual)
                    # Calcular ptje
                    suma = 0
                    # Para el puntaje realizo una suma de todas las casillas
                    # regulares editables y si es la primera vez que se
                    # resuelve el tablero se suman al puntaje.
                    for i in range(len(tab)-1):
                        for k in range(len(tab)-1):
                            if tab[i][k] != ".":
                                if "X" in tab[i][k]:
                                    suma += int((tab[i][k])[1:])
                                else:
                                    suma += int(tab[i][k])
                    dccasillas.puntaje += suma

                else:
                    continue

            else:
                print("\n~~~ La solución no es valida :( ~~~")

        # Llama a la función encontrar_solucion() para el tablero en su estado
        # actual. Todavia no esta listo.
        elif choice == "4":
            print("\n<-- Encontrar Solución -->")
            print("Funcion aun no disponible :)")

        # Lleva al usuario al menu de juego.
        elif choice == "5":
            print("\n<-- Volver al Menu de Juego -->")
            print("\nVolviendo al Menu de Juego ...")

            while True:

                """
                En este segundo while se itera sobre el menu de acciones.
                Permitiendo alternar entre ambos menus mediante el input
                del usuario.
                """

                # Muestra el menu de juego con los datos del usuario y
                # juego actual.
                choice = mostrar_menu_juego(dccasillas.usuario,
                                            dccasillas.puntaje,
                                            len(dccasillas.resueltos),
                                            len(dccasillas.tableros))

                # Re-instancia la clase por una nueva, empezando un juego nuevo
                # en base a la configuración y usuario dados.
                # Reemplaza la variable dccasillas con la instancia nueva.
                if choice == "1":
                    print("\n<-- Iniciar Juego nuevo -->\n")
                    print("El nombre de usuario actual es:"
                          f"{dccasillas.usuario}")
                    print("¿Deseas cambiarlo?\n[1] Si\n[2] No\n")

                    # while que revisa la validez del nombre de usuario.
                    while True:
                        choice_user = input("\n--> ")

                        if choice_user == "1":
                            user = input("Ingresa un usuario valido:\n* "
                                         "¡No un str vacío!\n\n--> ")
                            while user == "":
                                user = input("\nNombre invalido. Intenta"
                                             " de nuevo\n\n--> ")
                            print(f"\nNombre de usuario actual: {user}")
                            dccasillas.usuario = user
                            break

                        elif choice_user == "2":
                            print("Continuando con el numbre de usuario"
                                  f"actual: {dccasillas.usuario}")
                            break

                        else:
                            print("\nIngresa una opcion valida.")

                    print("\nIngresa una configuración de tablero")
                    print("* sin config/ previo ni .txt final.")
                    config = input("\n--> ")

                    while os.path.exists(f"config/{config}.txt") is not True:
                        print("\nArchivo no encontrado. Intenta de nuevo.")
                        config = input("\n--> ")

                    print("¡Archivo encontrado!")
                    dccasillas = iniciar_juego(dccasillas.usuario,
                                               f"{config}.txt")

                elif choice == "2":
                    print("\n<-- Continuar Juego -->\n")
                    print(f"Tablero actual: {dccasillas.tablero_actual+1}\n")
                    print("La configuración actual tiene "
                          f"{len(dccasillas.tableros)} tableros disponibles")
                    print("¿Desea continuar con el tablero actual o "
                          "cambiar de tablero?\n")
                    print("[1] Actual\n[2] Cambiar\n")
                    while True:
                        user_choice = input("\n--> ")
                        if user_choice == "1" or user_choice == "2":
                            if user_choice == "1":
                                print("\nContinuando con el tablero: "
                                      f"{dccasillas.tablero_actual}.")
                                break
                            elif user_choice == "2":
                                print("\nElija un tablero del 1 al "
                                      f"{len(dccasillas.tableros)}.")
                                while True:
                                    choice = input("\n--> ")
                                    if choice.isdigit() is True:
                                        largo = len(dccasillas.tableros)
                                        if 1 <= int(choice) <= largo:
                                            choice = int(choice)-1
                                            dccasillas.tablero_actual = choice
                                            break
                                    else:
                                        print("\nIngresa una opcion valida.")
                                break
                        else:
                            print("Ingrese una opcion valida")
                    break

                elif choice == "3":
                    print("\n<-- Guardar estado de juego -->")
                    if dccasillas.guardar_estado() is True:
                        print(">> Estado guardado con exito!")
                    else:
                        print(">> No se pudo guardar el archivo.")

                elif choice == "4":
                    print("\n<-- Recuperar estado de juego -->")
                    if dccasillas.recuperar_estado() is True:
                        print(">> Estado recuperado con exito!")
                    else:
                        print(">> No se pudo recuperar el archivo.")

                # Unica parte del codigo que conduce a salir del main
                elif choice == "5":
                    ("\n<-- Salir del programa -->")
                    print("¡Adios!")
                    salir = True
                    break

        # Control de salida
        if salir is True:
            break


main()

# Si se termina de ejecutar main, avisar que se termino de ejecutar el
#  programa correctamente

print("\n<-- Salido del programa con exito -->")
