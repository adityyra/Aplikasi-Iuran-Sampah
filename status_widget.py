from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, 
    QTableWidgetItem, QHeaderView, QTabWidget, QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor
from database import get_all_data
from dialog_tambah import DialogTambah

class StatusWidget(QWidget):
    back_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.tabs = QTabWidget()
        self.tab_lunas = QWidget()
        self.tab_belum = QWidget()

        self.tabs.addTab(self.tab_lunas, "Lunas")
        self.tabs.addTab(self.tab_belum, "Belum Lunas")

        self.setup_tab(self.tab_lunas, "Lunas")
        self.setup_tab(self.tab_belum, "Belum Lunas")

        layout.addWidget(self.tabs)

        # Tombol Kembali
        btn_back = QPushButton("Kembali")
        btn_back.clicked.connect(self.back_clicked.emit)
        layout.addWidget(btn_back)

        self.setLayout(layout)
        

    def setup_tab(self, tab, filter_status):
        layout = QVBoxLayout()
        table = QTableWidget()
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels(
            ["ID", "Nama", "Alamat", "Bulan", "Nominal", "Status", "Berlangganan"]
        )
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # Klik dua kali buat edit
        table.cellDoubleClicked.connect(self.edit_item)
        
        layout.addWidget(table)
        tab.setLayout(layout)
        
        # Simpan referensi tabel
        if filter_status == "Lunas":
            self.table_lunas = table
        else:
            self.table_belum = table

    def edit_item(self, row, column):
        table = self.sender()
        if not table:
            return
            
        id_item = table.item(row, 0)
        if not id_item:
            return
            
        # Susun ulang data dari baris tabel
        data = {
            "id": table.item(row, 0).text(),
            "nama_warga": table.item(row, 1).text(),
            "alamat": table.item(row, 2).text(),
            "bulan": table.item(row, 3).text(),
            "nominal": int(table.item(row, 4).text()),
            "status": table.item(row, 5).text(),
            "status_langganan": table.item(row, 6).text()
        }
        
        dlg = DialogTambah(data=data)
        if dlg.exec():
            self.load_data()

    def load_data(self):
        all_data = get_all_data()
        
        lunas_data = [d for d in all_data if d["status"] == "Lunas"]
        belum_data = [d for d in all_data if d["status"] == "Belum Lunas"]

        self.populate_table(self.table_lunas, lunas_data)
        self.populate_table(self.table_belum, belum_data)

    def populate_table(self, table, data_list):
        table.setRowCount(0)
        for data in data_list:
            row = table.rowCount()
            table.insertRow(row)

            values = [
                data["id"], data["nama_warga"], data["alamat"],
                data["bulan"], data["nominal"], data["status"],
                data.get("status_langganan", "Aktif")
            ]

            for col, val in enumerate(values):
                item = QTableWidgetItem(str(val))
                item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable) 
                
                if col == 5:
                    item.setBackground(
                        QColor("red") if val == "Belum Lunas" 
                        else QColor("lightgreen")
                    )
                table.setItem(row, col, item)
