from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
    QTableWidgetItem, QHeaderView, QTabWidget, QPushButton, QMessageBox, QAbstractItemView
)
from PyQt6.QtCore import Qt, pyqtSignal
from database import get_all_data, delete_data, update_data
from dialog_tambah import DialogTambah

class CustomerWidget(QWidget):
    back_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setObjectName("CustomerPage")
        layout = QVBoxLayout()


        self.tabs = QTabWidget()
        self.tab_aktif = QWidget()
        self.tab_tidak_aktif = QWidget()

        self.tabs.addTab(self.tab_aktif, "Pelanggan Aktif")
        self.tabs.addTab(self.tab_tidak_aktif, "Tidak Aktif")

        self.setup_tab(self.tab_aktif, "Aktif")
        self.setup_tab(self.tab_tidak_aktif, "Tidak Aktif")

        layout.addWidget(self.tabs)

        # Atur posisi tombol
        btn_layout = QHBoxLayout()
        
        btn_add = QPushButton("Tambah Pelanggan")
        btn_add.clicked.connect(self.show_add_dialog)

        btn_edit = QPushButton("Edit Pelanggan")
        btn_edit.clicked.connect(self.show_edit_dialog)

        btn_hapus = QPushButton("Hapus Pelanggan")
        btn_hapus.clicked.connect(self.hapus_pelanggan)
        
        btn_back = QPushButton("Kembali")
        btn_back.clicked.connect(self.back_clicked.emit)
        
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_edit)
        btn_layout.addWidget(btn_hapus)
        btn_layout.addWidget(btn_back)
        
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        
    def show_add_dialog(self):
        dlg = DialogTambah()
        if dlg.exec():
            self.load_data()

    def show_edit_dialog(self):
        # Ambil tabel dari tab yang aktif
        table = self.table_aktif if self.tabs.currentIndex() == 0 else self.table_tidak_aktif
        row = table.currentRow()
        
        if row < 0:
            QMessageBox.warning(self, "Peringatan", "Pilih pelanggan yang ingin diedit!")
            return
            
        id_data = str(table.item(row, 0).data(Qt.ItemDataRole.UserRole))
        current_data = next((d for d in self.all_data_cache if str(d["id"]) == id_data), None)
        
        if current_data:
            dlg = DialogTambah(data=current_data)
            if dlg.exec():
                self.load_data()
        else:
            QMessageBox.warning(self, "Error", "Data tidak ditemukan!")

    def hapus_pelanggan(self):
        table = self.table_aktif if self.tabs.currentIndex() == 0 else self.table_tidak_aktif
        row = table.currentRow()
        
        if row < 0:
            QMessageBox.warning(self, "Peringatan", "Pilih pelanggan yang ingin dihapus!")
            return
            
        reply = QMessageBox.question(
            self, "Konfirmasi", "Apakah Anda yakin ingin menghapus pelanggan ini?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            id_data = str(table.item(row, 0).data(Qt.ItemDataRole.UserRole))
            current_data = next((d for d in self.all_data_cache if str(d["id"]) == id_data), None)
            
            if current_data:
                name = str(current_data.get("nama_warga", "")).lower().strip()
                address = str(current_data.get("alamat", "")).lower().strip()
                
                # Cari semua data buat warga ini
                to_delete = [
                    d for d in self.all_data_cache 
                    if str(d["nama_warga"]).lower().strip() == name and 
                       str(d["alamat"]).lower().strip() == address
                ]
                
                for d in to_delete:
                    delete_data(d["id"])
                    
            self.load_data()


    def setup_tab(self, tab, filter_status):
        layout = QVBoxLayout()
        table = QTableWidget()
        table.setColumnCount(3) # Kolom ID, Nama, dan Alamat
        table.setHorizontalHeaderLabels(
            ["ID", "Nama", "Alamat"]
        )
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setVisible(False)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        layout.addWidget(table)
        tab.setLayout(layout)
        
        # Simpan referensi tabel
        if filter_status == "Aktif":
            self.table_aktif = table
        else:
            self.table_tidak_aktif = table

    def load_data(self):
        all_data = get_all_data()
        self.all_data_cache = all_data
        
        # Hapus duplikasi berdasarkan Nama dan Alamat
        seen_customers = set()
        unique_customers = []
        
        # Urutkan berdasarkan bulan? Atau ambil saja data pertama yang ketemu
        for data in all_data:
            customer_key = (
                str(data.get("nama_warga", "")).lower().strip(),
                str(data.get("alamat", "")).lower().strip()
            )
            if customer_key not in seen_customers:
                seen_customers.add(customer_key)
                unique_customers.append(data)

        aktif_data = [d for d in unique_customers if d.get("status_langganan", "Aktif") == "Aktif"]
        tidak_aktif_data = [d for d in unique_customers if d.get("status_langganan") == "Tidak Aktif"]

        self.populate_table(self.table_aktif, aktif_data)
        self.populate_table(self.table_tidak_aktif, tidak_aktif_data)

    def populate_table(self, table, data_list):
        table.setRowCount(0)
        # Urutkan berdasarkan nama biar rapi
        data_list.sort(key=lambda x: str(x.get("nama_warga", "")))
        
        for i, data in enumerate(data_list):
            row = table.rowCount()
            table.insertRow(row)

            # Tampilkan ID sebagai nomor urut (1, 2, 3...)
            display_id = i + 1
            values = [
                display_id, data["nama_warga"], data["alamat"]
            ]

            for col, val in enumerate(values):
                item = QTableWidgetItem(str(val))
                if col == 0:
                    # Simpan ID database ASLI di UserRole buat hapus/edit
                    item.setData(Qt.ItemDataRole.UserRole, data["id"])
                table.setItem(row, col, item)