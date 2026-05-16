from PyQt6.QtWidgets import QFrame, QVBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy
from PyQt6.QtCore import pyqtSignal

class Sidebar(QFrame):
    nav_requested = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setFixedWidth(260)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 28, 16, 28)
        layout.setSpacing(4)

        # Logo
        logo = QLabel("BizProcess")
        logo.setStyleSheet("font-size:22px;font-weight:bold;color:#3cd7ff;")
        sub  = QLabel("Optimizer Pro")
        sub.setStyleSheet("font-size:11px;color:#bbc9cf;margin-bottom:20px;")
        layout.addWidget(logo)
        layout.addWidget(sub)

        # Nav buttons
        self._btn("🏠  Dashboard",     "dashboard",  layout)
        self._btn("🚗  Avtomobillar",  "vehicles",   layout)
        self._btn("👥  Mijozlar",      "customers",  layout)
        self._btn("💰  Savdo",         "sales",      layout)
        self._btn("📦  Ombor",         "warehouse",  layout)
        self._btn("📊  Hisobotlar",    "reports",    layout)
        self._btn("⚙️  Sozlamalar",   "settings",   layout)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Logout
        self.logout_btn = QPushButton("🚪  Chiqish")
        self.logout_btn.setObjectName("SidebarItem")
        self.logout_btn.setStyleSheet(
            "QPushButton{color:#ff6b6b;background:rgba(255,107,107,0.1);border:none;"
            "border-radius:8px;padding:10px 16px;text-align:left;font-size:13px;}"
            "QPushButton:hover{background:rgba(255,107,107,0.2);}")
        layout.addWidget(self.logout_btn)

    def _btn(self, text, page_id, layout):
        btn = QPushButton(text)
        btn.setObjectName("SidebarItem")
        btn.clicked.connect(lambda: self.nav_requested.emit(page_id))
        layout.addWidget(btn)
        return btn
