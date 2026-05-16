from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame

class VehiclePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.frame = QFrame()
        self.frame.setObjectName("MicaCard")
        self.l = QVBoxLayout(self.frame)
        self.l.addWidget(QLabel("Avtomobillar Tizimi"))
        self.layout.addWidget(self.frame)

class CustomerPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.frame = QFrame()
        self.frame.setObjectName("MicaCard")
        self.l = QVBoxLayout(self.frame)
        self.l.addWidget(QLabel("Mijozlar Tizimi"))
        self.layout.addWidget(self.frame)

class SalesPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.frame = QFrame()
        self.frame.setObjectName("MicaCard")
        self.l = QVBoxLayout(self.frame)
        self.l.addWidget(QLabel("Savdo Moduli"))
        self.layout.addWidget(self.frame)
