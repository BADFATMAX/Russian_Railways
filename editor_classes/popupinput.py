from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton


class PopUpInput(QWidget):
    def __init__(self, parent, op):
        super().__init__()
        self.parent = parent
        self.op = op
        self.layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        self.content = None

        self.edit_line = QLineEdit()
        self.edit_line.setMaxLength(15)
        # self.edit_line.setGeometry(300, 300, 280, 170)
        self.edit_line.setPlaceholderText("Enter your text")

        self.send_button = QPushButton("OK")
        self.send_button.clicked.connect(self.send)
        button_layout.addWidget(self.send_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel)
        button_layout.addWidget(self.cancel_button)

        self.layout.addWidget(self.edit_line)
        self.layout.addLayout(button_layout)

        self.setLayout(self.layout)

    def send(self):
        if len(self.edit_line.text()) > 0:
            self.content = self.edit_line.text()
            self.parent.pop_up_input_handle(self)
            self.close()
        else:
            self.edit_line.setText("Enter your text")

    def cancel(self):
        self.op = None
        self.parent.pop_up_input_handle(self)
        self.close()
