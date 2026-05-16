from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt
import pyqtgraph as pg
import sqlite3

DB_PATH = 'd:/Backup/Desktop/Avtosalon/BizProcessOptimizerPro/database/app.db'

class DashboardPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(25)

        # Welcome Section
        self.welcome_frame = QFrame()
        self.welcome_frame.setObjectName("MicaCard")
        self.welcome_frame.setFixedHeight(120)
        self.welcome_layout = QVBoxLayout(self.welcome_frame)
        self.welcome_title = QLabel("Xayrli kun, Administrator! 👋")
        self.welcome_title.setObjectName("Headline")
        self.welcome_sub = QLabel("Tizim barqaror ishlamoqda. Bugungi ko'rsatkichlar optimallashtirilgan holatda.")
        self.welcome_sub.setObjectName("Subheadline")
        self.welcome_layout.addWidget(self.welcome_title)
        self.welcome_layout.addWidget(self.welcome_sub)
        self.layout.addWidget(self.welcome_frame)

        # Stats Grid
        self.stats_layout = QHBoxLayout()
        self.stats_layout.setSpacing(20)
        
        self.sale_stat_lbl = QLabel("$0")
        self.cust_stat_lbl = QLabel("0")
        self.car_stat_lbl = QLabel("0")
        self.rev_stat_lbl = QLabel("$0")
        
        self.sale_stat = self._create_stat_card("Umumiy Savdo Aylanmasi", self.sale_stat_lbl, "Faol", "#00ffa3")
        self.cust_stat = self._create_stat_card("Aktiv Mijozlar", self.cust_stat_lbl, "Faol", "#3cd7ff")
        self.car_stat = self._create_stat_card("Ombordagi Mashinalar", self.car_stat_lbl, "Mavjud", "#feb528")
        self.rev_stat = self._create_stat_card("Bu Oydagi Foyda", self.rev_stat_lbl, "O'sish", "#00ffa3")
        
        self.stats_layout.addWidget(self.sale_stat)
        self.stats_layout.addWidget(self.cust_stat)
        self.stats_layout.addWidget(self.car_stat)
        self.stats_layout.addWidget(self.rev_stat)
        self.layout.addLayout(self.stats_layout)

        # Main Content (Chart + Table)
        self.main_content = QHBoxLayout()
        self.main_content.setSpacing(20)

        # Chart
        self.chart_frame = QFrame()
        self.chart_frame.setObjectName("MicaCard")
        self.chart_layout = QVBoxLayout(self.chart_frame)
        self.chart_label = QLabel("So'nggi Tranzaksiyalar Grafigi")
        self.chart_label.setStyleSheet("font-weight: bold; font-size: 16px; margin-bottom: 10px;")
        self.chart_layout.addWidget(self.chart_label)
        
        self.plot = pg.PlotWidget()
        self.plot.setBackground('transparent')
        self.plot.showGrid(x=True, y=True, alpha=0.1)
        # Dummy data for chart (we could fetch from DB, but keeping dummy line for looks, 
        # or we will plot actual sales later if there's enough data)
        self.chart_layout.addWidget(self.plot)
        self.main_content.addWidget(self.chart_frame, 2)

        # Table
        self.table_frame = QFrame()
        self.table_frame.setObjectName("MicaCard")
        self.table_layout = QVBoxLayout(self.table_frame)
        self.table_label = QLabel("So'nggi Tranzaksiyalar")
        self.table_label.setStyleSheet("font-weight: bold; font-size: 16px; margin-bottom: 10px;")
        self.table_layout.addWidget(self.table_label)
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Sana", "Mijoz", "Avtomobil", "Summa"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setStyleSheet("background-color: transparent; border: none;")
        self.table_layout.addWidget(self.table)
        self.main_content.addWidget(self.table_frame, 3)

        self.layout.addLayout(self.main_content)

        self.refresh_data()

    def _create_stat_card(self, label_text, val_lbl, trend, trend_color):
        card = QFrame()
        card.setObjectName("MicaCard")
        card.setFixedHeight(120)
        layout = QVBoxLayout(card)
        
        h_layout = QHBoxLayout()
        val_lbl.setObjectName("StatValue")
        trend_label = QLabel(trend)
        trend_label.setStyleSheet(f"color: {trend_color}; font-weight: bold;")
        h_layout.addWidget(val_lbl)
        h_layout.addStretch()
        h_layout.addWidget(trend_label)
        
        lbl = QLabel(label_text)
        lbl.setObjectName("StatLabel")
        
        layout.addLayout(h_layout)
        layout.addWidget(lbl)
        return card

    def refresh_data(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            # Total customers
            c_cnt = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
            self.cust_stat_lbl.setText(str(c_cnt))
            
            # Vehicles available
            v_cnt = conn.execute("SELECT COUNT(*) FROM vehicles WHERE status='Available'").fetchone()[0]
            self.car_stat_lbl.setText(str(v_cnt))
            
            # Total Sales Amount
            s_sum = conn.execute("SELECT SUM(price) FROM sales").fetchone()[0]
            s_sum = s_sum if s_sum else 0
            self.sale_stat_lbl.setText(f"${s_sum:,.0f}")
            
            # This month revenue (simple sum for demo using total sales for now)
            self.rev_stat_lbl.setText(f"${s_sum:,.0f}")

            # Recent 5 transactions
            res = conn.execute('''
                SELECT strftime('%Y-%m-%d %H:%M', s.sale_date), c.name, v.brand || ' ' || v.model, s.price 
                FROM sales s
                JOIN customers c ON s.customer_id = c.id
                JOIN vehicles v ON s.vehicle_id = v.id
                ORDER BY s.sale_date DESC LIMIT 5
            ''').fetchall()
            
            self.table.setRowCount(len(res))
            sales_prices = []
            for r, d in enumerate(res):
                sales_prices.append(d[3])
                for c, v in enumerate(d):
                    item = QTableWidgetItem(str(v))
                    if c == 3: item.setText(f"${float(v):,.2f}")
                    self.table.setItem(r, c, item)

            # Update Chart based on latest 5 sales (reversed chronological)
            if sales_prices:
                sales_prices.reverse()
                self.plot.clear()
                self.plot.plot(list(range(1, len(sales_prices)+1)), sales_prices, pen=pg.mkPen(color='#3cd7ff', width=3))

            conn.close()
        except Exception as e:
            print("Dashboard refresh error:", e)
