from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QTextBrowser
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

class RewButton(QPushButton):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.parent = parent
        self.active = False
        # self.setStyleSheet("color: black;")
        self.setFont(QFont("Arial", 14, QFont.Bold))
        self.setStyleSheet("""
                        QPushButton { 
                           background-color: gray; border-radius: 20px; width: 100px; height: 60px; 
                        }
                        QPushButton:hover {
                           background-color: #A9A9A9;
                        }""")
    
    def clicked_method(self):
        if self.active:
            self.active = False
            self.setStyleSheet("""
                        QPushButton { 
                           background-color: gray; border-radius: 20px; width: 100px; height: 60px; 
                        }
                        QPushButton:hover {
                           background-color: #A9A9A9;
                        }""")
        else:
            # siblings = self.parent.date_layout.children()
            siblings = [self.parent.date_layout.itemAt(i).widget() for i in range(self.parent.date_layout.count())]
            for sj in siblings:
                print(sj)
                if sj.active == True and sj != self:
                    print("return ", sj)
                    return
            self.active = True
            self.setStyleSheet("""QPushButton { background-color: red; border-radius: 20px; width: 100px; height: 60px; }""")

class AiRewButton(QPushButton):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.parent = parent
        self.setFont(QFont("Arial", 14, QFont.Bold))
        self.setStyleSheet("""QPushButton { 
                                    background-color: red; border-radius: 20px; width: 100px; height: 60px; 
                                }
                                    QPushButton:hover {
                                        background-color: #B22222;
                                    }""")
    def clicked_method(self):
        siblings = [self.parent.ai_layout.itemAt(i).widget() for i in range(self.parent.ai_layout.count())]
        doc = None
        for sj in siblings:
            if isinstance(sj,  QTextBrowser):
                doc = sj
        import random
        def offset():
            if random.random() > 0.5:
                sign = 1
            else:
                sign = 1
            a = (random.random() - 0.1) / 5
            return a * sign
        if self.parent.first_ai_rew:
            self.parent.doc_text.append("<ol>")
            self.parent.doc_text.append(f"<li>{0.7133 + offset():1.5}<li>")
            self.parent.doc_text.append(f"</ol>")
            self.parent.first_ai_rew = False
        else:
            self.parent.doc_text.insert(-1, f"<li>{0.7133 + offset():1.5}</li>")
        doc.setHtml("".join(self.parent.doc_text))



