"""
Módulo de visualización y generación de gráficos estadísticos
para la caracterización de satélites artificiales (Etapa 2)
"""

import matplotlib.pyplot as plt
import numpy as np
from catalogo import grupo


def graficar_lanzamientos(lanzamientos: dict, desde: int = 1990, hasta: int = 2026):
    """
    Genera un gráfico de barras con la cantidad de satélites lanzados por año
    dentro del rango especificado
    """
    anios = [a for a in range(desde, hasta + 1)]
    cantidades = [lanzamientos.get(a, 0) for a in anios]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(anios, cantidades, color="#2b5c8f", edgecolor="black", linewidth=0.5)
    ax.set_title(f"Satélites activos lanzados por año ({desde}-{hasta})", fontsize=13)
    ax.set_xlabel("Año de lanzamiento", fontsize=11)
    ax.set_ylabel("Cantidad de satélites", fontsize=11)
    ax.grid(axis="y", linestyle="--", alpha=0.6)
    plt.tight_layout()
    return fig, ax


def graficar_lanzamientos_apilados(
    datos1: dict, datos2: dict, etiqueta1: str, etiqueta2: str, desde: int = 1990, hasta: int = 2026
):
    """
    Genera un gráfico de barras apiladas comparando dos series de lanzamientos por año.
    Los años faltantes en cualquiera de los diccionarios se consideran con valor 0
    """
    anios = [a for a in range(desde, hasta + 1)]
    valores1 = np.array([datos1.get(a, 0) for a in anios])
    valores2 = np.array([datos2.get(a, 0) for a in anios])

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.bar(anios, valores1, label=etiqueta1, color="#1f77b4", edgecolor="black", linewidth=0.5)
    ax.bar(anios, valores2, bottom=valores1, label=etiqueta2, color="#ff7f0e", edgecolor="black", linewidth=0.5)

    ax.set_title(f"Comparación de lanzamientos: {etiqueta1} vs. {etiqueta2} ({desde}-{hasta})", fontsize=13)
    ax.set_xlabel("Año de lanzamiento", fontsize=11)
    ax.set_ylabel("Cantidad de satélites", fontsize=11)
    ax.legend(fontsize=10)
    ax.grid(axis="y", linestyle="--", alpha=0.6)
    plt.tight_layout()
    return fig, ax


def graficar_altitud_media_por_grupo(resumen: dict):
    """
    Genera un gráfico de barras con la altitud media (km) calculada para cada grupo
    Ordena los grupos de menor a mayor altitud media 
    """
    # Ordenamos por altitud media
    items_ordenados = sorted(resumen.items(), key=lambda x: x[1]["media"])
    grupos = [item[0] for item in items_ordenados]
    medias = [item[1]["media"] for item in items_ordenados]

    fig, ax = plt.subplots(figsize=(10, 5))
    barras = ax.bar(grupos, medias, color="#3a9278", edgecolor="black", linewidth=0.6)

    ax.set_title("Altitud media por grupo de satélites", fontsize=13)
    ax.set_xlabel("Grupo", fontsize=11)
    ax.set_ylabel("Altitud media (km)", fontsize=11)
    plt.xticks(rotation=30, ha="right")
    ax.grid(axis="y", linestyle="--", alpha=0.6)

    # Etiqueta con el valor numérico arriba de cada barra
    for barra in barras:
        alto = barra.get_height()
        ax.annotate(
            f"{alto:.0f} km",
            xy=(barra.get_x() + barra.get_width() / 2, alto),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8,
        )

    plt.tight_layout()
    return fig, ax


def graficar_histograma_leo(satelites: list, ancho_bin: int = 50):
    """
    Genera un histograma de las altitudes en órbita baja (entre 200 y 2.000 km)
    utilizando bins con el ancho indicado por ancho_bin
    """
    altitudes_leo = [s.altitud_km for s in satelites if 200.0 <= s.altitud_km <= 2000.0]
    bins = np.arange(200, 2000 + ancho_bin, ancho_bin)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(altitudes_leo, bins=bins, color="#4a7c59", edgecolor="black", linewidth=0.5)

    ax.set_title(f"Distribución de altitudes en órbita baja (LEO) — Bins de {ancho_bin} km", fontsize=13)
    ax.set_xlabel("Altitud (km)", fontsize=11)
    ax.set_ylabel("Cantidad de satélites", fontsize=11)
    ax.grid(axis="y", linestyle="--", alpha=0.6)
    plt.tight_layout()
    return fig, ax


