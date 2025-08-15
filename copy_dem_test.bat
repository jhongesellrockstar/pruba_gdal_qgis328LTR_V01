@echo off
REM Copia un DEM para probar si GDAL puede crear archivos GeoTIFF
REM Ajustar las rutas para su entorno antes de ejecutar


python - <<PY
import sys
from osgeo import gdal

dem_file = r"%DEM%"
copy_file = r"%COPIA%"
print(f"Copiando {dem_file} a {copy_file}")
dem = gdal.Open(dem_file, gdal.GA_ReadOnly)
if dem is None:
    print("No se pudo abrir el DEM de entrada")
    sys.exit(1)

driver = gdal.GetDriverByName('GTiff')
if driver is None:
    print("No se encontró el driver GTiff")
    sys.exit(1)

try:
    gdal.UseExceptions()
    out = driver.CreateCopy(copy_file, dem, 0)
except RuntimeError as e:
    print("Fallo al copiar el DEM:", e)
    sys.exit(1)

if out is None:
    print("CreateCopy devolvió None")
    sys.exit(1)
else:
    print("Archivo creado correctamente")
PY

pause
