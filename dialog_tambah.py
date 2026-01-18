from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit,
    QPushButton, QComboBox, QMessageBox
)
from PyQt6.QtCore import Qt
from database import insert_data, update_data, MockResponse

class DialogTambah(QDialog):
    def __init__(self, data=None):
        super().__init__()
        self.data = data
        title = "Edit Pembayaran" if self.data else "Tambah Pembayaran"
        self.setWindowTitle(title)
        self.setFixedSize(300, 300)

        layout = QVBoxLayout()

        self.nama = QLineEdit()
        self.nama.setPlaceholderText("Nama ")

        self.alamat = QLineEdit()
        self.alamat.setPlaceholderText("Alamat / No.Rumah")

        self.bulan = QComboBox()
        self.bulan.addItems([
            "Januari", "Februari", "Maret", "April", "Mei", "Juni",
            "Juli", "Agustus", "September", "Oktober", "November", "Desember"
        ])
        self.bulan.setPlaceholderText("Bulan")
        self.bulan.setCurrentIndex(-1)

        self.nominal = QLineEdit()
        self.nominal.setPlaceholderText("Nominal")

        self.status = QComboBox()
        self.status.addItems(["Belum Lunas", "Lunas"])

        self.status_langganan = QComboBox()
        self.status_langganan.addItems(["Aktif", "Tidak Aktif"])

        # Isi otomatis kalau lagi edit data
        if self.data:
            self.nama.setText(str(self.data.get("nama_warga", "")))
            self.alamat.setText(str(self.data.get("alamat", "")))
            self.nominal.setText(str(self.data.get("nominal", "")))
            self.status.setCurrentText(str(self.data.get("status", "Belum Lunas")))
            self.status_langganan.setCurrentText(str(self.data.get("status_langganan", "Aktif")))

        # Hilangkan pilihan bulan karena prosesnya sekarang otomatis buat setahun
        self.bulan.setVisible(False)

        btn = QPushButton("Simpan")
        btn.clicked.connect(self.simpan)

        layout.addWidget(self.nama)
        layout.addWidget(self.alamat)
        layout.addWidget(self.bulan) # Tetap ada di layout tapi disembunyikan
        layout.addWidget(self.nominal)
        layout.addWidget(self.status)
        layout.addWidget(self.status_langganan)
        layout.addWidget(btn)

        self.setLayout(layout)

    def simpan(self):
        try:
            nominal_val = int(self.nominal.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "Nominal harus berupa angka!")
            return

        months = [
            "Januari", "Februari", "Maret", "April", "Mei", "Juni",
            "Juli", "Agustus", "September", "Oktober", "November", "Desember"
        ]

        payload = {
            "nama_warga": self.nama.text(),
            "alamat": self.alamat.text(),
            "bulan": self.bulan.currentText(),
            "nominal": nominal_val,

            "status": self.status.currentText(),
            "status_langganan": self.status_langganan.currentText()
        }
        
        try:
            if self.data: # Update/Ubah
                # Logika sinkronisasi: Update SEMUA data buat warga ini
                orig_name = str(self.data.get("nama_warga", "")).lower().strip()
                orig_address = str(self.data.get("alamat", "")).lower().strip()
                
                from database import get_all_data
                all_recs = get_all_data()
                
                # Cari semua data buat warga yang sama
                customer_recs = [
                    rec for rec in all_recs 
                    if str(rec["nama_warga"]).lower().strip() == orig_name and 
                       str(rec["alamat"]).lower().strip() == orig_address
                ]
                
                # Kalau data nggak ketemu (jarang terjadi), update yang sekarang aja
                if not customer_recs:
                    resp = update_data(self.data["id"], payload)
                else:
                    for rec in customer_recs:
                        update_payload = payload.copy()
                        update_payload["bulan"] = rec["bulan"] # Tetap pakai bulan yang sama
                        # Tetap pakai status lunas/belum. Biasanya status lunas per bulan,
                        # tapi nama/alamat/status langganan itu global.
                        update_payload["status"] = rec["status"] 
                        
                        update_data(rec["id"], update_payload)
                    resp = MockResponse(200) # Penanda berhasil

                success_code = 200
            else: # Tambah buat banyak bulan sekaligus

                for month in months:
                    p = payload.copy()
                    p["bulan"] = month
                    resp = insert_data(p)
                success_code = 201

            if resp.status_code in [200, 201, 204]:
                self.accept()
            else:
                QMessageBox.warning(self, "Gagal", f"Gagal menyimpan data: {resp.status_code}\n{resp.text}")
        except Exception as e:
             QMessageBox.critical(self, "Error", f"Terjadi kesalahan koneksi:\n{str(e)}")

