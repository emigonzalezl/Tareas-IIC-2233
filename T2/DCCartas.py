from abc import ABC, abstractmethod
import random
from habilidades_cartas import encontrar_habilidad, habilidad_Antimuros_IngUC, habilidad_barbaros, \
    habilidad_caballero, habilidad_cartel_de_duendes, habilidad_cañon, habilidad_cuartel_de_barbaros, \
    habilidad_duendes, habilidad_escuadron_de_esqueletos, habilidad_espiritu_igneo, habilidad_globo, habilidad_horno, habilidad_lapida, habilidad_maldecidor_duende, habilidad_montapatos, habilidad_PEPPA, habilidad_recolector_de_agua, habilidad_torre_bomba, habilidad_torre_DIE

# Clase madre abstracta
class Carta(ABC):

    def __init__(self, nombre, tipo, vida_maxima, vida,
                 multiplicador_defensa, precio, probabilidad_especial):
        self.nombre = nombre
        self.vida_maxima = vida_maxima
        self.vida = vida
        self.tipo = tipo
        self.multiplicador_defensa = multiplicador_defensa
        self.precio = precio
        self.probabilidad_especial = probabilidad_especial

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def recibir_daño(self):
        pass

    @abstractmethod
    def usar_habilidad_especial(self):
        pass


# Herencia simple
class CartaTropa(Carta):

    def __init__(self, nombre, tipo, vida_maxima, vida, multiplicador_defensa, precio,
                 probabilidad_especial, ataque, multiplicador_ataque, descripcion):
        super().__init__(nombre, tipo, vida_maxima, vida, multiplicador_defensa, precio,
                         probabilidad_especial)

        self.ataque = ataque
        self.multiplicador_ataque = multiplicador_ataque
        self.descripcion = descripcion

    def __str__(self):
        presentarse = (f"{self.nombre} ({self.tipo}): {self.vida:.2f}/{self.vida_maxima}"
                       f" HP, Ataque: {self.ataque}.")
        return presentarse

    def __repr__(self):
        return self.nombre

# Devuelve True si sique vivo (es int o numeric) o False si no, none si no puedo recibir el daño
    def recibir_daño(self, daño):

        if type(daño) is int or type(daño) is float:
            daño_recibido = daño * self.multiplicador_defensa

        elif type(daño) is str:
            if daño.isnumeric() is True:
                daño_recibido = float(daño) * self.multiplicador_defensa

            else:
                return None
        else:
            return None

        if self.vida - daño_recibido > 0:
            # Aun no muere
            self.vida -= daño_recibido
            return True

        elif self.vida - daño_recibido <= 0:
            # Se murio!
            self.vida = 0
            return False

    def atacar(self):
        atk = self.ataque * self.multiplicador_ataque
        return atk

    def usar_habilidad_especial(self, fase):
        if random.random() <= self.probabilidad_especial:
            if fase == "recibir":
                pass
            elif fase == "atacar":
                pass
            # AQUI IMPORTAR DICCIONARIO CON HABILIDADES


# Herencia simple
class CartaEstructura(Carta):

    def __init__(self, nombre, tipo, vida_maxima, vida, multiplicador_defensa,
                 precio, probabilidad_especial, descripcion):
        super().__init__(nombre, tipo, vida_maxima, vida, multiplicador_defensa,
                         precio, probabilidad_especial)

        self.descripcion = descripcion

    def __str__(self):
        presentarse = (f"{self.nombre} ({self.tipo}): {self.vida:.2f}/{self.vida_maxima} HP, "
                       f"Multiplicador defensa: {self.multiplicador_defensa}.")
        return presentarse

# Esto no era necesario pero para facilitarme la vida resteando el codigo.
    def __repr__(self):
        return self.nombre

# Devuelve True si sique vivo (es int o numeric) o False si no, none si no puedo recibir el daño
    def recibir_daño(self, daño):

        if type(daño) is int or type(daño) is float:
            daño_recibido = daño * self.multiplicador_defensa

        elif type(daño) is str:
            if daño.isnumeric() is True:
                daño_recibido = float(daño) * self.multiplicador_defensa

            else:
                return None
        else:
            return None

        if self.vida - daño_recibido > 0:
            # Aun no muere
            self.vida -= daño_recibido
            return True

        elif self.vida - daño_recibido <= 0:
            # Se murio!
            self.vida = 0
            return False

    def usar_habilidad_especial(self):
        if random.random() <= self.probabilidad_especial:
            return True
        else:
            return False


# Polimorfismo (overriding). Herencia multiple
class CartaMixta(CartaTropa, CartaEstructura):
    # Indicamos que los valores pasados son de CartaTropa y CartaEstructura
    def __init__(self, tropa: CartaTropa, estructura: CartaEstructura):
        self.tropa = tropa
        self.estructura = estructura
        self.tipo = "mixta"
        self.vida = self.vida_maxima

    @property
    def nombre(self):
        return f"{self.tropa.nombre} - {self.estructura.nombre}"

    @property
    def vida_maxima(self):
        return ((self.tropa.vida_maxima)/2 + self.estructura.vida_maxima)

    @property
    def ataque(self):
        return self.tropa.ataque

    @property
    def multiplicador_defensa(self):
        return max(self.tropa.multiplicador_defensa, self.estructura.multiplicador_defensa)

    @property
    def multiplicador_ataque(self):
        return max(self.tropa.multiplicador_ataque, self.multiplicador_defensa)

    @property
    def probabilidad_especial(self):
        # Promedio aumentado en un 10%
        return ((self.tropa.probabilidad_especial + self.estructura.precio.probabilidad_especial)/2)*1.1

    def __str__(self):
        presentarse = (f"{self.nombre} ({self.tipo}): {self.vida}/{self.vida_maxima}"
                       f" HP, Ataque: {self.ataque}, Multiplicador defensa: "
                       f"{self.multiplicador_defensa:.3f}.")
        return presentarse

    def __repr__(self):
        return f"{self.nombre}, {self.ataque}, {self.vida}/{self.vida_maxima}"

    def recibir_daño(self, daño):

        if type(daño) is int or type(daño) is float:
            daño_recibido = daño * self.multiplicador_defensa

        elif type(daño) is str:
            if daño.isnumeric() is True:
                daño_recibido = float(daño) * self.multiplicador_defensa

            else:
                return None
        else:
            return None

        if self.vida - daño_recibido > 0:
            # Aun no muere
            self.vida -= daño_recibido
            return True

        elif self.vida - daño_recibido <= 0:
            # Se murio!
            self.vida = 0
            return False

    def atacar(self):
        atk = self.ataque * self.multiplicador_ataque
        return atk

    def usar_habilidad_especial(self, fase):
        if random.random() <= self.probabilidad_especial:
            if fase == "recibir":
                pass
            elif fase == "atacar":
                pass



# bomb = CartaEstructura("Torre bomba", "estructura", 170, 170, 0.8, 9, 0.35,
#                        "Esta estructura deja una bomba al morir que causa un daño DANO_BOMBA")
# peppa = CartaTropa("P.E.P.P.A", "tropa", 200, 200, 0.9, 15, 0.2, 30, 1.2, "Cuando ataca, se "
#                    "sana en un CURE_PEPPA% de su vida máxima")

# mix = CartaMixta(peppa, bomb)

# print(mix.multiplicador_defensa)

# print(mix)