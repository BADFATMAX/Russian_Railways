from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton


class PopUp(QWidget):
    def __init__(self, parent, op):
        super().__init__()
        self.parent = parent
        self.op = op
        self.exit_flag = False
        self.layout = None
        self.content = None

    def cancel(self):
        self.exit_flag = True
        self.op = None
        self.parent.pop_up_handle(self)
        self.close()

    def closeEvent(self, a0):
        if not self.exit_flag:
            self.cancel()


class PopUpInput(PopUp):
    def __init__(self, parent, op):
        # super(PopUpInput, self).__init__(parent)
        super().__init__(parent, op)

        self.layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        edit_line = QLineEdit()
        edit_line.setMaxLength(15)
        # self.edit_line.setGeometry(300, 300, 280, 170)
        edit_line.setPlaceholderText("Enter your text")

        send_button = QPushButton("OK")
        send_button.clicked.connect(self.send)
        button_layout.addWidget(send_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.cancel)
        button_layout.addWidget(cancel_button)

        self.layout.addWidget(edit_line)
        self.layout.addLayout(button_layout)
        self.edit_line = edit_line

        self.setLayout(self.layout)

    def send(self):
        if len(self.edit_line.text()) > 0:
            self.exit_flag = True
            self.content = self.edit_line.text()
            self.parent.pop_up_handle(self)
            self.close()
        else:
            self.edit_line.setText("Enter your text")


class PopUpEditWay(PopUp):
    def __init__(self, parent, op, way):
        # super(PopUpInput, self).__init__(parent)
        super().__init__(parent, op)

        self.content = way

        self.layout = QHBoxLayout()
        send_button = QPushButton("Delete")
        send_button.clicked.connect(self.delete)
        self.layout.addWidget(send_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.cancel)
        self.layout.addWidget(cancel_button)
        self.setLayout(self.layout)

    def delete(self):
        self.exit_flag = True
        self.parent.pop_up_handle(self)
        self.close()
