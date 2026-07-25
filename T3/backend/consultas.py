from typing import Generator, List, Tuple
from math import pi
from collections import defaultdict
from utilidades import (Astronauta, Nave, Tripulacion, Planeta, Mineral,
                        PlanetaMineral, Mision, MisionMineral, radio_planeta)
from backend.consultas_2 import (planetas_visitados_por_nave, mineral_por_nave,
                                 porcentaje_extraccion, resultado_mision)


def cargar_astronautas(path: str) -> Generator[Astronauta, None, None]:

    with open(path, encoding='utf-8') as f:
        linea = f.readline()
        for linea in f:
            linea = linea.strip().split(",")
            astronauta = Astronauta(id_astronauta=int(linea[0]), nombre=linea[1], estado=linea[2])
            yield astronauta


def cargar_naves(path: str) -> Generator[Nave, None, None]:

    with open(path, encoding='utf-8') as f:
        linea = f.readline()
        for linea in f:
            linea = linea.strip().split(",")
            nave = Nave(patente=linea[0], material=linea[1], tamano=linea[2],
                        capacidad_astronautas=int(linea[3]), capacidad_minerales=float(linea[4]),
                        autonomia=float(linea[5]))
            yield nave


def cargar_tripulaciones(path: str) -> Generator[Tripulacion, None, None]:

    with open(path, encoding='utf-8') as f:
        linea = f.readline()
        for linea in f:
            linea = linea.strip().split(",")
            tripulacion = Tripulacion(id_equipo=int(linea[0]), patente_nave=linea[1],
                                      id_astronauta=int(linea[2]), rango=int(linea[3]))
            yield tripulacion


def cargar_planetas(path: str) -> Generator[Planeta, None, None]:

    with open(path, encoding='utf-8') as f:
        linea = f.readline()
        for linea in f:
            linea = linea.strip().split(",")
            planeta = Planeta(id_planeta=int(linea[0]), nombre=linea[1],
                              coordenada_x=float(linea[2]), coordenada_y=float(linea[3]),
                              tamano=linea[4], tipo=linea[5])
            yield planeta


def cargar_minerales(path: str) -> Generator[Mineral, None, None]:

    with open(path, encoding='utf-8') as f:
        linea = f.readline()
        for linea in f:
            linea = linea.strip().split(",")
            mineral = Mineral(id_mineral=int(linea[0]), nombre=linea[1], simbolo_quimico=linea[2],
                              numero_atomico=int(linea[3]), masa_atomica=float(linea[4]))
            yield mineral


def cargar_planeta_minerales(path: str) -> Generator[PlanetaMineral, None, None]:

    with open(path, encoding='utf-8') as f:
        linea = f.readline()
        for linea in f:
            linea = linea.strip().split(",")
            p_mineral = PlanetaMineral(id_planeta=int(linea[0]), id_mineral=int(linea[1]),
                                       cantidad_disponible=float(linea[2]), pureza=float(linea[3]))
            yield p_mineral


def cargar_mision(path: str) -> Generator[Mision, None, None]:
    with open(path, encoding='utf-8') as f:
        linea = f.readline()
        for linea in f:
            linea = linea.strip().split(",")
            if linea[5] == "True":
                linea[5] = True
            elif linea[5] == "False":
                linea[5] = False
            elif linea[5] == "None":
                linea[5] = None
            mision = Mision(id_mision=int(linea[0]), fecha=linea[1], hora=linea[2],
                            id_equipo=int(linea[3]), id_planeta=int(linea[4]), lograda=linea[5])
            yield mision


def cargar_materiales_mision(path: str) -> Generator[MisionMineral, None, None]:
    with open(path, encoding='utf-8') as f:
        linea = f.readline()
        for linea in f:
            linea = linea.strip().split(",")
            mision_mineral = MisionMineral(id_mision=int(linea[0]), id_mineral=int(linea[1]),
                                           cantidad=float(linea[2]))
            yield mision_mineral


def naves_de_material(generador_naves: Generator[Nave, None, None], material: str
                      ) -> Generator[Nave, None, None]:
    while True:
        try:
            nave = next(generador_naves)
            if nave.material == material:
                yield nave
        except StopIteration:
            return None


