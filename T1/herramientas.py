
"""
En Herramientas se encuentran dos funciones que definí para imprimir el
tablero y pedir una elección al usuario mediante el terminal.
Ambas funciones imprimen su respectivo menu y devuelven la variable 'choice',
dentro de la cual esta la elección de el numero/opcion elegida por el usuario

Tienen similar formato y funcionamiento.

Además, reciben los parametros de usuario, tableros resueltos, tableros
totales, y puntaje para proporcionar al usuario información sobre el estado
de juego actual.
"""


def mostrar_menu_juego(usuario="UUU", ptje="PPP",
                       t_resueltos="XXX", t_totales="YYY"):

    # Parte de impresión de menu
    print("")
    print(f"¡Bienvenido a DCCasillas!\n\nUsuario: {usuario}, Puntaje: {ptje}")
    print(f"Tableros Resueltos: {t_resueltos} de {t_totales}\n")
    print("*** Menú de juego ***\n")
    print("[1] Iniciar Juego nuevo\n[2] Continuar Juego")
    print("[3] Guardar estado de juego\n[4] Recuperar estado de juego")
    print("[5] Salir del programa\n")
    print("Indique su opción (1, 2, 3, 4, 5):\n")

    # Parte donde se pide el input del usuario
    opciones = ["1", "2", "3", "4", "5"]
    choice = input("--> ")

    # While se asegura de que la opcion este dentro de parametros validos
    while choice not in opciones:
        print("\nError: Porfavor ingrese una opción valida >:(")
        choice = input("\n--> ")

    return choice


def mostrar_menu_acciones(usuario="UUU", ptje="PPP",
                          num_tablero="XXX", t_totales="YYY", movimientos="0"):
    # Parte de impresión de menu
    print("\n")
    print(f"DCCasillas\n\nUsuario: {usuario}, Puntaje: {ptje}")
    print(f"Número de tablero: {num_tablero} de {t_totales}\n")
    print(f"Movimientos de tablero: {movimientos}")
    print("*** Menú de Acciones ***\n")
    print("[1] Mostrar tablero\n[2] Habilitar/deshabilitar casillas")
    print("[3] Verificar solución\n[4] Encontrar solución")
    print("[5] Volver al menú de Juego\n")
    print("Indique su opción (1, 2, 3, 4, 5):\n")

    # Parte donde se pide el input del usuario
    opciones = ["1", "2", "3", "4", "5"]
    choice = input("\n--> ")

    # While se asegura de que la opcion este dentro de parametros validos
    while choice not in opciones:
        print("\nError: Porfavor ingrese una opción valida >:(")
        choice = input("\n--> ")

    return choice
