
import os
import pandas as pd
import glob
import numpy as np
from datetime import datetime
from netCDF4 import Dataset

def extraer_elevacion_desde_nc(carpeta_origen):
    archivos_nc = glob.glob(os.path.join(carpeta_origen, "*.nc"))
    elevaciones = []
    for archivo in archivos_nc:
        try:
            nc = Dataset(archivo)
            if "elevation" in nc.variables:
                elev = nc.variables["elevation"][:]
                if hasattr(elev, "mean"):
                    elevaciones.append(float(elev.mean()))
            nc.close()
        except Exception:
            continue
    if elevaciones:
        return sum(elevaciones) / len(elevaciones)
    return None

def calcular_centroide_coordenadas(carpeta_origen):
    latitudes = []
    longitudes = []
    carpetas = glob.glob(os.path.join(carpeta_origen, "**", "lat-*lon-*"), recursive=True)
    for path in carpetas:
        folder = os.path.basename(path)
        try:
            lat_str = folder.split("_")[0].replace("lat-", "").replace("_", ".")
            lon_str = folder.split("_")[1].replace("lon-", "").replace("_", ".")
            latitudes.append(float(lat_str.replace(",", ".")))
            longitudes.append(float(lon_str.replace(",", ".")))
        except:
            continue
    if latitudes and longitudes:
        return round(np.mean(latitudes), 2), round(np.mean(longitudes), 2)
    else:
        return 0.0, 0.0

def procesar_txts_promedio(carpeta_origen):
    archivos_diarios = glob.glob(os.path.join(carpeta_origen, "**", "*_diario.txt"), recursive=True)
    if not archivos_diarios:
        raise FileNotFoundError("No se encontraron archivos *_diario.txt")

    lista_df = []

    for archivo in archivos_diarios:
        try:
            df = pd.read_csv(archivo, sep=";", parse_dates=["Fecha"])
            if {'mx2t_C', 'mn2t_C', 'tp_mm'}.issubset(df.columns):
                df['TempMedia'] = (df['mx2t_C'] + df['mn2t_C']) / 2
                df_filtrado = df[['Fecha', 'TempMedia', 'tp_mm']].copy()
                lista_df.append(df_filtrado)
        except Exception:
            continue

    if not lista_df:
        raise ValueError("No se pudo procesar ningún archivo diario válido.")

    df_concatenado = pd.concat(lista_df)
    df_promedio = df_concatenado.groupby('Fecha').mean().reset_index()

    return df_promedio

def exportar_archivos_swat(nombre_proyecto, carpeta_origen, carpeta_destino):
    climate_dir = os.path.join(carpeta_destino, f"Climate{nombre_proyecto}")
    os.makedirs(climate_dir, exist_ok=True)

    elevacion = extraer_elevacion_desde_nc(carpeta_origen)
    if elevacion is None:
        elevacion = 1790.0
        print("⚠ Elevación no encontrada. Se usará el valor por defecto: 1790.0 m")
    else:
        print(f"✅ Elevación promedio: {elevacion:.2f} m")

    lat_prom, lon_prom = calcular_centroide_coordenadas(carpeta_origen)
    print(f"📍 Centroide estimado: LAT={lat_prom}, LON={lon_prom}")

    df_clima = procesar_txts_promedio(carpeta_origen)
    if df_clima.empty:
        raise ValueError("Data climática promedio está vacía.")

    fecha_inicial = df_clima.iloc[0]['Fecha'].strftime('%Y%m%d')
    base_name = nombre_proyecto[:3].lower()

    robpcp_path = os.path.join(climate_dir, f"{base_name}pcp.txt")
    robtmp_path = os.path.join(climate_dir, f"{base_name}tmp.txt")

    with open(robpcp_path, "w") as f:
        f.write(f"{fecha_inicial}\n")
        for val in df_clima['tp_mm']:
            f.write(f"{round(val, 2)}\n")

    with open(robtmp_path, "w") as f:
        f.write(f"{fecha_inicial}\n")
        for val in df_clima['TempMedia']:
            f.write(f"{round(val, 2)}\n")

    pcp_path = os.path.join(climate_dir, "pcp.txt")
    tmp_path = os.path.join(climate_dir, "tmp.txt")

    with open(pcp_path, "w") as f:
        f.write("ID,NAME,LAT,LONG,ELEVATION\n")
        f.write(f"1,{base_name}pcp,{lat_prom},{lon_prom},{elevacion:.3f}\n")

    with open(tmp_path, "w") as f:
        f.write("ID,NAME,LAT,LONG,ELEVATION\n")
        f.write(f"1,{base_name}tmp,{lat_prom},{lon_prom},{elevacion:.3f}\n")
