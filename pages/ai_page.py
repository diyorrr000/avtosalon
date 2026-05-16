from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QFrame, QScrollArea
from PyQt6.QtCore import Qt, pyqtSlot
from services.ai_service import AIService

class AIAssistantPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ai_service = AIService()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(20)

        # Header
        self.header = QFrame()
        self.header.setObjectName("MicaCard")
        self.header_layout = QHBoxLayout(self.header)
        self.title = QLabel("AI Yordamchi (DeepSeek Chat Pro)")
        self.title.setObjectName("Headline")
        self.header_layout.addWidget(self.title)
        self.layout.addWidget(self.header)

        # Chat Area
        self.chat_display = QTextEdit()
        self.chat_display.setObjectName("MicaCard")
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("font-size: 14px; padding: 15px; border-radius: 12px;")
        self.layout.addWidget(self.chat_display)

        # Input Area
        self.input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Xabaringizni yozing...")
        self.input_field.setObjectName("SearchInput")
        self.input_field.setFixedHeight(50)
        self.input_field.returnPressed.connect(self.send_message)
        
        self.send_btn = QPushButton("YUBORISH")
        self.send_btn.setObjectName("PrimaryButton")
        self.send_btn.setFixedHeight(50)
        self.send_btn.setFixedWidth(120)
        self.send_btn.clicked.connect(self.send_message)

        self.input_layout.addWidget(self.input_field)
        self.input_layout.addWidget(self.send_btn)
        self.layout.addLayout(self.input_layout)

    def send_message(self):
        text = self.input_field.text().strip()
        if not text:
            return

        self.chat_display.append(f"<b>Siz:</b> {text}<br>")
        self.input_field.clear()
        self.chat_display.append("<i>AI oylamoqda...</i>")
        
        # In real app, this should be async
        response = self.ai_service.get_response(text)
        
        # Remove "AI oylamoqda..."
        cursor = self.chat_display.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        cursor.select(cursor.SelectionType.LineUnderCursor)
        cursor.removeSelectedText()
        
        self.chat_display.append(f"<b>AI:</b> {response}<br><br>")
        
        # Scroll to bottom
        self.chat_display.verticalScrollBar().setValue(self.chat_display.verticalScrollBar().maximum())
