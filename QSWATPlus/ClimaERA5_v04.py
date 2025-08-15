import cdsapi
from datetime import datetime, timedelta

class ClimaERA5:
    def __init__(self):
        self.client = cdsapi.Client()

    def descargar_datos(self, ruta_salida, fecha_inicio, fecha_fin, area, variables, progress_callback=None):
        """
        Descarga datos climáticos de ERA5 según los parámetros seleccionados.

        :param ruta_salida: Ruta donde se guardará el archivo descargado.
        :param fecha_inicio: Fecha de inicio en formato 'YYYY-MM-DD'.
        :param fecha_fin: Fecha de fin en formato 'YYYY-MM-DD'.
        :param area: Lista con coordenadas [N, W, S, E].
        :param variables: Lista de variables a descargar.
        :param progress_callback: Función de callback para actualizar la barra de progreso.
        """
        try:
            start_date = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            end_date = datetime.strptime(fecha_fin, '%Y-%m-%d')
            current_date = start_date
            total_months = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month + 1
            month_count = 0

            while current_date <= end_date:
                year = current_date.year
                month = current_date.month
                next_month = current_date + timedelta(days=32)
                next_month = next_month.replace(day=1)

                self.client.retrieve(
                    'reanalysis-era5-single-levels',
                    {
                        'product_type': 'reanalysis',
                        'variable': variables,
                        'year': str(year),
                        'month': str(month).zfill(2),
                        'day': [str(d).zfill(2) for d in range(1, 32)],
                        'time': [f"{h:02d}:00" for h in range(24)],
                        'area': area,
                        'format': 'netcdf',
                    },
                    f"{ruta_salida}_{year}_{month}.nc"
                )

                current_date = next_month
                month_count += 1
                if progress_callback:
                    progress_callback(month_count / total_months * 100)

            return f"Datos descargados correctamente en {ruta_salida}"
        except Exception as e:
            return f"Error al descargar datos: {e}"