from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton

class RhythmGameTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.pushButton = QPushButton("Rhythm game")
        self.layout.addWidget(self.pushButton)
        self.setLayout(self.layout)