def graficar_histograma_altitudes_log(satelites: list):
    """
    Genera un histograma de todas las altitudes de los satélites activos
    utilizando una escala logarítmica en el eje X y bins de ancho logarítmico
    """
    altitudes = [s.altitud_km for s in satelites if s.altitud_km > 0]
    min_alt = max(min(altitudes), 100.0)
    max_alt = max(altitudes)
    bins = np.logspace(np.log10(min_alt), np.log10(max_alt), num=60)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(altitudes, bins=bins, color="#6b4c9a", edgecolor="black", linewidth=0.5)
    ax.set_xscale("log")

    ax.set_title("Distribución global de altitudes (Escala logarítmica)", fontsize=13)
    ax.set_xlabel("Altitud (km) [Escala logarítmica]", fontsize=11)
    ax.set_ylabel("Cantidad de satélites", fontsize=11)
    ax.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.tight_layout()
    return fig, ax


def graficar_histograma_inclinaciones(registros: list, grupo_filtro: str = None):
    """
    Genera un histograma de la inclinación orbital (0° a 180°)
    Permite filtrar opcionalmente por un grupo específico (ej. 'Starlink', 'GPS')
    """
    if grupo_filtro:
        inclinaciones = [
            float(r["INCLINATION"])
            for r in registros
            if "INCLINATION" in r and grupo(r.get("OBJECT_NAME", "")) == grupo_filtro
        ]
        titulo = f"Distribución de inclinación orbital — {grupo_filtro} (0° a 180°)"
        color = "#e66101"
    else:
        inclinaciones = [float(r["INCLINATION"]) for r in registros if "INCLINATION" in r]
        titulo = "Distribución de inclinación orbital de todos los satélites (0° a 180°)"
        color = "#5e3c99"

    bins = np.arange(0, 181, 1)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(inclinaciones, bins=bins, color=color, edgecolor="none", alpha=0.8)

    ax.set_title(titulo, fontsize=13)
    ax.set_xlabel("Inclinación (°)", fontsize=11)
    ax.set_ylabel("Cantidad de satélites", fontsize=11)
    ax.set_xlim(0, 180)
    ax.grid(axis="y", linestyle="--", alpha=0.6)
    plt.tight_layout()
    return fig, ax


def graficar_distribucion_geografica(satelites: list):
    """
    Tema libre: Gráfico de dispersión 2D (Longitud vs. Latitud) instantáneo.
    Compara la distribución espacial de satélites LEO vs. GEO usando transparencia
    para evidenciar las concentraciones y la línea ecuatorial geoestacionaria.
    """
    # Filtramos coordenadas por tipo de órbita
    leo_lons = [s.longitud for s in satelites if s.tipo_orbita() == "LEO"]
    leo_lats = [s.latitud for s in satelites if s.tipo_orbita() == "LEO"]

    geo_lons = [s.longitud for s in satelites if s.tipo_orbita() == "GEO"]
    geo_lats = [s.latitud for s in satelites if s.tipo_orbita() == "GEO"]

    fig, ax = plt.subplots(figsize=(12, 6))

    # Puntos LEO con transparencia para apreciar el amontonamiento por latitud
    ax.scatter(leo_lons, leo_lats, color="#1f77b4", alpha=0.25, s=6, label=f"LEO ({len(leo_lons)} satélites)")

    # Puntos GEO en color contrastante sobre el ecuador
    ax.scatter(geo_lons, geo_lats, color="#d62728", alpha=0.8, s=16, label=f"GEO ({len(geo_lons)} satélites)")

    ax.set_title("Tema libre: Distribución espacial instantánea (LEO vs. GEO)", fontsize=13)
    ax.set_xlabel("Longitud (°)", fontsize=11)
    ax.set_ylabel("Latitud (°)", fontsize=11)
    ax.set_xlim(-180, 180)
    ax.set_ylim(-90, 90)

    # Línea de referencia ecuatorial (latitud 0)
    ax.axhline(0, color="black", linestyle=":", linewidth=0.8, alpha=0.7)

    ax.legend(loc="lower left", fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    return fig, ax


if __name__ == "__main__":
    # Prueba rápida de import y ejecución local
    print("Módulo graficos.py cargado correctamente sin errores.")