import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from netCDF4 import Dataset, num2date

def listar_archivos_nc(carpeta_entrada):
    return [f for f in os.listdir(carpeta_entrada) if f.endswith('.nc')]

def corregir_datos(df, variable):
    """Corrige datos faltantes o volados por interpolación lineal."""
    if variable in df.columns:
        df[variable] = df[variable].replace([np.inf, -np.inf], np.nan).interpolate(
            method='linear', limit_direction='both')
    return df

def procesar_archivo_individual(nombre_archivo, carpeta_entrada, carpeta_salida_general, log_callback=None):
    ruta_nc = os.path.join(carpeta_entrada, nombre_archivo)
    match = re.search(r'(\d{4})_(\d{2})', nombre_archivo)
    if not match:
        return
    año, mes = match.group(1), match.group(2)
    carpeta_salida = os.path.join(carpeta_salida_general, f"{año}_{mes}")
    os.makedirs(carpeta_salida, exist_ok=True)

    nc = Dataset(ruta_nc, mode='r')
    latitudes = nc.variables['latitude'][:]
    longitudes = nc.variables['longitude'][:]
    fechas_raw = num2date(nc.variables['valid_time'][:], nc.variables['valid_time'].units)
    fechas = [datetime(f.year, f.month, f.day, f.hour, f.minute, f.second) for f in fechas_raw]
    fechas = pd.to_datetime(fechas)

    mx2t = np.round(nc.variables['mx2t'][:] - 273.15, 2).reshape(len(fechas), -1)
    mn2t = np.round(nc.variables['mn2t'][:] - 273.15, 2).reshape(len(fechas), -1)
    tp = np.round(nc.variables['tp'][:] * 1000, 2).reshape(len(fechas), -1)

    lat_grid, lon_grid = np.meshgrid(latitudes, longitudes, indexing='ij')
    lat_flat = lat_grid.flatten()
    lon_flat = lon_grid.flatten()

    for idx, (lat, lon) in enumerate(zip(lat_flat, lon_flat)):
        nombre_base = f"lat{lat:.2f}_lon{lon:.2f}".replace('.', '_')
        carpeta_h = os.path.join(carpeta_salida, 'horario', nombre_base)
        carpeta_d = os.path.join(carpeta_salida, 'diario', nombre_base)
        os.makedirs(os.path.join(carpeta_h, 'figuras'), exist_ok=True)
        os.makedirs(os.path.join(carpeta_d, 'figuras'), exist_ok=True)

        df = pd.DataFrame({
            'Fecha': fechas,
            'mx2t_C': mx2t[:, idx],
            'mn2t_C': mn2t[:, idx],
            'tp_mm': tp[:, idx]
        })

        # Corrección solo para precipitación
        df = corregir_datos(df, 'tp_mm')

        # Guardar horario
        df.to_csv(os.path.join(carpeta_h, f"{nombre_base}_horario.txt"), sep='\t', index=False)
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(df['Fecha'].to_numpy(), df['mx2t_C'].to_numpy(), label='Max Temp')
        ax.plot(df['Fecha'].to_numpy(), df['mn2t_C'].to_numpy(), label='Min Temp')
        ax.plot(df['Fecha'].to_numpy(), df['tp_mm'].to_numpy(), label='Precipitación')
        ax.set_title(f"Horario - {nombre_base}")
        ax.legend()
        fig.autofmt_xdate()
        fig.savefig(os.path.join(carpeta_h, 'figuras', f"{nombre_base}_horaria.png"))
        plt.close()

        # Diario
        df_diario = df.resample('D', on='Fecha').mean().reset_index()
        df_diario.to_csv(os.path.join(carpeta_d, f"{nombre_base}_diario.txt"), sep=';', index=False)
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(df_diario['Fecha'].to_numpy(), df_diario['mx2t_C'].to_numpy(), label='Max Temp')
        ax.plot(df_diario['Fecha'].to_numpy(), df_diario['mn2t_C'].to_numpy(), label='Min Temp')
        ax.plot(df_diario['Fecha'].to_numpy(), df_diario['tp_mm'].to_numpy(), label='Precipitación')
        ax.set_title(f"Diario - {nombre_base}")
        ax.legend()
        fig.autofmt_xdate()
        fig.savefig(os.path.join(carpeta_d, 'figuras', f"{nombre_base}_diario.png"))
        plt.close()

    nc.close()
    if log_callback:
        log_callback(f"✅ Procesado: {nombre_archivo}")
