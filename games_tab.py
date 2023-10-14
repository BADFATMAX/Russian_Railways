import os

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QApplication
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
        self.pushButton.clicked.connect(self.cardgame)
        self.pushButton2.clicked.connect(self.slidinggame)
        self.pushButton3.clicked.connect(self.pianogame)
        self.layout.addWidget(self.pushButton)
        self.layout.addWidget(self.pushButton2)
        self.layout.addWidget(self.pushButton3)
        self.setLayout(self.layout)

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
        # subprocess.run(['python', 'games/PianoGame/main.py'])
        for w in ws:
            w.show()


