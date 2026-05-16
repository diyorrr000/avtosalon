from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, 
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QDialog, QFormLayout, QMessageBox)
from PyQt6.QtCore import Qt
import sqlite3

DB_PATH = 'd:/Backup/Desktop/Avtosalon/BizProcessOptimizerPro/database/app.db'

class AddCustomerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Yangi Mijoz Qo'shish")
        self.setFixedSize(400, 250)
        self.setStyleSheet("""
            QDialog { background-color: #0f1923; color: #e8f4fd; }
            QLabel { color: #e8f4fd; }
            QLineEdit {
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
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.address_input = QLineEdit()
        
        form.addRow("F.I.O:", self.name_input)
        form.addRow("Telefon:", self.phone_input)
        form.addRow("Email:", self.email_input)
        form.addRow("Manzil:", self.address_input)
        
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
        return (self.name_input.text().strip(), self.phone_input.text().strip(),
                self.email_input.text().strip(), self.address_input.text().strip())

class CustomerPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(20)

        # Header
        self.header = QHBoxLayout()
        self.title = QLabel("Mijozlar Bazasi (CRM)")
        self.title.setObjectName("Headline")
        self.header.addWidget(self.title)
        
        self.header.addStretch()
        
        self.search = QLineEdit()
        self.search.setPlaceholderText("Ism yoki Tel qidirish...")
        self.search.setObjectName("SearchInput")
        self.search.setFixedWidth(250)
        self.search.textChanged.connect(self.refresh_data)
        self.header.addWidget(self.search)
        
        self.add_btn = QPushButton("+ YANGI MIJOZ")
        self.add_btn.setObjectName("PrimaryButton")
        self.add_btn.clicked.connect(self.add_customer)
        self.header.addWidget(self.add_btn)
        
        self.layout.addLayout(self.header)

        # Table
        self.table_frame = QFrame()
        self.table_frame.setObjectName("MicaCard")
        self.table_layout = QVBoxLayout(self.table_frame)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "F.I.O", "Telefon", "Email", "Umumiy Xarid"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_layout.addWidget(self.table)
        
        self.layout.addWidget(self.table_frame)
        self.refresh_data()
        
    def add_customer(self):
        dlg = AddCustomerDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            data = dlg.get_data()
            if not data[0]:
                QMessageBox.warning(self, "Xato", "Mijoz ismi kiritilishi shart!")
                return
            try:
                conn = sqlite3.connect(DB_PATH)
                conn.execute("INSERT INTO customers (name, phone, email, address) VALUES (?, ?, ?, ?)", data)
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
            cursor.execute("SELECT id, name, phone, email, total_purchases FROM customers WHERE name LIKE ? OR phone LIKE ?", 
                           (f'%{search_text}%', f'%{search_text}%'))
        else:
            cursor.execute("SELECT id, name, phone, email, total_purchases FROM customers")
        
        customers = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(customers))
        for row, data in enumerate(customers):
            for col, value in enumerate(data):
                item = QTableWidgetItem(str(value))
                if col == 4: # Price
                    item.setText(f"${float(value):,.2f}")
                self.table.setItem(row, col, item)
