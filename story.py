
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt


class StoryTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        # Add a QLabel for the story text about the train at the top of the window
        storyLabel = QLabel(
            "<font size=40><b>Тууу туу, на ваши плечи легло ответственное задание - переправить уголь из Кузбасса в Камбоджу!</b></font>")
        storyLabels = QLabel(
            "<font size=40><b>Чтож, говорят вы спец.., надеемся для вас не составит труда пройти интересные задания на вашем пути! Удачи!</b></font>")
        storyLabel.setFont(QFont("Arial", 6, QFont.Bold))
        storyLabels.setFont(QFont("Arial", 6, QFont.Bold)
                            )  # Set the font to bold
        self.layout.addWidget(storyLabel)
        self.layout.addWidget(storyLabels)

        # Add a QLabel for the level text at the top of the window
        levelLabel = QLabel("УРОВЕНЬ №1")
        levelLabel.setFont(QFont("Arial", 60, QFont.Bold)) # Set the font to bold and large
        levelLabel.setStyleSheet("color: red;") # Set the text color to red
        levelLabel.setAlignment(Qt.AlignRight) # Align the text to the right
        self.layout.addWidget(levelLabel)

        # Create a QHBoxLayout for the picture and the buttons
        pictureAndButtonsLayout = QHBoxLayout()

        # Add a QLabel for the picture
        pixmap = QPixmap('GamePics/map.png')
        pixmap_bigger = pixmap.scaled(int(pixmap.width() * 1.2), int(pixmap.height() * 1.2))  # Make the picture 1.5 times bigger
        label = QLabel()
        label.setPixmap(pixmap_bigger)
        pictureAndButtonsLayout.addWidget(label)

        # Create a QVBoxLayout for the buttons
        buttonLayout = QVBoxLayout()

        # Create 5 buttons with bold font, round corners, and the specified names
        buttons = []
        button_names = ["КУЗБАСС", "КАМЕРУН", "КУБА", "КОРСИКА", "КАМБОДЖА"]
        for name in button_names:
            button = QPushButton(name)
            button.setFont(QFont("Arial", 14, QFont.Bold))
            button.setStyleSheet("QPushButton { background-color: gray; border-radius: 20px; width: 100px; height: 60px; }")  # Set the buttons to gray, with round corners, shorter width, and taller height
            buttons.append(button)

        # Set the first button to red
        buttons[0].setStyleSheet("QPushButton { background-color: red; border-radius: 20px; width: 100px; height: 60px; }")  # Set the first button to red, with round corners, shorter width, and taller height

        # Connect the button behavior
        for i in range(4):
            buttons[i].clicked.connect(lambda _, next_button=buttons[i+1]: self.enable_next_button(next_button))

        # Add the buttons to the button layout
        for button in buttons:
            buttonLayout.addWidget(button)

        # Add the button layout to the picture and buttons layout
        pictureAndButtonsLayout.addLayout(buttonLayout)

        # Add the picture and buttons layout to the main layout
        self.layout.addLayout(pictureAndButtonsLayout)

        self.setLayout(self.layout)

    # Enable the next button when the current button is clicked
    def enable_next_button(self, next_button):
        next_button.setStyleSheet("QPushButton { background-color: red; border-radius: 20px; width: 50px; height: 60px; }")  # Set the button to red, with round corners, shorter width, and taller height
        next_button.setEnabled(True)