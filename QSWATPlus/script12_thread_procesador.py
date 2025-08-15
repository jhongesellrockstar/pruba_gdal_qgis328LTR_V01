from PyQt5.QtCore import QThread, pyqtSignal
import script12_prime  # Importa lógica principal

class ProcesadorThread(QThread):
    progreso = pyqtSignal(str)
    progreso_barra = pyqtSignal(int)
    finalizado = pyqtSignal()

    def __init__(self, carpeta_entrada, carpeta_salida):
        super().__init__()
        self.carpeta_entrada = carpeta_entrada
        self.carpeta_salida = carpeta_salida
        self._interrumpir = False

    def run(self):
        archivos = script12_prime.listar_archivos_nc(self.carpeta_entrada)
        total = len(archivos)

        def log_callback(mensaje):
            self.progreso.emit(mensaje)

        for i, archivo in enumerate(archivos):
            if self._interrumpir:
                break
            script12_prime.procesar_archivo_individual(
                archivo, self.carpeta_entrada, self.carpeta_salida, log_callback
            )
            progreso_percent = int(((i + 1) / total) * 100)
            self.progreso_barra.emit(progreso_percent)

        self.finalizado.emit()

    def terminar(self):
        self._interrumpir = True
        self.quit()
