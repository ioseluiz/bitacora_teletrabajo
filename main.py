import sys
import os
try:
    import winreg
except ImportError:
    winreg = None

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from src.views.main_window import MainWindow
from src.views.styles import LIGHT_STYLE
from src.controllers.main_controller import MainController

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def is_dark_mode():
    """Detects if Windows is in Dark Mode."""
    if not winreg:
        return False
    try:
        registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        key = winreg.OpenKey(registry, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
        value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        return value == 0
    except Exception:
        return False

def main():
    app = QApplication(sys.argv)
    
    # Choose icon based on system theme
    dark = is_dark_mode()
    icon_name = "icono_blanco.ico" if dark else "icono_negro.ico"
    
    icon_path = resource_path(os.path.join("assets", icon_name))
    
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    else:
        # Fallback to general app_icon if specific ones don't exist
        fallback_path = resource_path(os.path.join("assets", "app_icon.ico"))
        if os.path.exists(fallback_path):
            app.setWindowIcon(QIcon(fallback_path))
        
    app.setStyleSheet(LIGHT_STYLE)
    
    view = MainWindow()
    controller = MainController(view)
    
    view.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
