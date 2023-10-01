from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton

class HistoryTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.pushButton = QPushButton("History Tab Button")
        self.layout.addWidget(self.pushButton)
        self.setLayout(self.layout)
