import os
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon
from .gdal_test_dialog import GdalTestDialog


class GdalTestPlugin:
    """Simple plugin demonstrating GDAL usage from QGIS."""

    def __init__(self, iface):
        self.iface = iface
        self.action = None
        self.dialog = None

    def initGui(self):
        icon_path = os.path.join(os.path.dirname(__file__), "icon.svg")
        self.action = QAction(QIcon(icon_path), "GDAL Test", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        if self.action:
            self.iface.removeToolBarIcon(self.action)
            self.action.deleteLater()

    def run(self):
        if not self.dialog:
            self.dialog = GdalTestDialog(self.iface.mainWindow())
        self.dialog.show()
        self.dialog.raise_()
        self.dialog.activateWindow()
