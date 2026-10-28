"""
Módulo que define la clase Satelite para representar la posición de un
satélite en un instante dado, yla función para crearlos a partir del catálogo
"""

from datetime import datetime
from funciones_base import crear_objeto_skyfield, obtener_posicion


class Satelite:
    """
    Representa un satélite artificial y su posición en un instante determinado
    """

    def __init__(self, nombre: str, latitud: float, longitud: float, altitud_km: float):
        """
        Guarda los cuatro datos como atributos del objeto.
        """
        self.nombre = nombre
        self.latitud = latitud
        self.longitud = longitud
        self.altitud_km = altitud_km

    def tipo_orbita(self) -> str:
        """
        Devuelve 'LEO', 'MEO', 'GEO' o 'HEO' según el rango de altitud:
        - LEO: menor a 2.000 km
        - MEO: de 2.000 km a menos de 34.000 km
        - GEO: de 34.000 km a 37.000 km
        - HEO: mayor a 37.000 km
        """
        if self.altitud_km < 2000:
            return "LEO"
        elif self.altitud_km < 34000:
            return "MEO"
        elif self.altitud_km <= 37000:
            return "GEO"
        else:
            return "HEO"

    def esta_en_zona(self, zona: tuple) -> bool:
        """
        Determina si el satélite está dentro del cuadro delimitado por
        (lon_min, lat_min, lon_max, lat_max). El borde cuenta como adentro
        """
        lon_min, lat_min, lon_max, lat_max = zona
        lon_valida = lon_min <= self.longitud <= lon_max
        lat_valida = lat_min <= self.latitud <= lat_max
        return lon_valida and lat_valida

    def __str__(self) -> str:
        """
        Representación en texto del satélite.
        Ejemplo: 'ISS (ZARYA) | LEO | 419.7 km'
        """
        return f"{self.nombre} | {self.tipo_orbita()} | {self.altitud_km:.1f} km"


def crear_satelites(registros: list, momento: datetime) -> list:
    """
    Devuelve una lista de objetos Satelite con su posición calculada en `momento`.
    Descarta aquellos satélites con altitud calculada menor a 100 km
    """
    satelites_creados = []
    
    for r in registros:
        nombre = r.get("OBJECT_NAME", "Desconocido")
        objeto_sky = crear_objeto_skyfield(r)
        lat, lon, alt = obtener_posicion(objeto_sky, momento)
        
        # Descartar satélites que ya cayeron o dan lecturas bajo atmósfera
        if alt >= 100.0:
            sat = Satelite(nombre, lat, lon, alt)
            satelites_creados.append(sat)
            
    return satelites_creados


if __name__ == "__main__":
    from datetime import timezone
    from catalogo import leer_satelites

    print("--- Test de unidad: satelite.py ---")
    
    # 1. Test básico de la clase
    iss = Satelite("ISS (ZARYA)", -41.1, -71.3, 419.734)
    print("Test __str__:", str(iss))
    print("Test tipo_orbita LEO:", iss.tipo_orbita())
    
    # Test bordes de órbitas
    geo_borde = Satelite("Test GEO", 0.0, 0.0, 34000.0)
    print("Test borde 34000 km (GEO):", geo_borde.tipo_orbita())
    
    # Test zona Bariloche
    bariloche = (-76.30, -46.13, -66.30, -36.13)
    print("¿ISS en Bariloche?:", iss.esta_en_zona(bariloche))

    # 2. Test con un subconjunto chico para verificar crear_satelites
    datos = leer_satelites("datos/satelites.json")
    if datos:
        ahora = datetime.now(timezone.utc)
        primeros_diez = crear_satelites(datos[:10], ahora)
        print(f"Objetos creados de muestra (10 registros): {len(primeros_diez)}")
        for s in primeros_diez[:3]:
            print("  ", s)