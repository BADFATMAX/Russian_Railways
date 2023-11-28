import os

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QApplication, QLabel
from PyQt5.QtGui import QPixmap
# from games.CardGame.card_game import main
import subprocess
import sys


class GamesTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.pushButton = QPushButton("CardGame")
        self.pushButton2 = QPushButton("SlidingGame")
        self.pushButton3 = QPushButton("PianoGame")

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
            }
            QPushButton:hover {
                background-color: #B22222;
            }
            """

        self.pushButton.setStyleSheet(button_style)
        self.pushButton2.setStyleSheet(button_style)
        self.pushButton3.setStyleSheet(button_style)

        self.pushButton.clicked.connect(self.cardgame)
        self.pushButton2.clicked.connect(self.slidinggame)
        self.pushButton3.clicked.connect(self.pianogame)
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
            pixmap = QPixmap(f'GamePics/game{i}.png')
            label = QLabel()
            label.setPixmap(pixmap)
            label.mousePressEvent = lambda event, game=i: self.on_picture_click(game)
            self.pictureLayout.addWidget(label)
        
        # Add pictures to the main layout
        self.layout.addLayout(self.pictureLayout)

    def on_picture_click(self, game):
        if game == 1:
            self.cardgame()
        elif game == 2:
            self.slidinggame()
        elif game == 3:
            self.pianogame()

    def cardgame(self):
        ws = QApplication.allWindows()
        for w in ws:
          w.close()
        subprocess.run([f'{sys.executable}', 'games/CardGame/card_game.py'])
        for w in ws:
          w.show()

    def slidinggame(self):
        ws = QApplication.allWindows()
        for w in ws:
            w.close()
        subprocess.run([f'{sys.executable}', 'games/Picture Sliding Puzzle/game.py'])
        for w in ws:
            w.show()

    def pianogame(self):
        ws = QApplication.allWindows()
        for w in ws:
            w.close()
        subprocess.run(f"{sys.executable} games/PianoGame/main.py")
        for w in ws:
            w.show()

    def game1(self):
        self.cardgame()

    def game2(self):
        self.slidinggame()

    def game3(self):
        self.pianogame()