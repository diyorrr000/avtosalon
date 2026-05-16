from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel,
    QLineEdit, QPushButton, QScrollArea, QGridLayout, QDialog, QFormLayout,
    QComboBox, QSpinBox, QDoubleSpinBox, QMessageBox, QSizePolicy)
from PyQt6.QtCore import Qt
import sqlite3

DB_PATH = 'd:/Backup/Desktop/Avtosalon/BizProcessOptimizerPro/database/app.db'

class AddVehicleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Yangi Avtomobil Qo'shish")
        self.setFixedSize(420, 360)
        self.setStyleSheet("""
            QDialog { background-color: #0f1923; color: #e8f4fd; }
            QLabel { color: #e8f4fd; }
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
                background: rgba(255,255,255,0.07);
                border: 1px solid rgba(60,215,255,0.3);
                border-radius: 6px; color: #e8f4fd; padding: 6px; min-height: 30px;
            }
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #3cd7ff,stop:1 #0099cc);
                color: #0f1923; border-radius: 8px; font-weight: bold; padding: 8px 20px;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        form = QFormLayout()
        form.setSpacing(12)

        self.brand = QLineEdit(); self.brand.setPlaceholderText("Chevrolet, Kia, BYD...")
        self.model = QLineEdit(); self.model.setPlaceholderText("Tracker, K5, Song Plus...")
        self.year = QSpinBox(); self.year.setRange(2000, 2030); self.year.setValue(2024)
        self.vin = QLineEdit(); self.vin.setPlaceholderText("VIN raqami")
        self.price = QDoubleSpinBox(); self.price.setRange(1000, 999999); self.price.setValue(20000); self.price.setPrefix("$")
        self.status = QComboBox(); self.status.addItems(["Available", "Sold", "Reserved"])

        form.addRow("Brend:", self.brand)
        form.addRow("Model:", self.model)
        form.addRow("Yil:", self.year)
        form.addRow("VIN:", self.vin)
        form.addRow("Narx:", self.price)
        form.addRow("Holat:", self.status)
        layout.addLayout(form)

        btn_row = QHBoxLayout()
        self.cancel_btn = QPushButton("Bekor")
        self.cancel_btn.setStyleSheet("background: rgba(255,255,255,0.1); color: #e8f4fd;")
        self.save_btn = QPushButton("Saqlash")
        self.cancel_btn.clicked.connect(self.reject)
        self.save_btn.clicked.connect(self.accept)
        btn_row.addWidget(self.cancel_btn)
        btn_row.addWidget(self.save_btn)
        layout.addLayout(btn_row)

    def get_data(self):
        return (self.brand.text().strip(), self.model.text().strip(),
                self.year.value(), self.vin.text().strip(),
                self.price.value(), self.status.currentText())


class VehicleCard(QFrame):
    def __init__(self, vehicle_data, on_delete=None, on_edit=None, parent=None):
        super().__init__(parent)
        self.vehicle_id = vehicle_data[0]
        self.on_delete = on_delete
        self.setObjectName("MicaCard")
        self.setFixedSize(270, 290)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(6)

        # Brand + Model
        title = QLabel(f"{vehicle_data[1]} {vehicle_data[2]}")
        title.setStyleSheet("font-weight:bold;font-size:16px;color:#e8f4fd;")
        layout.addWidget(title)

        # Year
        year_lbl = QLabel(f"📅 {vehicle_data[3]} yil")
        year_lbl.setStyleSheet("color:#bbc9cf;font-size:12px;")
        layout.addWidget(year_lbl)

        # VIN
        vin_lbl = QLabel(f"🔑 VIN: {vehicle_data[4]}")
        vin_lbl.setStyleSheet("color:#bbc9cf;font-size:11px;")
        layout.addWidget(vin_lbl)

        # Price
        price_lbl = QLabel(f"${vehicle_data[5]:,.0f}")
        price_lbl.setStyleSheet("color:#3cd7ff;font-weight:bold;font-size:20px;")
        layout.addWidget(price_lbl)

        # Status Badge
        status = vehicle_data[6]
        color = "#00ffa3" if status == "Available" else ("#feb528" if status == "Reserved" else "#ff6b6b")
        status_lbl = QLabel(f"● {status}")
        status_lbl.setStyleSheet(f"color:{color};font-weight:bold;font-size:12px;")
        layout.addWidget(status_lbl)

        layout.addStretch()

        # Buttons row
        btn_row = QHBoxLayout()
        edit_btn = QPushButton("✏️ Tahrir")
        edit_btn.setStyleSheet("""QPushButton{background:rgba(60,215,255,0.15);color:#3cd7ff;
            border:1px solid rgba(60,215,255,0.4);border-radius:6px;padding:4px 10px;font-size:11px;}
            QPushButton:hover{background:rgba(60,215,255,0.3);}""")
        del_btn = QPushButton("🗑️ O'chir")
        del_btn.setStyleSheet("""QPushButton{background:rgba(255,107,107,0.15);color:#ff6b6b;
            border:1px solid rgba(255,107,107,0.4);border-radius:6px;padding:4px 10px;font-size:11px;}
            QPushButton:hover{background:rgba(255,107,107,0.3);}""")
        edit_btn.clicked.connect(lambda: on_edit(self.vehicle_id) if on_edit else None)
        del_btn.clicked.connect(lambda: on_delete(self.vehicle_id) if on_delete else None)
        btn_row.addWidget(edit_btn)
        btn_row.addWidget(del_btn)
        layout.addLayout(btn_row)


class VehiclePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        main = QVBoxLayout(self)
        main.setContentsMargins(30, 30, 30, 30)
        main.setSpacing(20)

        # Header
        header = QHBoxLayout()
        title = QLabel("Avtomobillar Inventarizatsiyasi")
        title.setObjectName("Headline")
        header.addWidget(title)
        header.addStretch()

        self.search = QLineEdit()
        self.search.setPlaceholderText("🔍 Qidirish (Model, Brend, VIN)...")
        self.search.setObjectName("SearchInput")
        self.search.setFixedWidth(300)
        self.search.textChanged.connect(self.refresh_data)
        header.addWidget(self.search)

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Barchasi", "Available", "Sold", "Reserved"])
        self.filter_combo.setFixedWidth(130)
        self.filter_combo.setFixedHeight(38)
        self.filter_combo.currentTextChanged.connect(self.refresh_data)
        header.addWidget(self.filter_combo)

        add_btn = QPushButton("＋ YANGI QO'SHISH")
        add_btn.setObjectName("PrimaryButton")
        add_btn.setFixedHeight(38)
        add_btn.clicked.connect(self.add_vehicle)
        header.addWidget(add_btn)

        main.addLayout(header)

        # Stats bar
        self.stats_bar = QHBoxLayout()
        self.total_lbl = QLabel("Jami: 0")
        self.avail_lbl = QLabel("Mavjud: 0")
        self.sold_lbl  = QLabel("Sotilgan: 0")
        for lbl in [self.total_lbl, self.avail_lbl, self.sold_lbl]:
            lbl.setStyleSheet("color:#bbc9cf;font-size:13px;margin-right:20px;")
        self.stats_bar.addWidget(self.total_lbl)
        self.stats_bar.addWidget(self.avail_lbl)
        self.stats_bar.addWidget(self.sold_lbl)
        self.stats_bar.addStretch()
        main.addLayout(self.stats_bar)

        # Scroll Area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("background:transparent;border:none;")
        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("background:transparent;")
        self.grid = QGridLayout(self.scroll_content)
        self.grid.setSpacing(20)
        self.grid.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.scroll.setWidget(self.scroll_content)
        main.addWidget(self.scroll)

        self.refresh_data()

    def add_vehicle(self):
        dlg = AddVehicleDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            data = dlg.get_data()
            if not data[0] or not data[1]:
                QMessageBox.warning(self, "Xato", "Brend va model bo'sh bo'lishi mumkin emas!")
                return
            try:
                conn = sqlite3.connect(DB_PATH)
                conn.execute("INSERT INTO vehicles (brand,model,year,vin,price,status) VALUES (?,?,?,?,?,?)", data)
                conn.commit()
                conn.close()
                self.refresh_data()
            except Exception as e:
                QMessageBox.critical(self, "Xato", str(e))

    def delete_vehicle(self, vid):
        reply = QMessageBox.question(self, "O'chirish", "Ushbu avtomobilni o'chirishni tasdiqlaysizmi?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            conn = sqlite3.connect(DB_PATH)
            conn.execute("DELETE FROM vehicles WHERE id=?", (vid,))
            conn.commit()
            conn.close()
            self.refresh_data()

    def edit_vehicle(self, vid):
        conn = sqlite3.connect(DB_PATH)
        row = conn.execute("SELECT * FROM vehicles WHERE id=?", (vid,)).fetchone()
        conn.close()
        if not row:
            return
        dlg = AddVehicleDialog(self)
        dlg.setWindowTitle("Avtomobilni Tahrirlash")
        dlg.brand.setText(row[1]); dlg.model.setText(row[2])
        dlg.year.setValue(row[3]); dlg.vin.setText(row[4] or "")
        dlg.price.setValue(row[5])
        idx = dlg.status.findText(row[6])
        if idx >= 0: dlg.status.setCurrentIndex(idx)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            data = dlg.get_data()
            conn = sqlite3.connect(DB_PATH)
            conn.execute("UPDATE vehicles SET brand=?,model=?,year=?,vin=?,price=?,status=? WHERE id=?",
                         (*data, vid))
            conn.commit()
            conn.close()
            self.refresh_data()

    def refresh_data(self):
        # Clear grid safely
        while self.grid.count():
            item = self.grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        search_text = self.search.text()
        status_filter = self.filter_combo.currentText()

        conn = sqlite3.connect(DB_PATH)
        query = "SELECT * FROM vehicles WHERE (brand LIKE ? OR model LIKE ? OR vin LIKE ?)"
        params = [f'%{search_text}%'] * 3
        if status_filter != "Barchasi":
            query += " AND status=?"
            params.append(status_filter)
        vehicles = conn.execute(query, params).fetchall()

        # Stats
        total = conn.execute("SELECT COUNT(*) FROM vehicles").fetchone()[0]
        avail = conn.execute("SELECT COUNT(*) FROM vehicles WHERE status='Available'").fetchone()[0]
        sold  = conn.execute("SELECT COUNT(*) FROM vehicles WHERE status='Sold'").fetchone()[0]
        conn.close()

        self.total_lbl.setText(f"Jami: {total} ta")
        self.avail_lbl.setText(f"✅ Mavjud: {avail} ta")
        self.sold_lbl.setText(f"🔴 Sotilgan: {sold} ta")

        cols = 4
        for i, v in enumerate(vehicles):
            card = VehicleCard(v, on_delete=self.delete_vehicle, on_edit=self.edit_vehicle)
            self.grid.addWidget(card, i // cols, i % cols)
