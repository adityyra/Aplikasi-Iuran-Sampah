import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal

class LoginWindow(QWidget):
    login_success = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setObjectName("LoginWindow")
        self.setWindowTitle("Login")
        self.setFixedSize(800, 500)

        main_layout = QVBoxLayout()
        
        # Bagian atas buat tombol Keluar
        top_layout = QHBoxLayout()
        self.btn_exit = QPushButton("Keluar")
        self.btn_exit.setFixedSize(100, 35)
        self.btn_exit.setObjectName("ExitBtn")
        self.btn_exit.clicked.connect(lambda: sys.exit(0))
        top_layout.addWidget(self.btn_exit)
        top_layout.addStretch(1) # Geser tombol ke kiri
        
        main_layout.addLayout(top_layout)
        main_layout.addStretch(1) # Geser konten ke tengah


        self.title_label = QLabel("APLIKASI MANAJEMEN PEMBAYARAN IURAN SAMPAH")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: white;
            letter-spacing: 1px;
        """)

        self.pin_input = QLineEdit()
        self.pin_input.setFixedWidth(300)
        self.pin_input.setFixedHeight(40) # Sedikit lebih tinggi
        self.pin_input.setPlaceholderText("Masukkan PIN")
        self.pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pin_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pin_input.returnPressed.connect(self.check_login)

        self.btn_login = QPushButton("Masuk")
        self.btn_login.setFixedWidth(300)
        self.btn_login.setFixedHeight(40) # Samakan tingginya
        self.btn_login.clicked.connect(self.check_login)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #FF5555; font-weight: bold; font-size: 14px;")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_layout.addWidget(self.title_label, 0, Qt.AlignmentFlag.AlignCenter)
        main_layout.addSpacing(30) # Jarak vertikal setelah judul
        main_layout.addWidget(self.pin_input, 0, Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.btn_login, 0, Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.error_label, 0, Qt.AlignmentFlag.AlignCenter)
        
        main_layout.addStretch(1) # Geser konten ke tengah
        
        self.pin_input.setFocus()

        self.setLayout(main_layout)


    def check_login(self):
        pin = self.pin_input.text()
        if pin == "123":
            self.login_success.emit()
            self.close()
        else:
            self.error_label.setText("PIN Salah! Coba lagi.")
            self.pin_input.clear()
