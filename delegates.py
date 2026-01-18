from PyQt6.QtWidgets import QStyledItemDelegate, QStyle
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt

class StatusDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        painter.save()
        
        # Gambar background seleksi kalau barisnya dipilih
        if option.state & QStyle.StateFlag.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())

        # Tentukan warna teks
        # Utamakan warna foreground tiap item (Merah/Hijau) 
        # supaya status tetap kelihatan pas dipilih.
        color_data = index.data(Qt.ItemDataRole.ForegroundRole)
        if color_data:
             painter.setPen(QColor(color_data))
        elif option.state & QStyle.StateFlag.State_Selected:
             # Pakai warna putih kalau belum ada warna khusus
             painter.setPen(QColor("white"))
        else:
             painter.setPen(QColor("black"))
        
        # Gambar teksnya
        text = index.data(Qt.ItemDataRole.DisplayRole)
        if text:
            painter.drawText(option.rect, Qt.AlignmentFlag.AlignCenter, str(text))
            
        painter.restore()
