import os

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QApplication, QLabel
from PyQt5.QtGui import QPixmap
# from games.CardGame.card_game import main
import subprocess
import sys


class CommonTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.layout = QVBoxLayout()
        self.pushButton = QPushButton("РАБОТА ТОВАРИЩА")
        self.pushButton2 = QPushButton("МОЯ РАБОТА")
        self.pushButton3 = QPushButton("ОБЪЕДИНЕНИЕ")

        button_style = """
            QPushButton {
                background-color: red;
                border-style: outset;
                border-width: 2px;
                border-radius: 20px;
                border-color: beige;
                font-weight: bold;
                font-size: 22px;
                min-width: 100px;
                min-height: 50px;
                color: white;
            }
            QPushButton:hover {
                background-color: #B22222;
            }
            """

        self.pushButton.setStyleSheet(button_style)
        self.pushButton2.setStyleSheet(button_style)
        self.pushButton3.setStyleSheet(button_style)

        self.pushButton.clicked.connect(self.comrade)
        self.pushButton2.clicked.connect(self.mine)
        self.pushButton3.clicked.connect(self.unite)
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.pushButton)
        buttonLayout.addWidget(self.pushButton2)
        buttonLayout.addWidget(self.pushButton3)
        self.layout.addLayout(buttonLayout)
        self.setLayout(self.layout)
        self.setStyleSheet("background-color: white;")

        # Add pictures below the buttons
        self.pictureLayout = QHBoxLayout()
        for i in range(1, 4):
            pixmap = QPixmap(f'GamePics/work{i}.jpg')
            label = QLabel()
            label.setPixmap(pixmap)
            label.mousePressEvent = lambda event, mode=i: self.on_picture_click(mode)
            self.pictureLayout.addWidget(label)
        
        # Add pictures to the main layout
        self.layout.addLayout(self.pictureLayout)

    def on_picture_click(self, mode):
        if mode == 1:
            self.comrade()
        elif mode == 2:
            self.mine()
        elif mode == 3:
            self.unite()

    def comrade(self):
        self.parent.tab_widget.setCurrentIndex(0)
        self.parent.editor_tab.open_other()

    def mine(self):
        self.parent.tab_widget.setCurrentIndex(0)
        self.parent.editor_tab.open_mine()

    def unite(self):
        self.parent.tab_widget.setCurrentIndex(0)
        self.parent.editor_tab.do_union()