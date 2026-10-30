Seguimiento y caracterización de satélites — Etapa 1


## Integrante
* **Vicente O'Dwyer** 

## Tareas realizadas
* Implementación de lectura, conteos y filtros del catálogo en `catalogo.py`.
* Implementación de la clase `Satelite` y descarte por altitud en `satelite.py`
* Implementación de métricas, ordenamiento genérico y zonas en `analisis.py`
* Elaboración y ejecución del informe completo en `informe.ipynb`

## Cómo correr el proyecto

1. Activar el entorno virtual:
   * En Windows: `.venv\Scripts\activate`
   * En Linux/macOS: `source .venv/bin/activate`

2. Instalar dependencias satelitales (si no se hizo previamente):
   ```bash
   pip install --no-deps skyfield sgp4 jplephem certifi
   ```

3. Abrir y ejecutar el notebook:
   * Desde terminal: `python -m jupyterlab` (o `python -m notebook`)
   * Desde VS Code: abrir `informe.ipynb` y seleccionar el kernel `.venv`
   * Ejecutar todas las celdas desde el menú **Kernel > Restart & Run All**