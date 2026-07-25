from typing import Generator, Tuple
from utilidades import (Nave, Tripulacion, Planeta,
                        PlanetaMineral, Mision, MisionMineral)


def planetas_visitados_por_nave(generador_planetas: Generator[Planeta, None, None],
                                generador_misiones: Generator[Mision, None, None],
                                generador_tripulaciones: Generator[Tripulacion, None, None]
                                ) -> Generator[Tuple[str, str | None, int | None], None, None]:
    set_naves = set()
    lista_misiones = list(generador_misiones)
    lista_planetas = list(generador_planetas)

    planetas_por_id = {planeta.id_planeta: planeta for planeta in lista_planetas}

    while True:
        try:
            tripulacion = next(generador_tripulaciones)
        except StopIteration:
            break
        misiones = list(filter(lambda mineral: mineral.id_equipo == tripulacion.id_equipo,
                               lista_misiones))

        visito_planeta = False

        for mision in misiones:
            if mision.lograda is not None:
                planeta = planetas_por_id.get(mision.id_planeta)
                if planeta is not None:
                    set_naves.add((tripulacion.patente_nave, planeta.nombre, planeta.id_planeta))
                    visito_planeta = True
        if visito_planeta is False:
            set_naves.add((tripulacion.patente_nave, None, None))

    for nave in set_naves:
        yield nave


def mineral_por_nave(generador_tripulaciones: Generator[Tripulacion, None, None],
                     generador_misiones: Generator[Mision, None, None],
                     generador_misiones_mineral: Generator[MisionMineral, None, None]
                     ) -> Generator[Tuple[str, float], None, None]:

    dict_naves = {}
    lista_misiones = list(generador_misiones)
    lista_m_minerales = list(generador_misiones_mineral)

    m_mineral_por_id_m = {}
    for m_mineral in lista_m_minerales:
        m_mineral_por_id_m.setdefault(m_mineral.id_mision, []).append(m_mineral)

    misiones_por_equipo = {}
    for mision in lista_misiones:
        misiones_por_equipo.setdefault(mision.id_equipo, []).append(mision)

    while True:
        try:
            tripulacion = next(generador_tripulaciones)
        except StopIteration:
            break

        misiones = misiones_por_equipo.get(tripulacion.id_equipo, [])

        if tripulacion.patente_nave not in dict_naves:
            cantidad_recolectada = 0.0
            for mision in misiones:
                if mision.lograda is True:
                    minerales = m_mineral_por_id_m.get(mision.id_mision, [])
                    if minerales is not None:
                        cantidad_recolectada += sum(mineral.cantidad for mineral in minerales)
            dict_naves[tripulacion.patente_nave] = cantidad_recolectada

    for tupla in dict_naves.items():
        yield tupla


def porcentaje_extraccion(generador_tripulacion: Generator[Tripulacion, None, None],
                          generador_mision_mineral: Generator[MisionMineral, None, None],
                          generador_planeta_mineral: Generator[PlanetaMineral, None, None],
                          mision: Mision) -> Tuple[float, float]:

    if mision.lograda is False or mision.lograda is None:
        return (0.0, 0.0)

    lista_m_minerales = list(generador_mision_mineral)
    lista_tripulacion = list(generador_tripulacion)
    lista_p_minerales = list(generador_planeta_mineral)

    m_mineral_por_id_m = {}
    for m_mineral in lista_m_minerales:
        m_mineral_por_id_m.setdefault(m_mineral.id_mision, []).append(m_mineral)

    p_mineral_por_id_p = {}
    for p_mineral in lista_p_minerales:
        p_mineral_por_id_p.setdefault(p_mineral.id_planeta, []).append(p_mineral)

    minerales_extraidos = m_mineral_por_id_m.get(mision.id_mision, [])
    minerales_disponibles = p_mineral_por_id_p.get(mision.id_planeta, [])

    ids_ya_contados = []
    cantidad_extraida = 0.0
    cantidad_disponible = 0.0

    for mineral_d in minerales_disponibles:
        cantidad_disponible += mineral_d.cantidad_disponible * mineral_d.pureza

    for mineral_e in minerales_extraidos:
        for mineral_d in minerales_disponibles:
            if mineral_e.id_mineral == mineral_d.id_mineral:
                if mineral_e.id_mineral not in ids_ya_contados:
                    ids_ya_contados.append(mineral_e.id_mineral)
                    cantidad_extraida += mineral_e.cantidad

    n_tripulantes = len(list(filter(lambda tripulacion: tripulacion.id_equipo == mision.id_equipo,
                                    lista_tripulacion)))

    if cantidad_disponible != 0 and n_tripulantes != 0:
        porcentaje_extraido = (cantidad_extraida*100)/cantidad_disponible
        porcentaje_por_tripulante = porcentaje_extraido/n_tripulantes
        return (porcentaje_extraido, porcentaje_por_tripulante)
    else:
        return (0.0, 0.0)


def resultado_mision(mision: Mision, generador_naves: Generator[Nave, None, None],
                     generador_planeta_mineral: Generator[PlanetaMineral, None, None],
                     generador_tripulaciones: Generator[Tripulacion, None, None],
                     generador_mision_mineral: Generator[MisionMineral, None, None]) -> Mision:

    lista_naves = list(generador_naves)
    lista_p_minerales = list(generador_planeta_mineral)
    lista_tripulacion = list(generador_tripulaciones)
    lista_m_minerales = list(generador_mision_mineral)

    nave_por_patente = {nave.patente: nave for nave in lista_naves}

    p_mineral_por_id_p = {}
    for p_mineral in lista_p_minerales:
        p_mineral_por_id_p.setdefault(p_mineral.id_planeta, []).append(p_mineral)

    m_mineral_por_id_m = {}
    for m_mineral in lista_m_minerales:
        m_mineral_por_id_m.setdefault(m_mineral.id_mision, []).append(m_mineral)

    tripulantes_equipo = list(filter(lambda t: t.id_equipo == mision.id_equipo, lista_tripulacion))
    if not tripulantes_equipo:
        return mision._replace(lograda=False)

    patente = tripulantes_equipo[0].patente_nave
    nave = nave_por_patente.get(patente, None)
    if nave is None:
        return mision._replace(lograda=False)

    minerales_disponibles = p_mineral_por_id_p.get(mision.id_planeta, [])
    minerales_mision = m_mineral_por_id_m.get(mision.id_mision, [])

    m_puro_disponible_por_id = {}
    for p_mineral in minerales_disponibles:
        m_puro_disponible_por_id[p_mineral.id_mineral] = m_puro_disponible_por_id.get(p_mineral.id_mineral, 0.0) + (p_mineral.cantidad_disponible * p_mineral.pureza)

    for m_mineral in minerales_mision:
        if m_mineral.id_mineral == 1 and m_mineral.cantidad > 0:
            puro_planeta = m_puro_disponible_por_id.get(1, 0.0)
            if puro_planeta >= m_mineral.cantidad and m_mineral.cantidad < nave.capacidad_minerales:
                return mision._replace(lograda=True)
            break

    total_puro_objetivo = 0.0
    for m_mineral in minerales_mision:
        puro_planeta = m_puro_disponible_por_id.get(m_mineral.id_mineral, 0.0)
        if puro_planeta < m_mineral.cantidad:
            return mision._replace(lograda=False)
        total_puro_objetivo += m_mineral.cantidad

    if total_puro_objetivo < nave.capacidad_minerales:
        return mision._replace(lograda=True)
    else:
        return mision._replace(lograda=False)
