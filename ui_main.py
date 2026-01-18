from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QMessageBox, QStackedWidget, QHeaderView, QLabel,
    QAbstractItemView, QComboBox, QStyledItemDelegate, QStyle, QScrollArea, QButtonGroup
)
from PyQt6.QtGui import QColor, QAction
from PyQt6.QtCore import Qt, pyqtSignal
from database import get_all_data, delete_data, update_data
from dialog_tambah import DialogTambah
from customer_widget import CustomerWidget


from delegates import StatusDelegate
from income_widget import IncomeWidget

class LandingWidget(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.setObjectName("LandingWidget")
        self.parent_window = parent_window
        
        layout = QVBoxLayout()
        
        layout.addStretch()
        layout.addSpacing(50) # Turunkan sedikit
        
        title = QLabel("APLIKASI MANAJEMEN\nPEMBAYARAN IURAN SAMPAH")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)


        
        # Layout horizontal buat tombol-tombol
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20) # Jarak antar tombol
        
        btn_manage = QPushButton("📝\nKelola Data")
        btn_manage.setMinimumHeight(120)
        btn_manage.setMinimumWidth(200)
        btn_manage.clicked.connect(self.parent_window.go_manage)
        
        btn_status = QPushButton("👥\nPelanggan")
        btn_status.setMinimumHeight(120)
        btn_status.setMinimumWidth(200)
        btn_status.clicked.connect(self.parent_window.go_customer)
        
        btn_income = QPushButton("💰\nPenghasilan")
        btn_income.setMinimumHeight(120)
        btn_income.setMinimumWidth(200)
        btn_income.clicked.connect(self.parent_window.go_income)
        
        button_layout.addWidget(btn_manage)
        button_layout.addWidget(btn_status)
        button_layout.addWidget(btn_income)

        
        layout.addLayout(button_layout)
        layout.addStretch()

        # Tombol Keluar (Pojok Kiri Bawah)
        bottom_layout = QHBoxLayout()
        btn_logout = QPushButton("Kembali ke Login")
        btn_logout.setFixedSize(150, 40) # Lebih kecil dari tombol utama
        btn_logout.clicked.connect(self.parent_window.handle_logout)
        
        bottom_layout.addWidget(btn_logout)
        bottom_layout.addStretch() # Geser ke kiri
        
        layout.addLayout(bottom_layout)
        
        self.setLayout(layout)

