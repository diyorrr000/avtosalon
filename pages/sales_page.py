from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QComboBox, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
from PyQt6.QtCore import Qt
import sqlite3
import datetime

DB_PATH = 'd:/Backup/Desktop/Avtosalon/BizProcessOptimizerPro/database/app.db'

class SalesPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(25)

        # Header
        self.title = QLabel("Yangi Savdo Rasmiylashtirish")
        self.title.setObjectName("Headline")
        self.layout.addWidget(self.title)

        # Form Area
        self.form_frame = QFrame()
        self.form_frame.setObjectName("MicaCard")
        self.form_layout = QVBoxLayout(self.form_frame)
        self.form_layout.setContentsMargins(30, 30, 30, 30)
        self.form_layout.setSpacing(20)

        # Customer Selection
        self.cust_layout = QHBoxLayout()
        self.cust_label = QLabel("Mijozni tanlang:")
        self.cust_combo = QComboBox()
        self.cust_combo.setFixedHeight(40)
        self.cust_layout.addWidget(self.cust_label)
        self.cust_layout.addWidget(self.cust_combo, 1)
        self.form_layout.addLayout(self.cust_layout)

        # Vehicle Selection
        self.vec_layout = QHBoxLayout()
        self.vec_label = QLabel("Avtomobilni tanlang:")
        self.vec_combo = QComboBox()
        self.vec_combo.setFixedHeight(40)
        self.vec_layout.addWidget(self.vec_label)
        self.vec_layout.addWidget(self.vec_combo, 1)
        self.form_layout.addLayout(self.vec_layout)

        # Price Info
        self.price_layout = QHBoxLayout()
        self.price_label = QLabel("Sotish narxi ($):")
        self.price_input = QLineEdit()
        self.price_input.setObjectName("SearchInput")
        self.price_input.setFixedHeight(40)
        self.price_layout.addWidget(self.price_label)
        self.price_layout.addWidget(self.price_input, 1)
        self.form_layout.addLayout(self.price_layout)

        # Action Buttons
        self.btn_layout = QHBoxLayout()
        self.process_btn = QPushButton("SAVDONI TASDIQLASH")
        self.process_btn.setObjectName("PrimaryButton")
        self.process_btn.setFixedHeight(50)
        self.process_btn.clicked.connect(self.process_sale)
        
        self.invoice_btn = QPushButton("PDF INVOICE")
        self.invoice_btn.setFixedHeight(50)
        self.invoice_btn.setFixedWidth(150)
        
        self.btn_layout.addWidget(self.invoice_btn)
        self.btn_layout.addStretch()
        self.btn_layout.addWidget(self.process_btn)
        self.form_layout.addLayout(self.btn_layout)

        self.layout.addWidget(self.form_frame)
        self.layout.addStretch()

        self.refresh_data()

    def refresh_data(self):
        # Clear existing combos
        self.cust_combo.clear()
        self.vec_combo.clear()

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Load Customers
        cursor.execute("SELECT id, name FROM customers")
        for c in cursor.fetchall():
            self.cust_combo.addItem(f"{c[1]} (ID: {c[0]})", c[0])
            
        # Load Available Vehicles
        cursor.execute("SELECT id, brand, model, price FROM vehicles WHERE status = 'Available'")
        for v in cursor.fetchall():
            self.vec_combo.addItem(f"{v[1]} {v[2]} - ${v[3]:,.2f}", v[0])
            
        conn.close()

    def process_sale(self):
        cust_id = self.cust_combo.currentData()
        vec_id = self.vec_combo.currentData()
        price = self.price_input.text()

        if not cust_id or not vec_id or not price:
            QMessageBox.warning(self, "Xato", "Barcha maydonlarni to'ldiring!")
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # Record sale
            cursor.execute("INSERT INTO sales (customer_id, vehicle_id, price, status) VALUES (?, ?, ?, 'Completed')",
                           (cust_id, vec_id, float(price),))
            
            # Update vehicle status
            cursor.execute("UPDATE vehicles SET status = 'Sold' WHERE id = ?", (vec_id,))
            
            # Update customer total spending
            cursor.execute("UPDATE customers SET total_purchases = total_purchases + ? WHERE id = ?", (float(price), cust_id))
            
            conn.commit()
            conn.close()
            
            QMessageBox.information(self, "Muvaffaqiyat", "Savdo muvaffaqiyatli rasmiylashtirildi!")
            self.price_input.clear()
            self.refresh_data()
        except Exception as e:
            QMessageBox.critical(self, "Xato", f"Xatolik yuz berdi: {str(e)}")
