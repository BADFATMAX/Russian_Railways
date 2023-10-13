from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QApplication
# from games.CardGame.card_game import main
import subprocess


class GamesTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.pushButton = QPushButton("CardGame")
        self.pushButton2 = QPushButton("SlidingGame")
        self.pushButton.clicked.connect(self.cardgame)
        self.pushButton2.clicked.connect(self.slidinggame)
        self.layout.addWidget(self.pushButton)
        self.layout.addWidget(self.pushButton2)
        self.setLayout(self.layout)

    def cardgame(self):
        ws = QApplication.allWindows()
        for w in ws:
          w.close()
        subprocess.run(['python', 'games/CardGame/card_game.py'])
        for w in ws:
          w.show()

    def slidinggame(self):
        ws = QApplication.allWindows()
        for w in ws:
            w.close()
        subprocess.run(['python', 'games/Picture Sliding Puzzle/game.py'])
        for w in ws:
            w.show()