def misiones_desde_fecha(generador_misiones: Generator[Mision, None, None], fecha: str,
                         inverso: bool) -> Generator[Mision, None, None]:
    fecha_objetivo = fecha.split("-")
    fecha_objetivo = [int(fecha_objetivo[0]), int(fecha_objetivo[1]), int(fecha_objetivo[2])]
    if inverso is False:
        while True:
            try:
                mision = next(generador_misiones)
                fecha_mision = mision.fecha.split("-")
                fecha_mision = [int(fecha_mision[0]), int(fecha_mision[1]), int(fecha_mision[2])]
                if fecha_mision[0] > fecha_objetivo[0]:
                    yield mision
                elif fecha_mision[0] == fecha_objetivo[0]:
                    if fecha_mision[1] > fecha_objetivo[1]:
                        yield mision
                    elif fecha_mision[1] == fecha_objetivo[1]:
                        if fecha_mision[2] >= fecha_objetivo[2]:
                            yield mision
            except StopIteration:
                return None
    elif inverso is True:
        while True:
            try:
                mision = next(generador_misiones)
                fecha_mision = mision.fecha.split("-")
                fecha_mision = [int(fecha_mision[0]), int(fecha_mision[1]), int(fecha_mision[2])]
                if fecha_mision[0] < fecha_objetivo[0]:
                    yield mision
                elif fecha_mision[0] == fecha_objetivo[0]:
                    if fecha_mision[1] < fecha_objetivo[1]:
                        yield mision
                    elif fecha_mision[1] == fecha_objetivo[1]:
                        if fecha_mision[2] <= fecha_objetivo[2]:
                            yield mision
            except StopIteration:
                return None


def naves_por_intervalo_carga(generador_naves: Generator[Nave, None, None],
                              cargas: tuple[float, float]) -> Generator[Nave, None, None]:
    min = cargas[0]
    max = cargas[1]
    while True:
        try:
            nave = next(generador_naves)
            if min <= nave.capacidad_minerales <= max:
                yield nave
        except StopIteration:
            return None


def planetas_con_cantidad_de_minerales(generador_planeta_mineral: Generator[PlanetaMineral, None,
                                                                            None], id_mineral: int,
                                       cantidad_minima: int) -> List[int]:
    ids_planetas = []
    while True:
        try:
            planeta_mineral = next(generador_planeta_mineral)
            if planeta_mineral.id_mineral == id_mineral:
                if planeta_mineral.cantidad_disponible*planeta_mineral.pureza >= cantidad_minima:
                    ids_planetas.append(planeta_mineral.id_planeta)
        except StopIteration:
            return ids_planetas


def naves_astronautas_rango(generador_tripulacion: Generator[Tripulacion, None, None], rango: int,
                            minimo_astronautas: int) -> Generator[Tuple[str, Generator],
                                                                  None, None]:
    nave_actual = [None, []]
    while True:
        try:
            tripulacion = next(generador_tripulacion)
            if nave_actual[0] is None:
                nave_actual[0] = tripulacion.patente_nave
                if tripulacion.rango >= rango:
                    nave_actual[1].append(tripulacion.id_astronauta)
            elif tripulacion.patente_nave == nave_actual[0]:
                if tripulacion.rango >= rango:
                    nave_actual[1].append(tripulacion.id_astronauta)
            elif tripulacion.patente_nave != nave_actual[0]:
                if len(nave_actual[1]) >= minimo_astronautas:
                    generador_ids = (x for x in nave_actual[1])
                    nave_devuelta = (nave_actual[0], generador_ids)
                    yield nave_devuelta
                nave_actual = [tripulacion.patente_nave, []]
                if tripulacion.rango >= rango:
                    nave_actual[1].append(tripulacion.id_astronauta)
        except StopIteration:
            if len(nave_actual[1]) >= minimo_astronautas:
                generador_ids = (x for x in nave_actual[1])
                nave_devuelta = (nave_actual[0], generador_ids)
                yield nave_devuelta
            return None


def cambiar_rango_astronauta(generador_tripulacion: Generator[Tripulacion, None, None],
                             id_astronauta: int, rango_astronauta: int
                             ) -> Generator[Tripulacion, None, None]:
    while True:
        try:
            tripulacion = next(generador_tripulacion)
            if tripulacion.id_astronauta == id_astronauta:
                astronauta_nuevo = tripulacion._replace(rango=rango_astronauta)
                yield astronauta_nuevo
            else:
                yield tripulacion
        except StopIteration:
            return None


def encontrar_planetas_cercanos(generador_planetas: Generator[Planeta, None, None], x1: int,
                                y1: int, x2: int, y2: int, cantidad: int | None = None
                                ) -> Generator[Planeta, None, None]:
    contador = 0
    while True:
        try:
            planeta = next(generador_planetas)
            if cantidad is not None:
                if x1 <= planeta.coordenada_x <= x2 and y1 <= planeta.coordenada_y <= y2:
                    if contador < cantidad:
                        yield planeta
                        contador += 1
            else:
                if x1 <= planeta.coordenada_x <= x2 and y1 <= planeta.coordenada_y <= y2:
                    yield planeta
        except StopIteration:
            return None


def disponibilidad_por_planeta(generador_planeta_mineral: Generator[PlanetaMineral, None, None],
                               generador_planetas: Generator[Planeta, None, None], id_mineral: int
                               ) -> Generator[Tuple[str, int, float], None, None]:
    lista_p_min = list(generador_planeta_mineral)
    planeta_actual = [None, None, 0.0]
    while True:
        try:
            planeta = next(generador_planetas)
        except StopIteration:
            return None
        planeta_actual[0] = planeta.nombre
        planeta_actual[1] = planeta.id_planeta
        for p_mineral in lista_p_min:
            if p_mineral.id_planeta == planeta_actual[1] and p_mineral.id_mineral == id_mineral:
                planeta_actual[2] += p_mineral.cantidad_disponible
        yield (planeta_actual[0], planeta_actual[1], planeta_actual[2])
        planeta_actual = [None, None, 0.0]


