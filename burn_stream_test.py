#!/usr/bin/env python
"""Minimal test for GDAL CreateCopy to replicate burnStream copying step."""
import sys
import os
from osgeo import gdal
import shutil


def main(dem_path: str, burn_path: str) -> int:
    gdal.UseExceptions()
    dem_path = os.path.normpath(dem_path)
    burn_path = os.path.normpath(burn_path)

    dem_ds = gdal.Open(dem_path, gdal.GA_ReadOnly)
    if dem_ds is None:
        print(f"Could not open DEM {dem_path}")
        return 1
    driver = gdal.GetDriverByName("GTiff")
    if driver is None:
        print("GTiff driver not available")
        return 1
    try:
        burn_ds = driver.CreateCopy(burn_path, dem_ds, 0, options=["BIGTIFF=YES"])
    except RuntimeError as e:
        print(f"CreateCopy failed: {e}")
        print(f"GDAL error {gdal.GetLastErrorType()}: {gdal.GetLastErrorMsg()}")
        print("Attempting shutil.copy as fallback...")
        try:
            shutil.copy(dem_path, burn_path)
            print("Fallback copy succeeded")
            return 0
        except Exception as ex:
            print(f"Fallback copy failed: {ex}")
            return 1
    if burn_ds is None:
        print("CreateCopy returned None")
        return 1
    burn_ds = None
    dem_ds = None
    print("CreateCopy succeeded")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: burn_stream_test.py <input_dem> <output_dem>")
        sys.exit(1)
    sys.exit(main(sys.argv[1], sys.argv[2]))
