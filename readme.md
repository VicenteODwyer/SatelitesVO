# Seguimiento y caracterización de satélites

## Integrante
- **Vicente O'Dwyer**

## Tareas realizadas
- Implementación de lectura, conteos y filtros del catálogo en `catalogo.py`.
- Implementación de la clase `Satelite` y descarte por altitud en `satelite.py`.
- Implementación de métricas, ordenamiento genérico y zonas en `analisis.py`.
- Implementación de funciones de visualización estadística y dispersión geográfica 2D en `graficos.py`.
- Elaboración y ejecución del informe completo (Etapa 1, Etapa 2 y análisis tabular con `pandas`) en `informe.ipynb`.

## Cómo correr el proyecto

1. Activar el entorno virtual:
   - En Windows: `.venv\Scripts\activate`
   - En Linux/macOS: `source .venv/bin/activate`

2. Instalar dependencias (si no se hizo previamente):
   ```bash
   pip install --no-deps skyfield sgp4 jplephem certifi
   pip install numpy matplotlib pandas jupyter

3. Abrir y ejecutar el notebook:
   * Desde terminal: `python -m jupyterlab` (o `python -m notebook`)
   * Desde VS Code: abrir `informe.ipynb` y seleccionar el kernel `.venv`
   * Ejecutar todas las celdas desde el menú **Kernel > Restart & Run All**