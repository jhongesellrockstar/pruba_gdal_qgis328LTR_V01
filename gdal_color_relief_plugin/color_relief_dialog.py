import os
import tempfile

from qgis.PyQt.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QMessageBox,
)

try:
    from osgeo import gdal
except Exception:  # pragma: no cover - handled at runtime
    gdal = None


class ColorReliefDialog(QDialog):
    """Apply a simple color relief to a DEM using GDAL."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("DEM Color Relief")
        layout = QVBoxLayout()
        self.button = QPushButton("Colorize DEM")
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.button.clicked.connect(self.run_color_relief)

    def run_color_relief(self):
        if gdal is None:
            QMessageBox.critical(self, "GDAL", "GDAL library is not available")
            return

        input_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select DEM",
            "",
            "Raster files (*.tif *.img *.hdr *.asc *.*)",
        )
        if not input_path:
            return

        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save color relief",
            os.path.join(os.path.dirname(input_path), "color_relief.tif"),
            "GeoTIFF (*.tif)",
        )
        if not output_path:
            return

        try:
            with tempfile.NamedTemporaryFile("w", delete=False) as tmp:
                tmp.write(
                    "0 0 0 255\n"
                    "500 0 255 0\n"
                    "1000 255 255 0\n"
                    "2000 255 0 0\n"
                )
                color_file = tmp.name

            gdal.DEMProcessing(
                output_path,
                input_path,
                "color-relief",
                colorFilename=color_file,
            )

            QMessageBox.information(
                self,
                "GDAL",
                f"Color relief saved to:\n{output_path}",
                QMessageBox.Ok,
                QMessageBox.Ok,
            )
        except Exception as exc:
            QMessageBox.critical(self, "GDAL error", str(exc))
        finally:
            try:
                os.remove(color_file)
            except Exception:
                pass

