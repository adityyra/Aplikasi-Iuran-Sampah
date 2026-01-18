import sys
from PyQt6.QtWidgets import QApplication
from ui_main import MainWindow
from login_window import LoginWindow
from database import init_db

import os

def resource_path(relative_path):
    """ Ambil path absolut ke file resource, bisa buat dev atau PyInstaller """
    try:
        # PyInstaller bikin folder temp dan simpan path-nya di _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Inisialisasi Database
init_db()

app = QApplication(sys.argv)

# Muat stylesheet supaya jalan juga pas dipaket (bundle)
style_file = resource_path("style.qss")
with open(style_file, "r") as f:
    app.setStyleSheet(f.read())


def show_main():
    global window
    window = MainWindow()
    window.logout_signal.connect(logout)
    window.show()
    login.close()

def logout():
    global window
    window.close()
    login.show()

login = LoginWindow()
login.login_success.connect(show_main)
login.show()

sys.exit(app.exec())