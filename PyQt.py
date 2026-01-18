from PyQt6.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt

def create_card(icon_text, title, desc, callback):
    card = QFrame()
    card.setObjectName("card")

    layout = QVBoxLayout(card)
    layout.setSpacing(10)

    icon = QLabel(icon_text)
    icon.setObjectName("icon")
    icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

    lbl_title = QLabel(title)
    lbl_title.setObjectName("cardTitle")
    lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

    lbl_desc = QLabel(desc)
    lbl_desc.setObjectName("cardDesc")
    lbl_desc.setWordWrap(True)
    lbl_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)

    btn = QPushButton("Buka")
    btn.clicked.connect(callback)

    layout.addWidget(icon)
    layout.addWidget(lbl_title)
    layout.addWidget(lbl_desc)
    layout.addWidget(btn)

    return card