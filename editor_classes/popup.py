from PyQt5.QtCore import QRect, Qt, QDate, QTime
from PyQt5.QtGui import QPainter, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QMessageBox, QDialog, QLabel, \
    QDialogButtonBox, QFrame, QAbstractSpinBox, QToolButton, QGroupBox, QDateEdit, QTimeEdit
from datetime import time

from .draggable import DraggableLabel
import os
import json

def pushButtonStyle(button: QPushButton):
    button.setStyleSheet("""
                                   QPushButton { 
                                      background-color: snow; border-radius: 10px; min-width: 90px; height: 35px;color:white;
                                      color: dimgray
                                   }
                                   QPushButton:hover {
                                      background-color: Gainsboro;
                                   }""")
    button.setFont(QFont("Arial", 11, QFont.Bold))

def editLineStyle(line: QLineEdit):
    line.setStyleSheet("""
                       QLineEdit { 
                          background-color: snow; border-radius: 10px; width: 90px; height: 35px;color:white;
                          color: dimgray
                       }
                       """)
    line.setFont(QFont("Arial", 11, QFont.Bold))

def labelStyle(label):
    label.setStyleSheet("color: white;")
    label.setFont(QFont("Arial", 11, QFont.Bold))


def deleteItemsOfLayout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                deleteItemsOfLayout(item.layout())


class PopUp(QDialog):
    def __init__(self, parent, op: str):
        super().__init__(parent, Qt.WindowSystemMenuHint | Qt.WindowTitleHint)
        self.parent = parent
        self.op = op
        self.exit_flag = False
        self.layout = None
        self.content = None
        self.setWindowModality(Qt.ApplicationModal)
        self.setStyleSheet("""PopUp 
        {
            background-color: #B22222;
            color: white;
            
        }""")
        self.setFont(QFont("Arial", 11, QFont.Bold))

    def cancel(self):
        self.exit_flag = True
        self.op = None
        self.parent.pop_up_handle(self)
        self.close()

    def closeEvent(self, a0):
        if not self.exit_flag:
            self.cancel()


class PopUpMsg(PopUp):
    def __init__(self, parent, op):
        # super(PopUpInput, self).__init__(parent)
        super().__init__(parent, op)
        self.layout = QVBoxLayout()
        self.setWindowTitle("Сообщение")
        label = QLabel(op)
        labelStyle(label)

        self.layout.addWidget(label)
        ok_button = QPushButton("ОК")
        pushButtonStyle(ok_button)

        ok_button.clicked.connect(self.cancel)

        self.layout.addWidget(ok_button)
        self.setLayout(self.layout)


class PopUpLogin(PopUp):
    def __init__(self, parent, op):
        # super(PopUpInput, self).__init__(parent)
        super().__init__(parent, op)

        self.path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "auth.json")
        self.layout = QVBoxLayout()
        self.allow = False
        self.admin = False
        self.setWindowTitle("Авторизация")

        button_layout = QHBoxLayout()
        send_button = QPushButton("ОК")
        pushButtonStyle(send_button)
        send_button.clicked.connect(self.send)
        button_layout.addWidget(send_button)
        cancel_button = QPushButton("Отмена")
        pushButtonStyle(cancel_button)
        cancel_button.clicked.connect(self.cancel)
        button_layout.addWidget(cancel_button)

        edit_line_login = QLineEdit()
        editLineStyle(edit_line_login)
        edit_line_login.setMaxLength(15)
        edit_line_login.setPlaceholderText("Логин")

        self.edit_login = edit_line_login

        edit_line_password = QLineEdit()
        editLineStyle(edit_line_password)
        edit_line_password.setMaxLength(15)
        edit_line_password.setPlaceholderText("Пароль")
        edit_line_password.setEchoMode(QLineEdit.Password)
        self.edit_password = edit_line_password

        self.layout.addWidget(edit_line_login)
        self.layout.addWidget(edit_line_password)

        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)



    def pop_up_handle(self, obj: PopUp):
        self.children()[-1].setParent(None)
        print("children: ", len(self.children()))
        for child in self.children():
            print(child, " children: ", len(child.children()))

    def hash_pass(self):
        if self.edit_password is None:
            return None
        hs = 5381
        for c in self.edit_password.text():
            hs = ((hs << 5) + hs) + ord(c[0])
        return hs


    def send(self):
        if self.edit_login.text().__len__() <= 0 \
                or self.edit_password.text().__len__() <= 0:
            msg = PopUpMsg(self, "Неверный логин или пароль!")
            msg.show()
        else:
            with open(file=self.path) as fp:
                dat = json.load(fp)
                try:
                    hash_res = dat[self.edit_login.text()]
                except Exception:
                    hash_res = None
                print(self.edit_password.text())
                print(self.hash_pass())
                if hash_res is not None and str(self.hash_pass()) == hash_res:
                    self.allow = True
                    if self.edit_login.text() == "admin":
                        self.admin = True
                    self.close()
                else:
                    msg = PopUpMsg(self, "Неверный логин или пароль!")
                    msg.show()


