# AMPIS - Aplikasi Manajemen Pembayaran Iuran Sampah

Aplikasi desktop berbasis Python untuk mengelola iuran kebersihan/sampah warga secara digital, aman, dan efisien.

![Preview](BimDer.ico)

## ✨ Fitur Utama
- 🔐 **Login Keamanan**: Proteksi akses menggunakan PIN.
- 📊 **Laporan Otomatis**: Dashboard penghasilan bulanan real-time.
- 👥 **Data Pelanggan**: Kelola warga aktif dan tidak aktif dengan mudah.
- 💳 **History Pembayaran**: Lacak status Lunas/Belum Lunas per bulan.
- 🎨 **UI Modern**: Desain premium dengan tema warna *Midnight Teal*.

## 🚀 Teknologi yang Digunakan
- **Bahasa**: [Python 3](https://www.python.org/)
- **UI Framework**: [PyQt6](https://www.riverbankcomputing.com/software/pyqt/)
- **Database**: [SQLite](https://www.sqlite.org/)
- **Packaging**: [PyInstaller](https://pyinstaller.org/)

## 🛠️ Instalasi (Development)

1.  **Clone Repositori**:
    ```bash
    git clone https://github.com/username/project_akhir.git
    cd project_akhir
    ```

2.  **Install Dependensi**:
    ```bash
    pip install PyQt6
    ```

3.  **Jalankan Aplikasi**:
    ```bash
    python main.py
    ```

## 📦 Membuat Executable (.exe)
Untuk membuat file .exe mandiri, jalankan perintah berikut:
```bash
pyinstaller --noconfirm --onefile --windowed --icon "BimDer.ico" --add-data "style.qss;." main.py
```

## 📝 Lisensi
Proyek ini dibuat untuk memenuhi tugas Pratikum Pemrograman Visual.

---
**Disusun oleh:** Aditya Ramadani (3A)
**Universitas:** [Nama Universitas Anda]

