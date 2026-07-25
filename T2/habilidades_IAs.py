def habilidad_Crok(jugador, ia):
    # Dos cartas al azar no atacan ni defienden por 3 rondas
    pass


def habilidad_gemibee(jugador, ia):
    # Aumenta multiplicadores de ataque y defenesa en 0,1+ cada vez que la usa
    pass


def habilidad_cowpilot(jugador, ia):
    # cambia dos cartas al azar de tu maso por otra del mazo al azar
    pass


def habilidad_catgpt(jugador, ia):
    # multiplicadores de defensa de cartas activas = 0,65
    for carta in jugador.cartas:
        carta.multiplicador_defensa = 0.65
        carta.multiplicador_ataque = 0.65
    # por este turno o permanentes?
    pass


def habilidad_deepsheep(jugador, ia):
    # en el menu de la tarea se muestra solo la vida
    pass
