from PyQt5.QtCore import QRect, Qt, QDate, QTime
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QMessageBox, QDialog, QLabel, \
    QDialogButtonBox, QFrame, QAbstractSpinBox, QToolButton, QGroupBox, QDateEdit, QTimeEdit
from datetime import time

from .draggable import DraggableLabel


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

        self.setWindowTitle("Добавить путь")

        edit_line = QLineEdit()
        edit_line.setMaxLength(15)
        edit_line.setPlaceholderText("Название пути")

        send_button = QPushButton("ОК")
        send_button.clicked.connect(self.send)
        button_layout.addWidget(send_button)

        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.cancel)
        button_layout.addWidget(cancel_button)

        self.layout.addWidget(edit_line)
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
        self.layout.addWidget(QLabel("Редактировать путь: " + self.parent.rmap.ways[w_id][0]))

        rename_button = QPushButton("Переименовать")
        rename_button.clicked.connect(self.rename)
        buttons_ed.addWidget(rename_button)

        move_button = QPushButton("Переместить")
        move_button.clicked.connect(self.move_way)
        buttons_ed.addWidget(move_button)

        del_button = QPushButton("Удалить")
        del_button.clicked.connect(self.delete)
        buttons_ed.addWidget(del_button)

        cancel_button = QPushButton("ОК")
        cancel_button.clicked.connect(self.cancel)
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

            rename_layout.addWidget(QLabel("Переименовать путь"))
            rename_layout.addWidget(line)
            rename_layout.addLayout(edit_layout)

            edit_line = QLineEdit()
            edit_line.setMaxLength(15)
            edit_line.setPlaceholderText("Название пути")
            cancel_button = QPushButton("Закрыть")
            cancel_button.clicked.connect(self.close_inner)
            send_button = QPushButton("Подтвердить")
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
            self.layout.insertWidget(0, QLabel("Редактировать путь: " + self.parent.rmap.ways[self.content['w_id']][0]))
            self.close_inner()
        else:
            self.edit_line.setText("Название пути")

    def move_way(self):
        if self.layout.count() < 3:
            move_layout = QVBoxLayout()

            inner_layout = QHBoxLayout()
            arrows_layout = QVBoxLayout()

            arrow_up = QToolButton()
            arrow_down = QToolButton()
            arrow_up.setArrowType(Qt.UpArrow)
            arrow_down.setArrowType(Qt.DownArrow)
            arrow_up.clicked.connect(self.move_up)
            arrow_down.clicked.connect(self.move_down)
            arrows_layout.addWidget(arrow_up)
            arrows_layout.addWidget(arrow_down)

            cancel_button = QPushButton("Закрыть")
            cancel_button.clicked.connect(self.close_inner)

            inner_layout.addLayout(arrows_layout)
            inner_layout.addWidget(cancel_button)

            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)

            move_layout.addWidget(QLabel("Переместить путь"))
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

        time_edit_layout = QHBoxLayout()
        timeEdit1 = QTimeEdit(QTime.currentTime())
        timeEdit1.setTimeRange(QTime(self.parent.rmap.start, 0, 0, 0), QTime(self.parent.rmap.end, 0, 0, 0))

        timeEdit2 = QTimeEdit(QTime.currentTime())
        timeEdit2.setTimeRange(QTime(self.parent.rmap.start, 0, 0, 0), QTime(self.parent.rmap.end, 0, 0, 0))
        self.time_edits = [timeEdit1, timeEdit2]

        time_edit_layout.addWidget(timeEdit1)
        time_edit_layout.addWidget(timeEdit2)

        buttons = QHBoxLayout()
        send_button = QPushButton("ОК")
        send_button.clicked.connect(self.insert)
        buttons.addWidget(send_button)

        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.cancel)
        buttons.addWidget(cancel_button)

        self.layout.addWidget(QLabel(f"Поставить \"{el.text()}\" на \"{self.parent.rmap.ways[w_id][0]}\""))
        self.layout.addLayout(time_edit_layout)
        self.layout.addLayout(buttons)
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
    def __init__(self, parent, op, w_id:int, el:dict):
        # super(PopUpInput, self).__init__(parent)
        super().__init__(parent, op)

        self.content = {'w_id': w_id, 'element': el, 'old_element': el.copy()}
        self.layout = QVBoxLayout()
        self.setWindowTitle("Изменить элемент")

        time_edit_layout = QHBoxLayout()
        cur_time1 = QTime()
        cur_time1.setHMS(el['time_s'].hour, el['time_s'].minute, 0, 0)
        timeEdit1 = QTimeEdit(cur_time1)
        timeEdit1.setTimeRange(QTime(self.parent.rmap.start, 0, 0, 0), QTime(self.parent.rmap.end, 0, 0, 0))
        timeEdit1.timeChanged.connect(self.edit_time_s)

        cur_time2 = QTime()
        cur_time2.setHMS(el['time_e'].hour, el['time_e'].minute, 0, 0)
        timeEdit2 = QTimeEdit(cur_time2)
        timeEdit2.setTimeRange(QTime(self.parent.rmap.start, 0, 0, 0), QTime(self.parent.rmap.end, 0, 0, 0))
        # timeEdit2.editingFinished.connect(self.edit_time_e)
        timeEdit2.timeChanged.connect(self.edit_time_e)
        self.time_edits = [timeEdit1, timeEdit2]

        time_edit_layout.addWidget(timeEdit1)
        time_edit_layout.addWidget(timeEdit2)

        buttons = QHBoxLayout()
        send_button = QPushButton("ОК")
        send_button.clicked.connect(self.cancel)
        buttons.addWidget(send_button)

        del_button = QPushButton("Удалить")
        del_button.clicked.connect(self.delete)
        buttons.addWidget(del_button)

        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.restore)
        buttons.addWidget(cancel_button)

        self.layout.addWidget(QLabel(f"Изменить \"{el['name']}({el['time_s'].strftime('%H:%M')}-{el['time_e'].strftime('%H:%M')})\" на \"{self.parent.rmap.ways[w_id][0]}\""))
        self.layout.addLayout(time_edit_layout)
        self.layout.addLayout(buttons)
        self.setLayout(self.layout)
        self.adjustSize()

    def edit_time_s(self):
        self.content['element']['time_s'] = time(hour=self.time_edits[0].time().hour(), minute=self.time_edits[0].time().minute())
        self.parent.draw_map()

    def edit_time_e(self):
        self.content['element']['time_e'] = time(hour=self.time_edits[1].time().hour(), minute=self.time_edits[1].time().minute())
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
