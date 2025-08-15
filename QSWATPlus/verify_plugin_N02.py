from osgeo import gdal
import os

def check_gdal():
    print("🔎 Verificando GDAL...")
    print(f"GDAL version: {gdal.__version__}")
    driver = gdal.GetDriverByName('GTiff')
    if driver is None:
        print("❌ Driver GTiff no encontrado.")
        return False
    print("✅ Driver GTiff disponible.")
    return True

def test_create_copy(src_path, dst_path):
    print(f"🧪 Intentando copiar:\n  Origen: {src_path}\n  Destino: {dst_path}")
    
    if not os.path.exists(src_path):
        print("❌ Archivo DEM de origen no existe.")
        return

    ds = gdal.Open(src_path, gdal.GA_ReadOnly)
    if ds is None:
        print("❌ No se pudo abrir el DEM de origen.")
        return

    driver = gdal.GetDriverByName('GTiff')
    if driver is None:
        print("❌ No se encontró el driver GTiff.")
        return

    # Intentar crear copia
    out_ds = driver.CreateCopy(dst_path, ds, 0)
    if out_ds is not None:
        print("✅ Copia creada correctamente.")
        out_ds = None  # Cerrar
    else:
        print("❌ Error al crear la copia (CreateCopy falló).")
    ds = None

if __name__ == "__main__":
    if check_gdal():
        # Cambia estas rutas a un DEM válido en tu sistema
        dem_src = r"C:\SWATProject\robit06\Watershed\Rasters\DEM\srtm_30m.tif"
        dem_dst = r"C:\SWATProject\robit06\Watershed\Rasters\DEM\copia_test.tif"
        test_create_copy(dem_src, dem_dst)
