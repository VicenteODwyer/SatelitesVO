"""
Módulo con funciones de análisis, estadísticas, filtrado x zona
y ordenamiento sobre colecciones de objetos Satelite
"""

from catalogo import grupo


def contar_por_tipo(satelites: list) -> dict:
    """
    Cuenta satélites por tipo de órbita (LEO, MEO, GEO, HEO).
    Garantiza que las cuatro claves estén presentes en el diccionario resultante.
    """
    conteo = {"LEO": 0, "MEO": 0, "GEO": 0, "HEO": 0}
    for sat in satelites:
        tipo = sat.tipo_orbita()
        if tipo in conteo:
            conteo[tipo] += 1
    return conteo


def mas_bajo(satelites: list):
    """
    Devuelve el objeto Satelite con la menor altitud
    Retorna None si la lista está vacía
    """
    if not satelites:
        return None
    return min(satelites, key=lambda s: s.altitud_km)


def mas_alto(satelites: list):
    """
    Devuelve el objeto Satelite con la mayor altitud
    Retorna None si la lista está vacía
    """
    if not satelites:
        return None
    return max(satelites, key=lambda s: s.altitud_km)


def en_zona(satelites: list, zona: tuple) -> list:
    """
    Filtra y devuelve una lista con los satélites que están dentro de la zona dada
    """
    return [s for s in satelites if s.esta_en_zona(zona)]


def ordenar_por(satelites: list, atributo: str, descendente: bool = False) -> list:
    """
    Devuelve una nueva lista de satélites ordenada por el atributo especificado
    (por ejemplo: 'altitud_km', 'nombre', 'latitud')
    """
    return sorted(satelites, key=lambda s: getattr(s, atributo), reverse=descendente)


def top_n(satelites: list, n: int, mas_altos: bool = True) -> list:
    """
    Devuelve los n satélites más altos o más bajos reutilizando ordenar_por
    """
    # Si busca los más altos, orden descendente; si busca los más bajos, ascendente
    ordenados = ordenar_por(satelites, "altitud_km", descendente=mas_altos)
    return ordenados[:n]


def resumen_por_grupo(satelites: list) -> dict:
    """
    Genera un dic con estadísticas de altitud por grupo de satélites:
    cantidad, altitud mínima, media y máxima (sin redondear)
    """
    agrupados = {}
    for s in satelites:
        grp = grupo(s.nombre)
        if grp not in agrupados:
            agrupados[grp] = []
        agrupados[grp].append(s.altitud_km)

    resumen = {}
    for grp, altitudes in agrupados.items():
        resumen[grp] = {
            "cantidad": len(altitudes),
            "minima": min(altitudes),
            "media": sum(altitudes) / len(altitudes),
            "maxima": max(altitudes)
        }
    return resumen


if __name__ == "__main__":
    from satelite import Satelite

    print("Test de unidad: analisis.py")
    
    # 1. Prueba con lista vacía (casos borde)
    print("Conteo lista vacía:", contar_por_tipo([]))
    print("Más bajo en lista vacía:", mas_bajo([]))

    # 2. Prueba con satélites sintéticos
    s1 = Satelite("STARLINK-101", -40.0, -70.0, 550.0)
    s2 = Satelite("STARLINK-102", -42.0, -71.0, 560.0)
    s3 = Satelite("BEIDOU-M1", 10.0, 20.0, 21500.0)
    s4 = Satelite("GEO-TEST", 0.0, -50.0, 35786.0)
    muestra = [s1, s2, s3, s4]

    print("Conteo tipos:", contar_por_tipo(muestra))
    print("Más bajo:", mas_bajo(muestra))
    print("Más alto:", mas_alto(muestra))

    bariloche = (-76.30, -46.13, -66.30, -36.13)
    en_bari = en_zona(muestra, bariloche)
    print(f"En Bariloche ({len(en_bari)}):", [s.nombre for s in en_bari])

    print("Top 2 más altos:", [s.nombre for s in top_n(muestra, 2, mas_altos=True)])
    print("Top 2 más bajos:", [s.nombre for s in top_n(muestra, 2, mas_altos=False)])
    print("Resumen Starlink:", resumen_por_grupo(muestra).get("Starlink"))