class PopUpDev(PopUp):
    def __init__(self, parent, op):
        # super(PopUpInput, self).__init__(parent)
        super().__init__(parent, op)

        self.layout = QVBoxLayout()
        self.setWindowTitle("Dev")

        button_layout = QHBoxLayout()

        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.cancel)
        button_layout.addWidget(cancel_button)

        cl1 = QPushButton("__capture()")
        cl1.clicked.connect(self.cl1)
        button_layout.addWidget(cl1)

        cl2 = QPushButton("__makeDataset()")
        cl2.clicked.connect(self.cl2)
        button_layout.addWidget(cl2)

        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)

    def cl1(self):
        self.op = "__capture()"
        self.exit_flag = True
        self.parent.pop_up_handle(self)
        self.close()

    def cl2(self):
        self.op = "__makeDataset()"
        self.exit_flag = True
        self.parent.pop_up_handle(self)
        self.close()



class PopUpInput(PopUp):
    def __init__(self, parent, op):
        # super(PopUpInput, self).__init__(parent)
        super().__init__(parent, op)
        self.layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        self.setWindowTitle("Добавить путь")

        edit_line = QLineEdit()
        edit_line.setMaxLength(15)
        edit_line.setPlaceholderText("Название пути")

        send_button = QPushButton("ОК")
        send_button.clicked.connect(self.send)
        button_layout.addWidget(send_button)
        pushButtonStyle(send_button)

        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.cancel)
        button_layout.addWidget(cancel_button)
        pushButtonStyle(cancel_button)

        self.layout.addWidget(edit_line)
        editLineStyle(edit_line)
        self.layout.addLayout(button_layout)
        self.edit_line = edit_line

        self.setLayout(self.layout)
        # self.resize(self.sizeHint())

    def send(self):
        if len(self.edit_line.text()) > 0:
            self.exit_flag = True
            self.content = {'new name': self.edit_line.text()}
            self.parent.pop_up_handle(self)
            self.close()
        else:
            self.edit_line.setText("Название пути")


