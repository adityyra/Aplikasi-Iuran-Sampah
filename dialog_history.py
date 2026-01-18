from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
    QTableWidgetItem, QLineEdit, QHeaderView, QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor
from database import get_all_data
from delegates import StatusDelegate

class HistoryWidget(QWidget):
    back_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        # Hapus setting buat window karena sekarang sudah jadi widget

        layout = QVBoxLayout()

        # Kolom Pencarian
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Cari Nama ...")
        self.search_bar.textChanged.connect(self.filter_data)
        
        # Tabel
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setItemDelegateForColumn(5, StatusDelegate(self.table))
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False) # Hilangkan penomoran baris default
        
        # Atur posisi tombol kembali
        btn_layout = QHBoxLayout()
        btn_back = QPushButton("Kembali")
        btn_back.setStyleSheet("background-color: #2A9D8F; color: white; font-weight: bold; border-radius: 5px; padding: 10px;")
        btn_back.setFixedSize(100, 40)
        btn_back.clicked.connect(self.back_clicked.emit)
        
        btn_layout.addWidget(btn_back)
        btn_layout.addStretch() # Geser tombol ke kiri

        layout.addWidget(self.search_bar)
        layout.addWidget(self.table)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        
        # Muat data awal
        self.full_data = [] # Simpan data lengkap buat dicari/filter
        self.load_data()

    def load_data(self):
        self.table.setRowCount(0)
        self.full_data = get_all_data()
        self.populate_table(self.full_data)



    def populate_table(self, data_list):
        self.table.setRowCount(0)
        for data in data_list:
            row = self.table.rowCount()
            self.table.insertRow(row)

            values = [
                data["id"], data["nama"], data["alamat"],
                data["bulan"], data["nominal"], data["status"],
                data.get("status_langganan", "Aktif")
            ]

            for col, val in enumerate(values):
                item = QTableWidgetItem(str(val))
                item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable) # Make Read-Only
                
                if col == 5: # Kolom status
                    # Pakai logika ikon yang sama kayak di ui_main.py
                    if val == "Belum Lunas":
                        item.setText("✘")
                        item.setForeground(QColor("red"))
                    else:
                        item.setText("✔")
                        item.setForeground(QColor("green"))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    
                self.table.setItem(row, col, item)

    def filter_data(self, text):
        search_text = text.lower()
        if not search_text:
            self.populate_table(self.full_data)
            return

        filtered_data = [
            row for row in self.full_data 
            if search_text in row["nama"].lower()
        ]
        self.populate_table(filtered_data)