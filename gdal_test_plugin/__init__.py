from .gdal_test_plugin import GdalTestPlugin


def classFactory(iface):
    """QGIS calls this function to instantiate the plugin."""
    return GdalTestPlugin(iface)