class PopUpEditWay(PopUp):
    def __init__(self, parent, op, w_id: int):
        # super(PopUpInput, self).__init__(parent)
        super().__init__(parent, op)

        self.content = {'w_id': w_id}
        self.edit_line = None

        self.layout = QVBoxLayout()
        buttons = QHBoxLayout()
        buttons_ed = QVBoxLayout()
        buttons.addLayout(buttons_ed)

        self.setWindowTitle("Редактировать путь")
        label_edit_way = QLabel("Редактировать путь: " + self.parent.rmap.ways[w_id][0])
        labelStyle(label_edit_way)
        self.layout.addWidget(label_edit_way)

        rename_button = QPushButton("Переименовать")
        rename_button.clicked.connect(self.rename)
        buttons_ed.addWidget(rename_button)
        pushButtonStyle(rename_button)

        move_button = QPushButton("Переместить")
        move_button.clicked.connect(self.move_way)
        pushButtonStyle(move_button)
        buttons_ed.addWidget(move_button)

        del_button = QPushButton("Удалить")
        del_button.clicked.connect(self.delete)
        pushButtonStyle(del_button)
        buttons_ed.addWidget(del_button)

        cancel_button = QPushButton("ОК")
        cancel_button.clicked.connect(self.cancel)
        pushButtonStyle(cancel_button)
        buttons.addWidget(cancel_button)

        self.layout.addLayout(buttons)
        self.setLayout(self.layout)
        self.adjustSize()
        # self.resize(self.sizeHint())

    def delete(self):
        self.exit_flag = True
        self.op = "way_del"
        self.parent.pop_up_handle(self)
        self.close()

    def rename(self):
        if self.layout.count() < 3:
            rename_layout = QVBoxLayout()
            edit_layout = QHBoxLayout()

            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)

            rename_label = QLabel("Переименовать путь")
            labelStyle(rename_label)
            rename_layout.addWidget(rename_label)
            rename_layout.addWidget(line)
            rename_layout.addLayout(edit_layout)

            edit_line = QLineEdit()
            editLineStyle(edit_line)
            edit_line.setMaxLength(15)
            edit_line.setPlaceholderText("Название пути")
            cancel_button = QPushButton("Закрыть")
            pushButtonStyle(cancel_button)
            cancel_button.clicked.connect(self.close_inner)
            send_button = QPushButton("Подтвердить")
            pushButtonStyle(send_button)
            send_button.clicked.connect(self.set_rename)

            edit_layout.addWidget(edit_line)
            edit_layout.addWidget(send_button)
            edit_layout.addWidget(cancel_button)
            self.edit_line = edit_line

            self.layout.addLayout(rename_layout)

    def close_inner(self):
        deleteItemsOfLayout(self.layout.itemAt(2))
        self.layout.removeItem(self.layout.itemAt(2))
        # self.resize(self.sizeHint())

    def set_rename(self):
        if len(self.edit_line.text()) > 0:
            self.op = "way_rename"
            self.content.update({'new name': self.edit_line.text()})
            self.parent.pop_up_temp_handle(self)
            self.layout.removeWidget(self.layout.itemAt(0).widget())
            new_label = QLabel("Редактировать путь: " + self.parent.rmap.ways[self.content['w_id']][0])
            labelStyle(new_label)
            self.layout.insertWidget(0, new_label)
            self.close_inner()
        else:
            self.edit_line.setText("Название пути")

    def move_way(self):
        if self.layout.count() < 3:
            move_layout = QVBoxLayout()

            inner_layout = QHBoxLayout()
            arrows_layout = QVBoxLayout()

            arrow_up = QToolButton()
            arrow_up.setStyleSheet("QToolButton {color: DimGray; background-color: snow;}")
            arrow_down = QToolButton()
            arrow_down.setStyleSheet("QToolButton {color: DimGray; background-color: snow;}")
            arrow_up.setArrowType(Qt.UpArrow)
            arrow_down.setArrowType(Qt.DownArrow)
            arrow_up.clicked.connect(self.move_up)
            arrow_down.clicked.connect(self.move_down)
            arrows_layout.addWidget(arrow_up)
            arrows_layout.addWidget(arrow_down)

            cancel_button = QPushButton("Закрыть")
            pushButtonStyle(cancel_button)
            cancel_button.clicked.connect(self.close_inner)

            inner_layout.addLayout(arrows_layout)
            inner_layout.addWidget(cancel_button)

            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)

            move_way_label = QLabel("Переместить путь")
            labelStyle(move_way_label)
            move_layout.addWidget(move_way_label)
            move_layout.addWidget(line)
            move_layout.addLayout(inner_layout)

            self.layout.addLayout(move_layout)

    def move_up(self):
        self.op = "way_up"
        self.parent.pop_up_temp_handle(self)

    def move_down(self):
        self.op = "way_down"
        self.parent.pop_up_temp_handle(self)


class PopUpInsertElement(PopUp):
    def __init__(self, parent, op, el: DraggableLabel, w_id: int):
        # super(PopUpInput, self).__init__(parent)
        super().__init__(parent, op)

        self.content = {'w_id': w_id, 'element': el}
        self.layout = QVBoxLayout()
        self.setWindowTitle("Поставить элемент")
        self.edit_line = None

        time_edit_layout = QHBoxLayout()
        timeEdit1 = QTimeEdit(QTime.currentTime())
        editLineStyle(timeEdit1)
        timeEdit1.setTimeRange(QTime(self.parent.rmap.start, 0, 0, 0), QTime(self.parent.rmap.end, 0, 0, 0))

        timeEdit2 = QTimeEdit(QTime.currentTime())
        editLineStyle(timeEdit2)
        timeEdit2.setTimeRange(QTime(self.parent.rmap.start, 0, 0, 0), QTime(self.parent.rmap.end, 0, 0, 0))
        self.time_edits = [timeEdit1, timeEdit2]

        time_edit_layout.addWidget(timeEdit1)
        time_edit_layout.addWidget(timeEdit2)

        edit_line = QLineEdit()
        edit_line.setMaxLength(15)
        edit_line.setPlaceholderText("")

        buttons = QHBoxLayout()
        send_button = QPushButton("ОК")
        send_button.clicked.connect(self.insert)
        pushButtonStyle(send_button)
        buttons.addWidget(send_button)

        cancel_button = QPushButton("Отмена")
        pushButtonStyle(cancel_button)
        cancel_button.clicked.connect(self.cancel)
        buttons.addWidget(cancel_button)

        label_main = QLabel(f"Поставить \"{el.text()}\" на \"{self.parent.rmap.ways[w_id][0]}\"")
        labelStyle(label_main)
        self.layout.addWidget(label_main)
        self.layout.addLayout(time_edit_layout)
        self.layout.addLayout(buttons)
        editLineStyle(edit_line)
        self.layout.addWidget(edit_line)
        self.edit_line = edit_line
        self.setLayout(self.layout)
        self.adjustSize()

    def insert(self):
        self.exit_flag = True
        time_s = time(hour=int(self.time_edits[0].time().hour()), minute=int(self.time_edits[0].time().minute()))
        time_e = time(hour=int(self.time_edits[1].time().hour()), minute=int(self.time_edits[1].time().minute()))
        self.content.update({'time_s': time_s, 'time_e': time_e})
        self.parent.pop_up_handle(self)
        self.close()


