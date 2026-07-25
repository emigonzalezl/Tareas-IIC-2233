from parametros import CURE_PEPPA
from jugadores import Jugador


def habilidad_duendes(Carta, jugador, IA):
    oro_ganado = int(Carta.ataque)
    jugador.oro += oro_ganado
    # El daño que hacen se agrega como oro


def habilidad_PEPPA(CartaTropa, jugador, IA):
    CartaTropa.vida_maxima * CURE_PEPPA
    pass

# chequeo manual
def habilidad_montapatos():
    # Agregarla hace atacar antes q la IA
    pass


def habilidad_Antimuros_IngUC():
    # Cuando ataca se elimina del mazo
    pass


def habilidad_caballero():
    # Aumenta defensa de las demas tropas en un %DEF_CAB
    pass


def habilidad_maldecidor_duende():
    # Ataca una vez y una segunda vez por la mitad del ataque de la IA
    pass


def habilidad_escuadron_de_esqueletos():
    #  PROB_LARRY_GOD% de hacer 5 veces su daño y PROB_LARRY_MID% de morir insta al ser atacado.
    pass


def habilidad_barbaros():
    # Si ataca y sobrevive la ronda tiene PROB_BARB de aumentar permanentemente su ataque en POWER_UP_BARB%
    pass


def habilidad_espiritu_igneo():
    # probabilidad PROB_FIRE de no recibir daño en un turno
    pass


def habilidad_globo():
    # PROB_GLOBO de dejar una bomba que hace daño a la IA.
    pass


def habilidad_cañon():
    # Reduce defensas de IA en CANNON_ABILITY%
    pass


def habilidad_torre_DIE():
    # aplica DIE_PROB% de que la IA no ataque
    pass


def habilidad_recolector_de_agua():
    # Si muere se reemplaza por otra tropa aleatoria de la colección.
    pass


def habilidad_horno():
    # Al morir se reemplaza por el espiritu igneo
    pass


def habilidad_lapida():
    # PROB_LAPIDA% de no recibir daño del enemigo
    pass


def habilidad_cuartel_de_barbaros():
    # AL morir se reemplaza por barbaros
    pass


def habilidad_torre_bomba():
    # deja bomba al morir de DANO_BOMBA%
    pass


def habilidad_cartel_de_duendes():
    # Al morir se reemplaza por duendes
    pass

def encontrar_habilidad(carta):
    habilidades_cartas = {
        "Duendes": [habilidad_duendes, "ataque"],
        "P.E.P.P.A.": [habilidad_PEPPA, "ataque"],
        "Montapatos": [habilidad_montapatos, None],
        "Antimuros IngUC": [habilidad_Antimuros_IngUC, "ataque"],
        "Caballero": [habilidad_caballero, "recibir"],
        "Maldecidor Duende": [habilidad_maldecidor_duende, "ataque"],
        "Escuadrón de Esqueletos": [habilidad_escuadron_de_esqueletos, "ambas"],
        "Bárbaros": [habilidad_barbaros, "recibir"],
        "Espíritu Ígneo": [habilidad_espiritu_igneo, "recibir"],
        "Globo": [habilidad_globo, "recibir"],
        "Cañón": [habilidad_cañon, "ataque"],
        "Torre DIE": [habilidad_torre_DIE, "recibir"],  # (?)
        "Recolector de Agua": [habilidad_recolector_de_agua, "recibir"],
        "Horno": [habilidad_horno, "recibir"],
        "Lápida": [habilidad_lapida, "recibir"],
        "Cuartel de Bárbaros": [habilidad_cuartel_de_barbaros, "recibir"],
        "Torre Bomba": [habilidad_torre_bomba, "recibir"],
        "Cuartel de Duendes": [habilidad_cartel_de_duendes, "recibir"]
        }
    
    for nombre in habilidades_cartas:
        if nombre == carta.nombre:
            pass
            
# , "ataque"
