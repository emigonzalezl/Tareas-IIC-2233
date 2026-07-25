import random


class Jugador():

    def __init__(self, nombre, dinero, ias_len):
        self.nombre = nombre
        self.dinero = dinero
        self.cartas = []  # instancias de cartas actuales. Hasta 5.
        self.coleccion = []  # instancias de todas las cartas disponibles no actuales
        self.rondas = 0
        self.ias_derrotadas = 0
        self.ias_totales = ias_len

    def __str__(self):
        presentarse = []
        presentarse.append(f"Jugador: {self.nombre}")
        presentarse.append(f"Victorias: {self.ias_derrotadas}/{self.ias_totales}")
        presentarse.append("Cartas:\n")

# Esto no sabia como se usaba y lo aprendí de:
# https://www.codecademy.com/resources/docs/python/built-in-functions/enumerate
        for i, carta in enumerate(self.cartas, start=1):
            presentarse.append(f"[{i}] {carta}")
        return "\n".join(presentarse)

    def recibir_daño(self, daños, ia):

        # for carta in self.cartas:
        #     carta.usar_habilidad_especial("recibir")

        estructuras = []

        for carta in self.cartas:
            if carta.tipo == "estructura" or carta.tipo == "mixta":
                estructuras.append(carta)

        if len(estructuras) >= 1:

            for carta in estructuras:
                if carta.tipo == "estructura":  # daño efectivo repartido en las estructuras
                    viva = carta.recibir_daño(daños[1]/len(estructuras))
                elif carta.tipo == "mixta":
                    viva = carta.recibir_daño(daños[2]/len(estructuras))

                print(f"La carta {carta.nombre} es atacada! {carta.vida:.2f}/"
                      f"{carta.vida_maxima}.\n")
                if viva is False:
                    self.cartas.remove(carta)
                    print(f"¡Oh no! la carta {carta.nombre} ha sido eliminada 💀")

        else:

            for carta in self.cartas:
                if carta.tipo == "tropa":
                    viva = carta.recibir_daño(daños[0])
                if carta.tipo == "estructura":
                    viva = carta.recibir_daño(daños[1])
                elif carta.tipo == "mixta":
                    viva = carta.recibir_daño(daños[2])

                print(f"\n{ia.nombre} ataca a {carta.nombre}! {carta.vida}/{carta.vida_maxima}")
                if viva is False:
                    self.cartas.remove(carta)
                    print(f"¡Oh no! la carta {carta.nombre} ha sido eliminada 💀")

        # Esto no devuelve nada, solo elimina las cartas y aplica daño segun corresponde

    def atacar(self):

        daños = [[0, "tropa"], [0, "estructura"], [0, "mixta"]]

        for carta in self.cartas:
            for i in range(len(daños)):
                if daños[i][1] == carta.tipo and carta.tipo != "estructura":
                    daño = carta.atacar()
                    daños[i][0] += daño

        return daños

        # Que devuelva el total del daño por tipo de carta


class IA():

    def __init__(self, nombre, vida_maxima, ataque, probabilidad_especial, velocidad, descripcion):
        self.nombre = nombre
        self.vida_maxima = vida_maxima
        self.vida = vida_maxima
        self.ataque = ataque
        self.probabilidad_especial = probabilidad_especial
        self.velocidad = velocidad
        self.descripcion = descripcion
        self.multiplicadores_defensa = []  # lista por tipo t, e, m
        self.multiplicadores_ataque = []  # lista por tipo

    def __str__(self):
        presentar = (f'IA: {self.nombre}, vida: {self.vida:.1f}/{self.vida_maxima}\n'
                     f'"{self.descripcion}"')
        return presentar

    # Devuelve lista con daño por tipo
    def atacar(self):

        daño_tropa = self.ataque * self.multiplicadores_ataque[0]
        daño_estructura = self.ataque * self.multiplicadores_ataque[1]
        daño_mixta = self.ataque * self.multiplicadores_ataque[2]

        daños = [daño_tropa, daño_estructura, daño_mixta]

        return daños

    def recibir_daño(self, daños):
        daño_recibido = 0
        for i in range(len(daños)):
            if daños[i][1] == 'tropa':
                daño_recibido += daños[i][0] * self.multiplicadores_defensa[0]
            elif daños[i][1] == 'estructura':
                daño_recibido += daños[i][0] * self.multiplicadores_defensa[1]
            elif daños[i][1] == 'mixta':
                daño_recibido += daños[i][0] * self.multiplicadores_defensa[2]

        if self.vida - daño_recibido > 0:
            # Esta vivo
            self.vida -= daño_recibido
            return True
        else:
            # Se murio!
            return False

    def habilidad_especial(self):
        if random.random() <= self.probabilidad_especial:
            return True
        else:
            return False
