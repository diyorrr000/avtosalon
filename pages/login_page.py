from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLineEdit, QPushButton, QLabel, QHBoxLayout, QCheckBox
from PyQt6.QtCore import Qt, pyqtSignal
import bcrypt
import sqlite3

class LoginPage(QWidget):
    login_success = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Login Card
        self.card = QFrame()
        self.card.setObjectName("MicaCard")
        self.card.setFixedSize(400, 550)
        self.card_layout = QVBoxLayout(self.card)
        self.card_layout.setContentsMargins(40, 40, 40, 40)
        self.card_layout.setSpacing(20)

        # Header
        self.title = QLabel("Kirish")
        self.title.setObjectName("Headline")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.card_layout.addWidget(self.title)

        self.subtitle = QLabel("Xavfsiz Tizimga Kirish Protocol v4.0")
        self.subtitle.setObjectName("Subheadline")
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.card_layout.addWidget(self.subtitle)

        # Fields
        self.username = QLineEdit()
        self.username.setPlaceholderText("Foydalanuvchi nomi")
        self.username.setObjectName("SearchInput")
        self.username.setFixedHeight(45)
        self.card_layout.addWidget(self.username)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Parol")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setObjectName("SearchInput")
        self.password.setFixedHeight(45)
        self.card_layout.addWidget(self.password)

        # Options
        self.options_layout = QHBoxLayout()
        self.remember_me = QCheckBox("Meni eslab qol")
        self.options_layout.addWidget(self.remember_me)
        self.card_layout.addLayout(self.options_layout)

        # Login Button
        self.login_btn = QPushButton("TIZIMGA KIRISH")
        self.login_btn.setObjectName("LoginButton")
        self.login_btn.setFixedHeight(50)
        self.login_btn.clicked.connect(self.handle_login)
        self.card_layout.addWidget(self.login_btn)

        # Error message
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #ffb4ab; font-size: 12px;")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.card_layout.addWidget(self.error_label)

        self.layout.addWidget(self.card)

    def handle_login(self):
        username = self.username.text()
        password = self.password.text().encode('utf-8')

        conn = sqlite3.connect('d:/Backup/Desktop/Avtosalon/BizProcessOptimizerPro/database/app.db')
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash, role, display_name FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()

        if result:
            db_hash = result[0].encode('utf-8')
            if bcrypt.checkpw(password, db_hash):
                self.login_success.emit({
                    "username": username,
                    "role": result[1],
                    "display_name": result[2]
                })
                return
        
        self.error_label.setText("Foydalanuvchi nomi yoki parol xato!")
