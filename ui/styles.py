class StyleManager:
    @staticmethod
    def get_main_style():
        return """
        * {
            font-family: 'Inter', sans-serif;
            color: #e5e2e1;
            outline: none;
        }

        QMainWindow {
            background-color: #0A0A0A;
        }

        /* Sidebar Style */
        QFrame#Sidebar {
            background-color: rgba(28, 27, 27, 0.9);
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }

        QPushButton#SidebarItem {
            text-align: left;
            padding: 10px 15px;
            background-color: transparent;
            border-radius: 8px;
            font-size: 14px;
            color: #bbc9cf;
        }

        QPushButton#SidebarItem:hover {
            background-color: rgba(58, 57, 57, 0.5);
            color: #e5e2e1;
        }

        QPushButton#SidebarItem[active="true"] {
            background-color: #3cd7ff;
            color: #003642;
            font-weight: bold;
        }

        /* Header Style */
        QFrame#Header {
            background-color: rgba(19, 19, 19, 0.8);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        QLineEdit#SearchInput {
            background-color: rgba(255, 255, 255, 0.05);
            border: none;
            border-radius: 15px;
            padding: 8px 15px;
            font-size: 14px;
            color: #e5e2e1;
        }

        /* Card Style */
        QFrame#MicaCard {
            background-color: rgba(28, 27, 27, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
        }

        QLabel#Headline {
            font-size: 24px;
            font-weight: bold;
            color: white;
        }

        QLabel#Subheadline {
            font-size: 14px;
            color: #bbc9cf;
        }

        /* Stats Cards */
        QLabel#StatValue {
            font-size: 28px;
            font-weight: bold;
            color: white;
        }

        QLabel#StatLabel {
            font-size: 12px;
            color: #bbc9cf;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        /* Buttons */
        QPushButton#PrimaryButton {
            background-color: #00ffa3;
            color: #003920;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: bold;
        }

        QPushButton#PrimaryButton:hover {
            background-color: #52ffac;
        }

        QPushButton#LoginButton {
            background-color: #3cd7ff;
            color: #001f27;
            border-radius: 8px;
            padding: 12px;
            font-size: 16px;
            font-weight: bold;
        }

        /* Table Style */
        QTableWidget {
            background-color: transparent;
            border: none;
            gridline-color: rgba(255, 255, 255, 0.05);
        }

        QHeaderView::section {
            background-color: rgba(255, 255, 255, 0.05);
            color: #bbc9cf;
            padding: 10px;
            border: none;
            text-transform: uppercase;
            font-size: 10px;
            font-weight: bold;
        }

        QTableWidget::item {
            padding: 10px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }
        """
