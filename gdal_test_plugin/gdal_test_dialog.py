import os
from qgis.PyQt.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QMessageBox,
)
from qgis.PyQt.QtCore import Qt
try:
    from osgeo import gdal
except Exception:  # pragma: no cover - handled at runtime
    gdal = None


class GdalTestDialog(QDialog):
    """Dialog with a single button to test GDAL."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("GDAL Test")
        layout = QVBoxLayout()
        self.button = QPushButton("Run GDAL")
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.button.clicked.connect(self.run_gdal)

    def run_gdal(self):
        if gdal is None:
            QMessageBox.critical(self, "GDAL", "GDAL library is not available")
            return

        input_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select raster",
            "",
            "Raster files (*.*)",
        )
        if not input_path:
            return
        try:
            ds = gdal.Open(input_path)
            if ds is None:
                QMessageBox.warning(self, "GDAL", "Unable to open selected file")
                return
            output_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save copy",
                os.path.join(os.path.dirname(input_path), "gdal_copy.tif"),
                "GeoTIFF (*.tif)",
            )
            if not output_path:
                return
            gdal.Translate(output_path, ds)
            QMessageBox.information(
                self,
                "GDAL",
                f"Dataset copied to:\n{output_path}",
                QMessageBox.Ok,
                QMessageBox.Ok,
            )
        except Exception as exc:
            QMessageBox.critical(self, "GDAL error", str(exc))
