@echo off
REM Ejecuta burn_stream_test.py con rutas predefinidas
REM Ajustar si es necesario para otros datos

set "DEM=C:\Users\jhonv\Downloads\robit_data\rasters\srtm_30m\hdr.adf"
set "BURN=C:\Users\jhonv\Downloads\robit_data\rasters\srtm_30m\hdr_burned.tif"
REM Archivo de red hídrica (no utilizado en esta prueba de copia)
set "STREAM=C:\Users\jhonv\Downloads\robit_data\shapefiles\robReach.shp"

REM Ajustar PYTHON_EXE si se requiere el Python de QGIS
set PYTHON_EXE=python
"%PYTHON_EXE%" "%~dp0burn_stream_test.py" "%DEM%" "%BURN%"

echo.
echo Se intentó copiar %DEM% a %BURN%
pause
