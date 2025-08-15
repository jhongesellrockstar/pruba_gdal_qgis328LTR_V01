from PyQt5.QtWidgets import QApplication
from qswatdialog import QSwatDialog
import sys

app = QApplication(sys.argv)
window = QSwatDialog()
window.show()
sys.exit(app.exec_())
