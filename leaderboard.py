import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap

class LeaderboardTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Create a QLabel to display the image
        image_label = QLabel()
        pixmap = QPixmap("image.png")
        image_label.setPixmap(pixmap)

        # Add the QLabel to the layout
        layout.addWidget(image_label)

        self.setLayout(layout)