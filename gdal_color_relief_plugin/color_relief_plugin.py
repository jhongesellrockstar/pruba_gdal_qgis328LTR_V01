import os

from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon

from .color_relief_dialog import ColorReliefDialog


class ColorReliefPlugin:
    """Generate a colorized raster from a DEM using GDAL."""

    def __init__(self, iface):
        self.iface = iface
        self.action = None
        self.dialog = None

    def initGui(self):
        icon_path = os.path.join(os.path.dirname(__file__), "icon.svg")
        self.action = QAction(QIcon(icon_path), "DEM Color Relief", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        if self.action:
            self.iface.removeToolBarIcon(self.action)
            self.action.deleteLater()

    def run(self):
        if not self.dialog:
            self.dialog = ColorReliefDialog(self.iface.mainWindow())
        self.dialog.show()
        self.dialog.raise_()
        self.dialog.activateWindow()

