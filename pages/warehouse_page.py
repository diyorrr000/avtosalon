from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, 
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QMessageBox, QDialog, QFormLayout, QSpinBox, QDoubleSpinBox)
from PyQt6.QtCore import Qt
import sqlite3

DB_PATH = 'd:/Backup/Desktop/Avtosalon/BizProcessOptimizerPro/database/app.db'

class AddPartDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Yangi Ehtiyot Qism")
        self.setFixedSize(400, 300)
        self.setStyleSheet("""
            QDialog { background-color: #0f1923; color: #e8f4fd; }
            QLabel { color: #e8f4fd; }
            QLineEdit, QSpinBox, QDoubleSpinBox {
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
        form = QFormLayout()
        
        self.name_input = QLineEdit()
        self.qty_input = QSpinBox()
        self.qty_input.setRange(0, 99999)
        self.min_qty_input = QSpinBox()
        self.min_qty_input.setRange(0, 99999)
        self.min_qty_input.setValue(10)
        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0, 999999)
        self.price_input.setPrefix("$")
        
        form.addRow("Qism Nomi:", self.name_input)
        form.addRow("Hozirgi Miqdor:", self.qty_input)
        form.addRow("Minimal Limit:", self.min_qty_input)
        form.addRow("Narxi:", self.price_input)
        
        layout.addLayout(form)
        
        btn_layout = QHBoxLayout()
        self.cancel_btn = QPushButton("Bekor")
        self.cancel_btn.setStyleSheet("background: rgba(255,255,255,0.1); color: #e8f4fd;")
        self.cancel_btn.clicked.connect(self.reject)
        
        self.save_btn = QPushButton("Saqlash")
        self.save_btn.clicked.connect(self.accept)
        
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.save_btn)
        layout.addLayout(btn_layout)

    def get_data(self):
        return (self.name_input.text().strip(), self.qty_input.value(),
                self.min_qty_input.value(), self.price_input.value())


class WarehousePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(20)

        # Header
        self.header = QHBoxLayout()
        self.title = QLabel("Ehtiyot Qismlar Ombori")
        self.title.setObjectName("Headline")
        self.header.addWidget(self.title)
        
        self.header.addStretch()
        
        self.search = QLineEdit()
        self.search.setPlaceholderText("Qism nomini qidirish...")
        self.search.setObjectName("SearchInput")
        self.search.setFixedWidth(250)
        self.search.textChanged.connect(self.refresh_data)
        self.header.addWidget(self.search)
        
        self.add_btn = QPushButton("+ QISM QO'SHISH")
        self.add_btn.setObjectName("PrimaryButton")
        self.add_btn.clicked.connect(self.add_part)
        self.header.addWidget(self.add_btn)
        
        self.layout.addLayout(self.header)

        # Table
        self.table_frame = QFrame()
        self.table_frame.setObjectName("MicaCard")
        self.table_layout = QVBoxLayout(self.table_frame)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Nom", "Miqdor", "Minimal Miqdor", "Narx ($)"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_layout.addWidget(self.table)
        
        self.layout.addWidget(self.table_frame)
        
        # Low Stock Alert Area
        self.alert_frame = QFrame()
        self.alert_frame.setObjectName("MicaCard")
        self.alert_frame.setStyleSheet("border: 1px solid #ffb4ab;")
        self.alert_layout = QHBoxLayout(self.alert_frame)
        self.alert_text = QLabel("DIQQAT: Ayrim ehtiyot qismlar zahirasi kamaymoqda!")
        self.alert_text.setStyleSheet("color: #ffb4ab; font-weight: bold;")
        self.alert_layout.addWidget(self.alert_text)
        self.layout.addWidget(self.alert_frame)
        self.alert_frame.hide()

        self.refresh_data()
        
    def add_part(self):
        dlg = AddPartDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            data = dlg.get_data()
            if not data[0]:
                QMessageBox.warning(self, "Xato", "Qism nomini kiritish shart!")
                return
            try:
                conn = sqlite3.connect(DB_PATH)
                conn.execute("INSERT INTO warehouse (part_name, quantity, min_quantity, price) VALUES (?, ?, ?, ?)", data)
                conn.commit()
                conn.close()
                self.refresh_data()
            except Exception as e:
                QMessageBox.critical(self, "Xato", str(e))

    def refresh_data(self):
        search_text = self.search.text()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        if search_text:
            cursor.execute("SELECT id, part_name, quantity, min_quantity, price FROM warehouse WHERE part_name LIKE ?", 
                           (f'%{search_text}%',))
        else:
            cursor.execute("SELECT id, part_name, quantity, min_quantity, price FROM warehouse")
        
        parts = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(parts))
        has_alert = False
        for row, data in enumerate(parts):
            for col, value in enumerate(data):
                item = QTableWidgetItem(str(value))
                if col == 2 and int(value) <= data[3]: # current <= min
                    item.setStyleSheet("color: #ffb4ab; font-weight: bold;")
                    has_alert = True
                self.table.setItem(row, col, item)
        
        if has_alert:
            self.alert_frame.show()
        else:
            self.alert_frame.hide()
