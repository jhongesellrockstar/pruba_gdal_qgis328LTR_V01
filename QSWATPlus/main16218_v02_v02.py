import sys
import os
import traceback
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from .SWATPlusIGP_v09_v02 import Ui_MainWindow
from .ClimaERA5_v04 import ClimaERA5
import NavegadorGio  # Importamos el módulo del visor web de Giovanni

class EmittingStream(QObject):
    textWritten = pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

class DownloadThread(QThread):
    progress = pyqtSignal(int)
    result = pyqtSignal(str)

    def __init__(self, ruta_salida, fecha_inicio, fecha_fin, area, variables):
        super().__init__()
        self.ruta_salida = ruta_salida
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.area = area
        self.variables = variables

    def run(self):
        try:
            clima = ClimaERA5()
            resultado = clima.descargar_datos(
                self.ruta_salida, self.fecha_inicio, self.fecha_fin, self.area, self.variables, self.update_progress
            )
            self.result.emit(resultado)
        except Exception as e:
            self.result.emit(f"Error: {str(e)}\n{traceback.format_exc()}")

    def update_progress(self, progress):
        self.progress.emit(int(progress))

class SWATApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.setup_logging()

        # Integrar el visor web de Giovanni
        self.navegador_gio = NavegadorGio.NavegadorGio(self.widget_browse_giovanni, self.pushButton_navegadorGPM)

    def setup_logging(self):
        sys.stdout = EmittingStream(textWritten=self.write_log)
        sys.stderr = EmittingStream(textWritten=self.write_log)

    def write_log(self, text):
        self.textEdit_log.append(text)

    def initUI(self):
        self.PushButton_13_ERA5_apikey.clicked.connect(self.save_api_key)
        self.pushButton_12_ERA5_Descargar.clicked.connect(self.download_data)
        self.pushButton_11_ERA5_rutafiles.clicked.connect(self.select_folder)
        # Línea removida: self.pushButton_Giovanni_Token.clicked.connect(self.obtain_token)

    def save_api_key(self):
        api_key_content = self.textEdit_ERA5_apikey.toPlainText()
        user_home = os.path.expanduser("~")
        ruta = os.path.join(user_home, ".cdsapirc")
        try:
            with open(ruta, 'w') as file:
                file.write(api_key_content)
            self.label_24_ERA5_result_total.setText("API Key guardada correctamente.")
        except Exception as e:
            self.label_24_ERA5_result_total.setText(f"Error: {e}")

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta")
        if folder:
            self.lineEdit_2_ERA5_rutafiles.setText(folder)

    def download_data(self):
        user_home = os.path.expanduser("~")
        ruta = os.path.join(user_home, ".cdsapirc")

        if not os.path.exists(ruta):
            self.label_24_ERA5_result_total.setText("Error: El archivo .cdsapirc no existe. Por favor, ingrese su API key.")
            return

        start_date = self.dateEdit_3_ERA5_star.date().toString("yyyy-MM-dd")
        end_date = self.dateEdit_4_ERA5_end.date().toString("yyyy-MM-dd")
        area = [
            float(self.lineEdit_3_ERA5_ESI.text()), float(self.lineEdit_4_ERA5_ESD.text()),
            float(self.lineEdit_5_ERA5_ESI.text()), float(self.lineEdit_6_ERA5_ESD.text())
        ]

        if not (area[0] > area[2] and area[1] < area[3]):
            self.label_21_ERA5_result_area.setText("Error: Coordenadas del área no válidas.")
            return
        else:
            self.label_21_ERA5_result_area.setText("Área de descarga validada correctamente.")

        variables = []
        if self.CheckBox_15_ERA5_tmpMax.isChecked():
            variables.append("maximum_2m_temperature_since_previous_post_processing")
        if self.CheckBox_16_ERA5_tmpMin.isChecked():
            variables.append("minimum_2m_temperature_since_previous_post_processing")
        if self.CheckBox_17_ERA5_pcp.isChecked():
            variables.append("total_precipitation")

        self.progressBar_2_ERA5_barra.setValue(0)

        ruta_salida = os.path.join(self.lineEdit_2_ERA5_rutafiles.text(), "ruta_salida.nc")
        self.thread = DownloadThread(ruta_salida, start_date, end_date, area, variables)
        self.thread.progress.connect(self.update_progress)
        self.thread.result.connect(self.download_finished)
        self.thread.start()

    def update_progress(self, progress):
        self.progressBar_2_ERA5_barra.setValue(progress)

    def download_finished(self, result):
        self.progressBar_2_ERA5_barra.setValue(100)
        self.label_24_ERA5_result_total.setText(result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = SWATApp()
    ventana.show()
    sys.exit(app.exec_())
