"""
Módulo para la lectura, procesamiento y agrupamiento de los registros
del catálogo de satélites en formato JSON
"""

import json

# Diccionario de prefijos de nombres a nombres de grupo normalizados
GRUPOS = {
    "STARLINK": "Starlink",
    "ONEWEB": "OneWeb",
    "KUIPER": "Kuiper",
    "QIANFAN": "Qianfan",
    "IRIDIUM": "Iridium",
    "GLOBALSTAR": "Globalstar",
    "NAVSTAR": "GPS",
    "BEIDOU": "BeiDou"
}


def leer_satelites(ruta: str) -> list:
    """
    Lee un JSON con los datos de satélites con UTF-8.
    Si el archivo no existe, imprime un aviso y devuelve una lista vacía
    """
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            registros = json.load(archivo)
            return registros
    except FileNotFoundError:
        print(f"Aviso: El archivo en '{ruta}' no fue encontrado.")
        return []


def ano_lanzamiento(registro: dict) -> int:
    """
    Obtiene el año de lanzamiento del satélite a partir de los
    primeros 4 caracteres de su clave 'OBJECT_ID'
    """
    object_id = registro.get("OBJECT_ID", "")
    return int(object_id[:4])


def grupo(nombre: str) -> str:
    """
    Devuelve el grupo al que pertenece un satélite según el prefijo de su nombre.
    Si no coincide con ningún prefijo, devuelve "Otros"
    """
    nombre_mayuscula = nombre.upper()
    for prefijo, nombre_grupo in GRUPOS.items():
        if nombre_mayuscula.startswith(prefijo):
            return nombre_grupo
    return "Otros"


def contar_por_grupo(registros: list) -> dict:
    """
    Cuenta cuántos satélites pertenecen a cada grupo en la lista de registros
    Devuelve un diccionario 
    """
    conteo = {}
    for r in registros:
        nombre = r.get("OBJECT_NAME", "")
        grp = grupo(nombre)
        conteo[grp] = conteo.get(grp, 0) + 1
    return conteo


def lanzamientos_por_ano(registros: list) -> dict:
    """
    Cuenta la cantidad de satélites activos lanzados por año
    Devuelve un diccionario 
    """
    lanzamientos = {}
    for r in registros:
        ano = ano_lanzamiento(r)
        lanzamientos[ano] = lanzamientos.get(ano, 0) + 1
    return lanzamientos


if __name__ == "__main__":
    # Bloque de prueba local: no se ejecuta al ser importado desde otro módulo
    datos = leer_satelites("datos/satelites.json")
    print(f"Total registros cargados: {len(datos)}")
    
    if datos:
        print(f"Ejemplo ano_lanzamiento (satélite 0): {ano_lanzamiento(datos[0])}")
        print("Conteo por grupo:", contar_por_grupo(datos))
        lanz = lanzamientos_por_ano(datos)
        print("Lanzamientos en 2024:", lanz.get(2024, 0))