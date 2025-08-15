from .color_relief_plugin import ColorReliefPlugin


def classFactory(iface):
    """QGIS calls this function to instantiate the plugin."""
    return ColorReliefPlugin(iface)
