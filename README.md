# GDAL burn stream test

Este repositorio proporciona un script de prueba `burn_stream_test.py` para replicar el paso de copia de burnStream utilizando la función `CreateCopy` de GDAL.

## Uso

```bash
python burn_stream_test.py <input_dem> <output_dem>
```

El script intenta copiar el DEM de entrada a un nuevo archivo GeoTIFF. Si `CreateCopy` falla, realiza una copia de respaldo usando `shutil.copy`.

