import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QHBoxLayout
from ui.styles import StyleManager
from services.translation_service import TranslationManager
from database.db_manager import DatabaseManager
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.vehicle_page import VehiclePage
from pages.customer_page import CustomerPage
from pages.sales_page import SalesPage
from pages.warehouse_page import WarehousePage
from pages.reports_page import ReportsPage
from pages.settings_page import SettingsPage
from components.sidebar import Sidebar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BizProcess Optimizer Pro")
        self.resize(1500, 950)

        self.db = DatabaseManager()
        self.trans = TranslationManager()

        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.sidebar = Sidebar(self)
        root.addWidget(self.sidebar)
        self.sidebar.hide()

        self.stacked = QStackedWidget()
        root.addWidget(self.stacked)

        # Pages
        self.login_page     = LoginPage(self)
        self.dashboard_page = DashboardPage(self)
        self.vehicle_page   = VehiclePage(self)
        self.customer_page  = CustomerPage(self)
        self.sales_page     = SalesPage(self)
        self.warehouse_page = WarehousePage(self)
        self.reports_page   = ReportsPage(self)
        self.settings_page  = SettingsPage(self)

        for p in [self.login_page, self.dashboard_page, self.vehicle_page,
                  self.customer_page, self.sales_page, self.warehouse_page,
                  self.reports_page, self.settings_page]:
            self.stacked.addWidget(p)

        self.setStyleSheet(StyleManager.get_main_style())

        # Signals
        self.login_page.login_success.connect(self.on_login_success)
        self.sidebar.nav_requested.connect(self.navigate_to)
        self.sidebar.logout_btn.clicked.connect(self.logout)

    def on_login_success(self, user_info):
        self.current_user = user_info
        self.sidebar.show()
        self.stacked.setCurrentWidget(self.dashboard_page)
        self.dashboard_page.refresh_data()

    def logout(self):
        self.sidebar.hide()
        self.stacked.setCurrentWidget(self.login_page)

    def navigate_to(self, page_name):
        pages = {
            "dashboard":  self.dashboard_page,
            "vehicles":   self.vehicle_page,
            "customers":  self.customer_page,
            "sales":      self.sales_page,
            "warehouse":  self.warehouse_page,
            "reports":    self.reports_page,
            "settings":   self.settings_page,
        }
        if page_name in pages:
            self.stacked.setCurrentWidget(pages[page_name])
            if hasattr(pages[page_name], 'refresh_data'):
                pages[page_name].refresh_data()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
