from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel,
    QComboBox, QPushButton, QFormLayout, QMessageBox)
from PyQt6.QtCore import Qt
import sqlite3, shutil, os, json
from datetime import datetime

DB_PATH = 'd:/Backup/Desktop/Avtosalon/BizProcessOptimizerPro/database/app.db'
CONFIG_PATH = 'd:/Backup/Desktop/Avtosalon/BizProcessOptimizerPro/config.json'

class SettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)

        # Header
        title = QLabel("⚙️ Tizim Sozlamalari")
        title.setObjectName("Headline")
        layout.addWidget(title)

        # General Settings
        gen_card = QFrame()
        gen_card.setObjectName("MicaCard")
        gen_layout = QFormLayout(gen_card)
        gen_layout.setContentsMargins(30, 24, 30, 24)
        gen_layout.setSpacing(18)

        sec_title = QLabel("Umumiy Sozlamalar")
        sec_title.setStyleSheet("font-weight:bold;font-size:15px;color:#3cd7ff;margin-bottom:8px;")
        gen_layout.addRow(sec_title)

        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["O'zbekcha 🇺🇿", "English 🇬🇧", "Русский 🇷🇺"])
        self.lang_combo.setFixedHeight(40)
        gen_layout.addRow("Tizim tili:", self.lang_combo)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["🌑 Dark Mode (Glassmorphism)", "☀️ Light Mode"])
        self.theme_combo.setFixedHeight(40)
        gen_layout.addRow("Mavzu (Theme):", self.theme_combo)

        self.curr_combo = QComboBox()
        self.curr_combo.addItems(["USD ($)", "UZS (so'm)", "EUR (€)"])
        self.curr_combo.setFixedHeight(40)
        gen_layout.addRow("Valyuta:", self.curr_combo)

        layout.addWidget(gen_card)

        # Database
        db_card = QFrame()
        db_card.setObjectName("MicaCard")
        db_layout = QFormLayout(db_card)
        db_layout.setContentsMargins(30, 24, 30, 24)
        db_layout.setSpacing(18)

        db_title = QLabel("Ma'lumotlar Bazasi")
        db_title.setStyleSheet("font-weight:bold;font-size:15px;color:#3cd7ff;margin-bottom:8px;")
        db_layout.addRow(db_title)

        self.backup_btn = QPushButton("💾 DATABASE BACKUP QILISH")
        self.backup_btn.setObjectName("PrimaryButton")
        self.backup_btn.setFixedHeight(44)
        self.backup_btn.clicked.connect(self.do_backup)
        db_layout.addRow("Zaxira nusxa:", self.backup_btn)

        self.stats_lbl = QLabel()
        self.stats_lbl.setStyleSheet("color:#bbc9cf;font-size:12px;")
        db_layout.addRow("Holati:", self.stats_lbl)

        layout.addWidget(db_card)

        # Save Button
        save_row = QHBoxLayout()
        save_row.addStretch()
        self.save_btn = QPushButton("✅ SOZLAMALARNI SAQLASH")
        self.save_btn.setObjectName("PrimaryButton")
        self.save_btn.setFixedHeight(48)
        self.save_btn.setFixedWidth(260)
        self.save_btn.clicked.connect(self.save_settings)
        save_row.addWidget(self.save_btn)
        layout.addLayout(save_row)

        layout.addStretch()
        
        self.load_settings()
        self.refresh_data()

    def load_settings(self):
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, 'r') as f:
                    config = json.load(f)
                    
                lang = config.get("language", "uz")
                theme = config.get("theme", "dark")
                
                # set combo indexes
                if lang == "en": self.lang_combo.setCurrentIndex(1)
                elif lang == "ru": self.lang_combo.setCurrentIndex(2)
                else: self.lang_combo.setCurrentIndex(0)
                
                if theme == "light": self.theme_combo.setCurrentIndex(1)
                else: self.theme_combo.setCurrentIndex(0)
            except:
                pass

    def refresh_data(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            v = conn.execute("SELECT COUNT(*) FROM vehicles").fetchone()[0]
            c = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
            s = conn.execute("SELECT COUNT(*) FROM sales").fetchone()[0]
            conn.close()
            self.stats_lbl.setText(f"Avtomobillar: {v} ta | Mijozlar: {c} ta | Savdolar: {s} ta")
        except:
            self.stats_lbl.setText("Ma'lumot olishda xato.")

    def do_backup(self):
        try:
            backup_dir = 'd:/Backup/Desktop/Avtosalon/BizProcessOptimizerPro/backup'
            os.makedirs(backup_dir, exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            dest = os.path.join(backup_dir, f"app_backup_{ts}.db")
            shutil.copy(DB_PATH, dest)
            QMessageBox.information(self, "Muvaffaqiyat", f"Backup saqlandi!\n📁 {dest}")
        except Exception as e:
            QMessageBox.critical(self, "Xato", f"Backup xatosi: {e}")

    def save_settings(self):
        lang_idx = self.lang_combo.currentIndex()
        theme_idx = self.theme_combo.currentIndex()
        
        lang = "uz" if lang_idx == 0 else ("en" if lang_idx == 1 else "ru")
        theme = "dark" if theme_idx == 0 else "light"
        
        config = {"language": lang, "theme": theme, "currency": "usd"}
        
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f)
            
        QMessageBox.information(self, "Saqlandi", 
            "✅ Sozlamalar muvaffaqiyatli saqlandi.\nO'zgarishlar kuchga kirishi uchun dasturni qayta yoping va oching (Restart).")
