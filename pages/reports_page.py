from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton
from PyQt6.QtCore import Qt
import sqlite3

class ReportsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(25)

        # Header
        self.header = QHBoxLayout()
        self.title = QLabel("Tahlil va Hisobotlar")
        self.title.setObjectName("Headline")
        self.header.addWidget(self.title)
        
        self.header.addStretch()
        
        self.export_pdf = QPushButton("PDF EXPORT")
        self.export_excel = QPushButton("EXCEL EXPORT")
        self.export_pdf.setFixedHeight(40)
        self.export_excel.setFixedHeight(40)
        self.header.addWidget(self.export_pdf)
        self.header.addWidget(self.export_excel)
        
        self.layout.addLayout(self.header)

        # Summary Grid
        self.summary_layout = QHBoxLayout()
        self.today_sales = self._create_summary_box("Bugungi Savdo", "$45,200")
        self.month_sales = self._create_summary_box("Oylik Savdo", "$890,000")
        self.total_profit = self._create_summary_box("Jami Foyda", "$1.1M")
        
        self.summary_layout.addWidget(self.today_sales)
        self.summary_layout.addWidget(self.month_sales)
        self.summary_layout.addWidget(self.total_profit)
        self.layout.addLayout(self.summary_layout)

        # Detailed Report Table
        self.table_frame = QFrame()
        self.table_frame.setObjectName("MicaCard")
        self.table_layout = QVBoxLayout(self.table_frame)
        
        self.title_label = QLabel("Batafsil Savdo Hisoboti")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 16px; margin-bottom: 10px;")
        self.table_layout.addWidget(self.title_label)
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Sana", "Mijoz", "Avtomobil", "Summa"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_layout.addWidget(self.table)
        
        self.layout.addWidget(self.table_frame)
        self.refresh_data()

    def _create_summary_box(self, label, value):
        box = QFrame()
        box.setObjectName("MicaCard")
        layout = QVBoxLayout(box)
        val = QLabel(value)
        val.setStyleSheet("font-size: 24px; font-weight: bold; color: #00ffa3;")
        lbl = QLabel(label)
        lbl.setStyleSheet("color: #bbc9cf; font-size: 12px; text-transform: uppercase;")
        layout.addWidget(val)
        layout.addWidget(lbl)
        return box

    def refresh_data(self):
        conn = sqlite3.connect('d:/Backup/Desktop/Avtosalon/BizProcessOptimizerPro/database/app.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.sale_date, c.name, v.brand || ' ' || v.model, s.price 
            FROM sales s
            JOIN customers c ON s.customer_id = c.id
            JOIN vehicles v ON s.vehicle_id = v.id
            ORDER BY s.sale_date DESC
        """)
        rows = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(rows))
        for r, data in enumerate(rows):
            for c, val in enumerate(data):
                item = QTableWidgetItem(str(val))
                if c == 3:
                    item.setText(f"${float(val):,.2f}")
                self.table.setItem(r, c, item)