class MainWindow(QMainWindow):
    logout_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("APLIKASI MANAJEMEN PEMBAYARAN IURAN SAMPAH")

        self.resize(800, 500)

        # Atur Stacked Widget buat ganti-ganti halaman
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # === Halaman 0: Halaman Depan ===
        self.page_landing = LandingWidget(self)
        self.stacked_widget.addWidget(self.page_landing)
        
        # === Halaman 1: Kelola Data ===
        self.page_main = QWidget()
        self.page_main.setObjectName("ManagePage")
        self.init_manage_ui()
        self.stacked_widget.addWidget(self.page_main)
        
        # === Halaman 2: Pelanggan ===
        self.page_customer = CustomerWidget()
        self.page_customer.back_clicked.connect(self.go_landing)
        self.stacked_widget.addWidget(self.page_customer)
        
        # === Halaman 3: Penghasilan ===
        self.page_income = IncomeWidget()
        self.page_income.back_clicked.connect(self.go_landing)
        self.stacked_widget.addWidget(self.page_income)

        

        

        self.load_data()

    def init_manage_ui(self):
        layout = QVBoxLayout(self.page_main)

        # Filter Bulan (Tombol Horizontal)
        # Wadah buat ScrollArea
        filter_container = QWidget()
        filter_layout = QHBoxLayout(filter_container)
        filter_layout.setContentsMargins(0, 0, 0, 0)
        filter_layout.setSpacing(10)
        
        self.btn_group_bulan = QButtonGroup(self)
        self.btn_group_bulan.setExclusive(True)
        self.btn_group_bulan.buttonClicked.connect(self.on_month_btn_clicked)
        
        months = [
            "Januari", "Februari", "Maret", "April", "Mei", "Juni",
            "Juli", "Agustus", "September", "Oktober", "November", "Desember"
        ]
        
        self.selected_month = "Januari" # Bulan default

        for i, month in enumerate(months):
            btn = QPushButton(month)
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            # Opsional: Gaya buat tombol yang dipilih
            btn.setStyleSheet("""
                QPushButton {
                    padding: 5px 10px;
                    border: 1px solid #ccc;
                    border-radius: 15px;
                    background-color: #f0f0f0;
                }
                QPushButton:checked {
                    background-color: #2A9D8F;
                    color: white;
                    border: 1px solid #2A9D8F;
                }
            """)
            
            if month == self.selected_month:
                btn.setChecked(True)
                
            self.btn_group_bulan.addButton(btn, i)
            filter_layout.addWidget(btn)
            
        filter_layout.addStretch()

        scroll_area = QScrollArea()
        scroll_area.setWidget(filter_container)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedHeight(60) # Sesuaikan tinggi kalau perlu
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        

        layout.addWidget(scroll_area)

        # Ringkasan Pembayaran
        self.summary_widget = QWidget()
        summary_layout = QHBoxLayout(self.summary_widget)
        summary_layout.setContentsMargins(0, 10, 0, 10)
        
        self.label_summary = QLabel("Lunas: 0 | Belum Lunas: 0")
        self.label_summary.setStyleSheet("""
            font-weight: bold; 
            font-size: 14px; 
            color: #333;
            background-color: #f8f9fa;
            padding: 5px 15px;
            border-radius: 10px;
            border: 1px solid #dee2e6;
        """)
        summary_layout.addWidget(self.label_summary)
        summary_layout.addStretch()
        
        layout.addWidget(self.summary_widget)


        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["Nama", "Alamat", "Nominal", "Status", "Berlangganan", ""]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents) # Kolom ikon dibuat pas ukurannya
        self.table.setItemDelegateForColumn(5, StatusDelegate(self.table))

        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.cellClicked.connect(self.on_cell_clicked)
        # self.table.cellDoubleClicked.connect(self.show_dialog_edit) # Disabled per user request

        btn_back = QPushButton("Kembali")
        btn_back.setFixedSize(100, 40) # Smaller fixed size
        btn_back.clicked.connect(self.go_landing)

        layout.addWidget(self.table)

        
        # Back Button Layout (Bottom Left)
        back_layout = QHBoxLayout()
        back_layout.addWidget(btn_back)
        back_layout.addStretch() # Push to left
        
        layout.addLayout(back_layout)

    def on_month_btn_clicked(self, btn):
        self.selected_month = btn.text()
        self.filter_by_month()

    def filter_by_month(self):
        # selected_month = self.combo_bulan.currentText() # Logika lama
        selected_month = self.selected_month
        rows = self.table.rowCount()
        
        # Filter ketat (nggak ada "Semua Bulan")
        count_lunas = 0
        count_belum_lunas = 0
        
        for row in range(rows):
            # Metadata disimpan di UserRole item "Nama" (kolom 0)
            item = self.table.item(row, 0)
            status_item = self.table.item(row, 3) # Kolom Status
            langganan_item = self.table.item(row, 4) # Kolom Berlangganan
            
            if not item:
                continue
                
            month_text = item.data(Qt.ItemDataRole.UserRole + 1)
            if not month_text:
                month_text = ""
            
            if str(month_text).lower() == selected_month.lower():
                 self.table.setRowHidden(row, False)
                 
                 # Cuma hitung warga Aktif di ringkasan pembayaran
                 if langganan_item and langganan_item.text() == "Aktif":
                     if status_item and status_item.text() == "Lunas":
                         count_lunas += 1
                     else:
                         count_belum_lunas += 1
            else:
                 self.table.setRowHidden(row, True)


        
        # Update label ringkasan
        self.label_summary.setText(f"Lunas: {count_lunas} | Belum Lunas: {count_belum_lunas}")


    def load_data(self):
        self.table.setRowCount(0)
        data_list = get_all_data()
        self.all_data_cache = data_list # Simpan data buat referensi edit
        
        for data in data_list:
            row = self.table.rowCount()
            self.table.insertRow(row)

            # Kolom digeser (ID dihapus)
            values = [
                data["nama_warga"], data["alamat"],
                data["nominal"], data["status"],
                data.get("status_langganan", "Aktif"),
                "" # Tempat buat ikon
            ]

            for col, val in enumerate(values):
                item = QTableWidgetItem(str(val))
                
                # Kolom 0 (Nama): Simpan ID dan bulan
                if col == 0:
                    item.setData(Qt.ItemDataRole.UserRole, data["id"]) # ID Database
                    item.setData(Qt.ItemDataRole.UserRole + 1, data["bulan"]) # Bulan
                
                # Kolom Ikon (Indeks 5)
                if col == 5:
                    if data["status"] == "Belum Lunas":
                        item.setText("✘")
                        item.setForeground(QColor("red"))
                    else:
                        item.setText("✔")
                        item.setForeground(QColor("green"))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    item.setFont(self.font())

                # Background merah buat warga tidak aktif
                if data.get("status_langganan") == "Tidak Aktif":
                    item.setBackground(QColor("#E74C3C")) # Merah halus
                    if col != 5: # Jangan timpa warna ikon
                        item.setForeground(QColor("white"))

                self.table.setItem(row, col, item)


        
        # Pakai lagi filternya setelah data dimuat
        self.filter_by_month()

    def show_dialog_add(self):
        dlg = DialogTambah() # Nggak ada data = Mode Tambah
        if dlg.exec():
            self.load_data()

    def show_dialog_edit(self, row=None, col=None):
        if row is None:
            row = self.table.currentRow()
            
        if row < 0:
            QMessageBox.warning(self, "Peringatan", "Pilih data yang ingin diedit!")
            return
        
        # Ambil ID database asli dari data tersembunyi
        id_item = self.table.item(row, 0)
        id_data = str(id_item.data(Qt.ItemDataRole.UserRole))
        
        # Cari objek data aslinya
        current_data = next((d for d in self.all_data_cache if str(d["id"]) == id_data), None)
        
        if current_data:
            dlg = DialogTambah(data=current_data) # Kirim data = Mode Edit
            if dlg.exec():
                self.load_data()
        else:
             QMessageBox.warning(self, "Error", "Data tidak ditemukan!")

    def hapus_data(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Peringatan", "Pilih data!")
            return
        # Dialog konfirmasi
        reply = QMessageBox.question(
            self,
            "Konfirmasi",
            "Apakah Anda yakin ingin menghapus data ini?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return
        id_data = str(self.table.item(row, 0).data(Qt.ItemDataRole.UserRole))
        delete_data(id_data)
        self.load_data()

    def on_cell_clicked(self, row, col):
        # Kolom 5 itu kolom ikon status
        if col == 5:

            item = self.table.item(row, 0)
            id_data = item.data(Qt.ItemDataRole.UserRole)
            
            # Cari objek data lengkapnya
            current_data = next((d for d in self.all_data_cache if d["id"] == id_data), None)
            
            if current_data:
                new_status = "Lunas" if current_data["status"] == "Belum Lunas" else "Belum Lunas"
                
                # Dialog konfirmasi
                msg = f"Ubah status pembayaran menjadi '{new_status}'?"
                reply = QMessageBox.question(
                    self, "Konfirmasi", msg,
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )
                
                if reply != QMessageBox.StandardButton.Yes:
                    return

                # Buat data minimal buat update

                # Update_data butuh data lengkap, jadi kita salin datanya terus ganti statusnya.
                payload = current_data.copy()
                payload["status"] = new_status
                # Hapus ID dari data kalau ada karena dikirim terpisah
                payload.pop("id", None) 
                
                update_data(id_data, payload)
                self.load_data() # Refresh tampilan

    # --- Navigasi ---
    def go_landing(self):
        self.load_data() # Refresh data utama pelan-pelan
        self.stacked_widget.setCurrentIndex(0)

    def go_manage(self):
        self.load_data()
        self.stacked_widget.setCurrentIndex(1)



        
    def go_customer(self):
        self.page_customer.load_data()
        self.stacked_widget.setCurrentIndex(2)
        
    def go_income(self):
        self.page_income.refresh_data()
        self.stacked_widget.setCurrentIndex(3)


    def handle_logout(self):
        self.logout_signal.emit()