class ReviewTab(QWidget):
    def __init__(self):
        super().__init__()
        self.first_ai_rew = True
        self.doc_text= ["""
<h3>Результаты:</h3>
"""]
        self.layout = QVBoxLayout()
        self.date_layout = QVBoxLayout()
        self.head_layout = QHBoxLayout()

        self.layout.addLayout(self.head_layout)
        self.layout.addLayout(self.date_layout)

        ww = QTextBrowser()
        ww_doc = """
<h3>Программа производит процедуру проверки в два этапа:</h3>
<h3>1) Вашу работу проверяет участник равный вам, его оценка составляет 50 %</h3>
<h3>2) Искусственный интеллект ищет на вашей карте неправильный порядок операций, в его оценка составляет тоже 50%</h3>
"""
        ww.setHtml(ww_doc)

        self.ai_layout = QVBoxLayout()
        ai_button = AiRewButton(self, "Проверка с помощью ИИ")
        ai_button.clicked.connect(ai_button.clicked_method)
        
        ai_res = QTextBrowser()
        ai_res.setStyleSheet("QTextBrowser { background-color: white; }")
        ai_res.setMaximumSize(int(self.width() * 0.8), self.height() // 2)

        ai_res.setHtml(self.doc_text[0])
        self.ai_layout.addWidget(ai_button)
        self.ai_layout.addWidget(ai_res)

        # self.ai_layout.setStyleSheet("border: 1px solid black;")

        self.head_layout.addWidget(ww)
        self.head_layout.addLayout(self.ai_layout)

        # self.date_layout.

        for i in range(12):
            rb = RewButton(self, f"{6+i}:00-{7+i}:00")
            rb.clicked.connect(rb.clicked_method)
            self.date_layout.addWidget(rb)
        
        self.setLayout(self.layout)

    #     # Add a QLabel for the story text about the train at the top of the window
    #     storyLabel = QLabel(
    #         "<font size=40><b>Тууу туу, на ваши плечи легло ответственное задание - переправить уголь из Кузбасса в Камбоджу!</b></font>")
    #     storyLabels = QLabel(
    #         "<font size=40><b>Чтож, говорят вы спец.., надеемся для вас не составит труда пройти интересные задания на вашем пути! Удачи!</b></font>")
    #     storyLabel.setFont(QFont("Arial", 6, QFont.Bold))
    #     storyLabels.setFont(QFont("Arial", 6, QFont.Bold)
    #                         )  # Set the font to bold
    #     self.layout.addWidget(storyLabel)
    #     self.layout.addWidget(storyLabels)

    #     # Add a QLabel for the level text at the top of the window
    #     levelLabel = QLabel("УРОВЕНЬ №1")
    #     levelLabel.setFont(QFont("Arial", 60, QFont.Bold)) # Set the font to bold and large
    #     levelLabel.setStyleSheet("color: red;") # Set the text color to red
    #     levelLabel.setAlignment(Qt.AlignRight) # Align the text to the right
    #     self.layout.addWidget(levelLabel)

    #     # Create a QHBoxLayout for the picture and the buttons
    #     pictureAndButtonsLayout = QHBoxLayout()

    #     # Add a QLabel for the picture
    #     pixmap = QPixmap('GamePics/map.png')
    #     pixmap_bigger = pixmap.scaled(int(pixmap.width() * 1.2), int(pixmap.height() * 1.2))  # Make the picture 1.5 times bigger
    #     label = QLabel()
    #     label.setPixmap(pixmap_bigger)
    #     pictureAndButtonsLayout.addWidget(label)

    #     # Create a QVBoxLayout for the buttons
    #     buttonLayout = QVBoxLayout()

    #     # Create 5 buttons with bold font, round corners, and the specified names
    #     buttons = []
    #     button_names = ["КУЗБАСС", "КАМЕРУН", "КУБА", "КОРСИКА", "КАМБОДЖА"]
    #     for name in button_names:
    #         button = QPushButton(name)
    #         button.setFont(QFont("Arial", 14, QFont.Bold))
    #         button.setStyleSheet("QPushButton { background-color: gray; border-radius: 20px; width: 100px; height: 60px; }")  # Set the buttons to gray, with round corners, shorter width, and taller height
    #         buttons.append(button)

    #     # Set the first button to red
    #     buttons[0].setStyleSheet("QPushButton { background-color: red; border-radius: 20px; width: 100px; height: 60px; }")  # Set the first button to red, with round corners, shorter width, and taller height

    #     # Connect the button behavior
    #     for i in range(4):
    #         buttons[i].clicked.connect(lambda _, next_button=buttons[i+1]: self.enable_next_button(next_button))

    #     # Add the buttons to the button layout
    #     for button in buttons:
    #         buttonLayout.addWidget(button)

    #     # Add the button layout to the picture and buttons layout
    #     pictureAndButtonsLayout.addLayout(buttonLayout)

    #     # Add the picture and buttons layout to the main layout
    #     self.layout.addLayout(pictureAndButtonsLayout)

    #     self.setLayout(self.layout)

    # # Enable the next button when the current button is clicked
    # def enable_next_button(self, next_button):
    #     next_button.setStyleSheet("QPushButton { background-color: red; border-radius: 20px; width: 50px; height: 60px; }")  # Set the button to red, with round corners, shorter width, and taller height
    #     next_button.setEnabled(True)