def misiones_por_tipo_planeta(generador_misiones: Generator[Mision, None, None],
                              generador_planetas: Generator[Planeta, None, None], tipo: str
                              ) -> Generator[Mision, None, None]:
    planetas = []
    for planeta in generador_planetas:
        if planeta.tipo == tipo:
            planetas.append(planeta)
    while True:
        try:
            mision = next(generador_misiones)
        except StopIteration:
            break
        for planeta in planetas:
            if mision.id_planeta == planeta.id_planeta and planeta.tipo == tipo:
                if mision.lograda is not None:
                    yield mision


def naves_pueden_llevar(generador_naves: Generator[Nave, None, None],
                        generador_planeta_mineral: Generator[PlanetaMineral, None, None],
                        id_planeta: int) -> Generator[tuple[str, int, float], None, None]:
    lista_p_minerales = list(generador_planeta_mineral)
    p_minerales_por_id = filter(lambda fila: fila[0] == id_planeta, lista_p_minerales)
    p_minerales = list(p_minerales_por_id)
    while True:
        try:
            nave = next(generador_naves)
        except StopIteration:
            return None
        for p_mineral in p_minerales:
            cantidad = 100*nave.capacidad_minerales/p_mineral.cantidad_disponible
            if cantidad > 100:
                se_lleva = 100
            elif cantidad < 0:
                se_lleva = 0.00
            else:
                se_lleva = cantidad
            yield (nave.patente, p_mineral.id_mineral, round(se_lleva, 2))


def planetas_por_estadisticas(generador_mineral: Generator[Mineral, None, None],
                              generador_planeta_mineral: Generator[PlanetaMineral, None, None],
                              generador_planeta: Generator[Planeta, None, None],
                              moles_elemento_min: float, concentracion_molar_min: float,
                              densidad_min: float) -> Generator[Planeta, None, None]:
    lista_p_minerales = list(generador_planeta_mineral)
    lista_minerales = list(generador_mineral)
    minerales_por_id = {mineral.id_mineral: mineral for mineral in lista_minerales}

    p_mineral_por_planeta = defaultdict(list)
    for p_mineral in lista_p_minerales:
        p_mineral_por_planeta[p_mineral.id_planeta].append(p_mineral)

    while True:
        try:
            planeta = next(generador_planeta)
        except StopIteration:
            return None
        volumen_planeta = (4/3)*pi*(radio_planeta(planeta.id_planeta, planeta.tamano))**3
        p_minerales = p_mineral_por_planeta.get(planeta.id_planeta)

        for p_mineral in p_minerales:
            pasa = [None, None, None]
            mineral = minerales_por_id[p_mineral.id_mineral]
            cantidad = p_mineral.cantidad_disponible*p_mineral.pureza
            moles = cantidad*1000000/mineral.masa_atomica
            c_molar = cantidad*1000000/(volumen_planeta*mineral.masa_atomica)
            densidad = cantidad*1000000/volumen_planeta

            if moles_elemento_min is not None:
                if moles >= moles_elemento_min:
                    pasa[0] = True
                else:
                    pasa[0] = False
            if concentracion_molar_min is not None:
                if c_molar >= concentracion_molar_min:
                    pasa[1] = True
                else:
                    pasa[1] = False
            if densidad_min is not None:
                if densidad > densidad_min:
                    pasa[2] = True
                else:
                    pasa[2] = False
            else:
                pass
            if False not in pasa:
                yield planeta
                break


def ganancias_potenciales_por_planeta(generador_minerales: Generator[Mineral, None, None],
                                      generador_planeta_mineral: Generator[PlanetaMineral,
                                                                           None, None],
                                      generador_planetas: Generator[Planeta, None, None],
                                      precios: dict) -> dict:
    dict_planetas = {}
    lista_p_minerales = list(generador_planeta_mineral)
    lista_minerales = list(generador_minerales)
    dict_minerales = {mineral.id_mineral: mineral for mineral in lista_minerales}

    p_mineral_por_planeta = {}
    for p_mineral in lista_p_minerales:
        p_mineral_por_planeta.setdefault(p_mineral.id_planeta, []).append(p_mineral)

    while True:
        try:
            planeta = next(generador_planetas)
        except StopIteration:
            break
        valor_potencial = 0
        p_minerales = p_mineral_por_planeta.get(planeta.id_planeta, [])
        for p_mineral in p_minerales:
            mineral = dict_minerales[p_mineral.id_mineral]
            valor = precios.get(mineral.nombre, 0.0)
            if valor is None:
                valor = 0.0
            valor_potencial += valor * (p_mineral.cantidad_disponible*p_mineral.pureza)
        dict_planetas[planeta.id_planeta] = valor_potencial

    return dict_planetas
