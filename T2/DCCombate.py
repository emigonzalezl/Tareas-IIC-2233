import random
from parametros import ORO_POR_RONDA


def combate(jugador, ia):

    primero = False

    # Ver quien va primero
    print("\nComparando velocidades entre el jugador y la IA...")
    while True:
        chance = random.random()
        if chance > ia.velocidad:
            print(f"\n¡Vas muy rapido! Atacaras primero")
            primero = True
            break
        elif chance < ia.velocidad:
            print(f"¡La IA {ia.nombre} es muy veloz! atacara primero.")
            break

    # Si tiene el montapatos automaticamente va primero (prob especial 100%)
    tiene_montapatos = False

    for carta in jugador.cartas:
        if carta.nombre == "Montapatos":
            print("Pero tu tienes el Montapatos! Por lo que te corresponde atacar primero")
            tiene_montapatos = True

    # Si es que el jugador empieza, primero fase de ataque y despues de defensa
    if primero is True or tiene_montapatos is True:
        print("""\n
        -----------------------------
                 FASE DE ATAQUE
        -----------------------------\n
    """)
        daños = jugador.atacar()
        esta_viva = ia.recibir_daño(daños)

        if esta_viva is True:
            print("Tus cartas le han hecho daño a la IA!\n")
            print(f"Ahora {ia.nombre} tiene {ia.vida:.2f}/{ia.vida_maxima}")

        # Seguir con el ataque de la IA

            print("""\n
        -----------------------------
                FASE DE DEFENSA
        -----------------------------\n
        """)
            daños = ia.atacar()
            if len(jugador.cartas) >= 1:
                jugador.recibir_daño(daños, ia)
            else:
                return False

            if len(jugador.cartas) < 1:
                return False
        else:
            print(f"¡Has derrotado a {ia.nombre}!")
            return True
    else:
        print("""\n
        -----------------------------
                FASE DE DEFENSA
        -----------------------------\n
        """)
        if len(jugador.cartas) >= 1:
            daños = ia.atacar()
            jugador.recibir_daño(daños, ia)
        else:
            return False

        if len(jugador.cartas) < 1:
            return False

        if len(jugador.cartas) >= 1:

            ("""\n
        -----------------------------
                 FASE DE ATAQUE
        -----------------------------\n
    """)

            daños = jugador.atacar()
            esta_viva = ia.recibir_daño(daños)

            if esta_viva is True:
                print("Tus cartas le han hecho daño a la IA!")
                print(f"Ahora {ia.nombre} tiene {ia.vida:.2f}/{ia.vida_maxima}")
            else:
                return True
        else:
            return False

    jugador.rondas += 1
    jugador.dinero += ORO_POR_RONDA