class PopUpEditElement(PopUp):
    def __init__(self, parent, op, w_id: int, el: dict):
        # super(PopUpInput, self).__init__(parent)
        super().__init__(parent, op)

        self.content = {'w_id': w_id, 'element': el, 'old_element': el.copy()}
        self.layout = QVBoxLayout()
        self.setWindowTitle("Изменить элемент")

        self.edit_line = None

        time_edit_layout = QHBoxLayout()
        cur_time1 = QTime()
        cur_time1.setHMS(el['time_s'].hour, el['time_s'].minute, 0, 0)
        timeEdit1 = QTimeEdit(cur_time1)
        editLineStyle(timeEdit1)
        timeEdit1.setTimeRange(QTime(self.parent.rmap.start, 0, 0, 0), QTime(self.parent.rmap.end, 0, 0, 0))
        timeEdit1.timeChanged.connect(self.edit_time_s)

        cur_time2 = QTime()
        cur_time2.setHMS(el['time_e'].hour, el['time_e'].minute, 0, 0)
        timeEdit2 = QTimeEdit(cur_time2)
        editLineStyle(timeEdit2)
        timeEdit2.setTimeRange(QTime(self.parent.rmap.start, 0, 0, 0), QTime(self.parent.rmap.end, 0, 0, 0))
        # timeEdit2.editingFinished.connect(self.edit_time_e)
        timeEdit2.timeChanged.connect(self.edit_time_e)
        self.time_edits = [timeEdit1, timeEdit2]

        time_edit_layout.addWidget(timeEdit1)
        time_edit_layout.addWidget(timeEdit2)

        edit_line = QLineEdit()
        editLineStyle(edit_line)
        edit_line.setMaxLength(15)
        edit_line.setText(el['text'])
        edit_line.textChanged.connect(self.changed_text)

        buttons = QHBoxLayout()
        send_button = QPushButton("ОК")
        pushButtonStyle(send_button)
        send_button.clicked.connect(self.cancel)
        buttons.addWidget(send_button)

        del_button = QPushButton("Удалить")
        pushButtonStyle(del_button)
        del_button.clicked.connect(self.delete)
        buttons.addWidget(del_button)

        cancel_button = QPushButton("Отмена")
        pushButtonStyle(cancel_button)
        cancel_button.clicked.connect(self.restore)
        buttons.addWidget(cancel_button)

        label_widg = QLabel(
            f"Изменить \"{el['name']}({el['time_s'].strftime('%H:%M')}-{el['time_e'].strftime('%H:%M')})\" на \"{self.parent.rmap.ways[w_id][0]}\"")
        labelStyle(label_widg)
        self.layout.addWidget(label_widg)
        self.layout.addLayout(time_edit_layout)
        self.layout.addLayout(buttons)
        self.edit_line = edit_line
        self.layout.addWidget(edit_line)
        self.setLayout(self.layout)
        self.adjustSize()

    def edit_time_s(self):
        self.content['element']['time_s'] = time(hour=self.time_edits[0].time().hour(),
                                                 minute=self.time_edits[0].time().minute())
        self.parent.draw_map()

    def edit_time_e(self):
        self.content['element']['time_e'] = time(hour=self.time_edits[1].time().hour(),
                                                 minute=self.time_edits[1].time().minute())
        self.parent.draw_map()

    def changed_text(self):
        self.content['element']['text'] = self.edit_line.text()
        self.parent.draw_map()

    def restore(self):
        self.content['element'].clear()
        self.content['element'].update(self.content['old_element'])
        self.parent.draw_map()
        self.cancel()

    def delete(self):
        way_index = self.content['w_id']
        (self.parent.rmap.elements[way_index]).remove(self.content['element'])
        if len(self.parent.rmap.elements[way_index]) < 1:
            del self.parent.rmap.elements[way_index]
        self.parent.draw_map()
        self.cancel()
