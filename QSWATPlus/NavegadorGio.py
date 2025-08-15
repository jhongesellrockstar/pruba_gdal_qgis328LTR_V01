from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

# URL predeterminada para el visor de Giovanni
DEFAULT_URL = "https://giovanni.gsfc.nasa.gov/giovanni/#service=ArAvTs&starttime=2023-01-01T00:00:00Z&endtime=2023-01-01T00:59:59Z"

class NavegadorGio:
    def __init__(self, web_view, refresh_button):
        """
        Inicializa el navegador para visualizar Giovanni.

        :param web_view: El widget promovido a QWebEngineView.
        :param refresh_button: Botón para refrescar la página.
        """
        self.web_view = web_view
        self.refresh_button = refresh_button

        # Configurar botón para actualizar el sitio web
        self.refresh_button.clicked.connect(self.reload_page)

        # Cargar la URL por defecto al inicio
        self.web_view.load(QUrl(DEFAULT_URL))

    def reload_page(self):
        """Recarga la página con la URL actual o restablece la predeterminada."""
        current_url = self.web_view.url().toString().strip()

        if not current_url or current_url == "about:blank":
            current_url = DEFAULT_URL
        
        self.web_view.load(QUrl(current_url))
