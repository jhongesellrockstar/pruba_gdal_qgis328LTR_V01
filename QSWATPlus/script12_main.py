from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox, QMainWindow, QInputDialog
from PyQt5.QtCore import Qt
from interfaz_ui_01 import Ui_MainWindow
from script12_thread_procesador import ProcesadorThread
import sys


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Inicialización
        self.carpeta_entrada = ""
        self.carpeta_salida = ""
        self.hilo = None
        self.ruta_log_txt = "log.txt"
        self.ui.progressBar.setValue(0)

        # Conectar botones
        self.ui.btn_cargar_entrada.clicked.connect(self.seleccionar_carpeta_entrada)
        self.ui.btn_cargar_salida.clicked.connect(self.seleccionar_carpeta_salida)
        self.ui.btn_ejecutar.clicked.connect(self.ejecutar_procesamiento)
        self.ui.btn_cancelar.clicked.connect(self.cancelar_procesamiento)
        self.ui.ERA5_procesamiento_exportar.clicked.connect(self.exportar_formato_swat)

    def exportar_formato_swat(self):
        nombre_proyecto, ok = QInputDialog.getText(self, "Nombre del proyecto", "Ingrese el nombre del proyecto:")
        if not ok or not nombre_proyecto:
            return

        from script12_exportar_swat import exportar_archivos_swat
        try:
            exportar_archivos_swat(nombre_proyecto, self.carpeta_salida, self.carpeta_salida)
            self.log(f"✅ Archivos SWAT generados para {nombre_proyecto}")
        except Exception as e:
            self.log(f"❌ Error: {str(e)}")

    def log(self, mensaje):
        self.ui.txt_log.append(mensaje)
        with open(self.ruta_log_txt, "a", encoding="utf-8") as f:
            f.write(mensaje + "\n")

    def seleccionar_carpeta_entrada(self):
        carpeta = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta de entrada")
        if carpeta:
            self.carpeta_entrada = carpeta
            self.ui.lbl_entrada.setText(carpeta)

    def seleccionar_carpeta_salida(self):
        carpeta = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta de salida")
        if carpeta:
            self.carpeta_salida = carpeta
            self.ui.lbl_salida.setText(carpeta)

    def ejecutar_procesamiento(self):
        if not self.carpeta_entrada or not self.carpeta_salida:
            QMessageBox.warning(self, "Advertencia", "Debes seleccionar ambas carpetas.")
            return

        self.ui.txt_log.clear()
        self.ui.progressBar.setValue(0)
        self.log("🔄 Iniciando procesamiento...")

        # Iniciar hilo
        self.hilo = ProcesadorThread(self.carpeta_entrada, self.carpeta_salida)
        self.hilo.progreso.connect(self.log)
        self.hilo.progreso_barra.connect(self.ui.progressBar.setValue)
        self.hilo.finalizado.connect(self.finalizado)
        self.hilo.start()

    def cancelar_procesamiento(self):
        if self.hilo:
            self.log("⛔ Cancelando procesamiento...")
            self.hilo.terminar()
            self.hilo = None

    def finalizado(self):
        self.log("✅ Procesamiento finalizado.")
        QMessageBox.information(self, "Completado", "Todos los archivos han sido procesados.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())
