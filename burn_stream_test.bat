@echo off
REM Simple wrapper to test GDAL CreateCopy using burn_stream_test.py
REM Usage: burn_stream_test.bat input_dem.tif output_dem.tif

if "%~2"=="" (
  echo Usage: %~nx0 input_dem.tif output_dem.tif
  exit /b 1
)

REM Adjust PYTHON_EXE if QGIS Python is required
set PYTHON_EXE=python
"%PYTHON_EXE%" "%~dp0burn_stream_test.py" "%~1" "%~2"
