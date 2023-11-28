import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

class LeaderboardTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        # Setting up the top label
        self.label = QLabel("Добро пожаловать! Ваше место в рейтинге: #1")
        self.label.setStyleSheet("font-weight: bold; color: red; text-align: center; border: 2px solid red;")
        self.label.setFont(QFont("Arial", 38))  # Set the font size to 24
        self.layout.addWidget(self.label)

        # Adding the leader.png to the right of the label
        pixmap = QPixmap("GamePics/leader.png")
        pixmap = pixmap.scaled(480, 300, Qt.KeepAspectRatio)
        leader_image = QLabel()
        leader_image.setPixmap(pixmap)
        leader_image.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(leader_image)


        # Setting up the two boxes
        self.main_layout = QHBoxLayout()
        self.layout.addLayout(self.main_layout)

        self.leaderboard_box = QVBoxLayout()
        self.main_layout.addWidget(self.create_bordered_widget(self.leaderboard_box))

        self.picture_box = QVBoxLayout()
        self.main_layout.addWidget(self.create_bordered_widget(self.picture_box))

        # Setting up the leaderboard label
        self.leaderboard_label = QLabel("Доска почёта")
        self.leaderboard_label.setStyleSheet("font-weight: bold; text-align: center;")
        self.leaderboard_label.setFont(QFont("Arial", 24))  # Set the font size to 20
        self.leaderboard_box.addWidget(self.leaderboard_label)

        # Setting up the player buttons
        self.player_1_button = QPushButton("ИГРОК №1")
        self.player_1_button.setStyleSheet("border-radius: 10px; font-weight: bold; background-color: red;")
        self.player_1_button.clicked.connect(lambda: self.show_picture("playersCSV/p_1.jpg"))
        self.player_1_button.setMinimumHeight(50)
        self.player_1_button.setMinimumWidth(150)
        self.player_1_button.setStyleSheet("text-align: center;")
        self.player_1_button.setFont(QFont("Arial", 10)) 
        self.leaderboard_box.addWidget(self.player_1_button)

        self.player_2_button = QPushButton("ИГРОК №1")
        self.player_2_button.setStyleSheet("border-radius: 10px; font-weight: bold; background-color: red;")
        self.player_2_button.clicked.connect(lambda: self.show_picture("playersCSV/p_2.jpg"))
        self.player_2_button.setMinimumHeight(50)
        self.player_2_button.setMinimumWidth(150)
        self.player_2_button.setStyleSheet("text-align: center;")
        self.player_2_button.setFont(QFont("Arial", 10)) 
        self.leaderboard_box.addWidget(self.player_2_button)

        self.player_3_button = QPushButton("ИГРОК №1")
        self.player_3_button.setStyleSheet("border-radius: 10px; font-weight: bold; min-height: 80px; background-color: red;")
        self.player_3_button.clicked.connect(lambda: self.show_picture("playersCSV/p_3.jpg"))
        self.player_3_button.setMinimumHeight(50)
        self.player_3_button.setMinimumWidth(150)
        self.player_3_button.setStyleSheet("text-align: center;")
        self.player_3_button.setFont(QFont("Arial", 10)) 
        self.leaderboard_box.addWidget(self.player_3_button)

        self.setLayout(self.layout)

    def create_bordered_widget(self, layout):
        widget = QWidget()
        widget.setStyleSheet("border: 2px solid red; border-radius: 10px;")
        widget.setLayout(layout)
        return widget

    def show_picture(self, path):
        # Clearing the picture box layout
        for i in reversed(range(self.picture_box.count())): 
            self.picture_box.itemAt(i).widget().setParent(None)

        # Adding the picture to the picture box
        pixmap = QPixmap(path)
        label = QLabel()
        label.setPixmap(pixmap)
        self.picture_box.addWidget(label)