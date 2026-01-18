from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QScrollArea, QFrame, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from database import get_all_data

class IncomeWidget(QWidget):
    back_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setObjectName("IncomePage")
        layout = QVBoxLayout()
        
        # Bagian Atas/Header
        header_layout = QHBoxLayout()
        self.btn_back = QPushButton("Kembali")
        self.btn_back.setObjectName("KembaliBtn")
        self.btn_back.setFixedSize(100, 40)
        self.btn_back.clicked.connect(self.back_clicked.emit)
        
        title = QLabel("LAPORAN PENGHASILAN BULANAN")
        title.setObjectName("IncomeTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #F1C40F;") # Judul warna emas
        
        header_layout.addWidget(self.btn_back)
        header_layout.addStretch(1)
        header_layout.addWidget(title)
        header_layout.addStretch(1)
        # Spasi biar seimbang
        header_layout.addSpacing(100)
        
        layout.addLayout(header_layout)
        layout.addSpacing(20)

        # Area scroll buat daftar bulan
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")
        
        container = QWidget()
        self.grid = QGridLayout(container)
        self.grid.setSpacing(15)
        
        scroll.setWidget(container)
        layout.addWidget(scroll)
        
        self.setLayout(layout)
        self.refresh_data()

    def refresh_data(self):
        # Bersihkan grid
        while self.grid.count():
            child = self.grid.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        all_data = get_all_data()
        
        months = [
            "Januari", "Februari", "Maret", "April", "Mei", "Juni",
            "Juli", "Agustus", "September", "Oktober", "November", "Desember"
        ]
        
        # Totalin penghasilan
        income_map = {m: 0 for m in months}
        for d in all_data:
            if str(d.get("status", "")).lower() == "lunas":
                m = d.get("bulan", "")
                if m in income_map:
                    try:
                        income_map[m] += int(d.get("nominal", 0))
                    except:
                        pass
        
        # Buat Grid (3 kolom)
        for i, month in enumerate(months):
            row = i // 3
            col = i % 3
            
            card = QFrame()
            card.setObjectName("IncomeCard")
            card.setStyleSheet("""
                QFrame#IncomeCard {
                    background-color: #2C3E50;
                    border: 1px solid #16A085;
                    border-radius: 12px;
                    padding: 15px;
                }
            """)
            card_layout = QVBoxLayout(card)
            
            m_label = QLabel(month)
            m_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #BDC3C7;")
            m_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            amount = income_map[month]
            a_label = QLabel(f"Rp {amount:,}")
            a_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2ECC71;") # Hijau tanda sukses
            a_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            card_layout.addWidget(m_label)
            card_layout.addWidget(a_label)
            
            self.grid.addWidget(card, row, col)
