from datetime import datetime, time as dt_time

from PyQt5 import QtSvg, QtGui
from PyQt5.QtCore import QPointF, QPoint, QSize, QRect, QRectF
from PyQt5.QtCore import QPointF
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag, QPixmap, QPainter, QPolygonF, QPen, QBrush, QWheelEvent, QFont, QImage
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGraphicsScene, QGraphicsView, \
    QFileDialog, QGridLayout, QFrame, QApplication, QScrollArea

from editor_classes.draggable import DraggableLabel
from editor_classes.editorscene import EditorScene
from editor_classes.popup import PopUpInput, PopUp, PopUpEditWay, deleteItemsOfLayout, PopUpInsertElement, \
    pushButtonStyle, \
    PopUpEditElement, PopUpMsg, PopUpDev
from map_class import RailMap
import math

from functools import reduce
import os


class EditorView(QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def wheelEvent(self, event: QWheelEvent):
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ControlModifier:
            sign = 1 if event.angleDelta().y() > 0 else -1
            hsb = self.horizontalScrollBar()
            print(hsb.maximum())
            hsb.setValue(hsb.value() + sign * hsb.maximum() // 16)
        elif modifiers == Qt.ShiftModifier:
            sign = -1 if event.angleDelta().y() > 0 else 1
            vsb = self.verticalScrollBar()
            vsb.setValue(vsb.value() + sign * vsb.maximum() // 12)
        elif event.angleDelta().y() > 0:
            self.scale(1.6, 1.6)
        else:
            self.scale(0.625, 0.625)

    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.parent().parent.admin:
            msg = PopUpDev(self, "dev")
            msg.show()
        else:
            pass

    def pop_up_handle(self, obj: PopUp):
        if obj.op == "__capture()":
            self.__capture()
        elif obj.op == "__makeDataset()":
            self.__makeDataset()
        self.children()[-1].setParent(None)
        print("children: ", len(self.children()))
        for child in self.children():
            print(child, " children: ", len(child.children()))

    def __makeDataset(self):
        with open(os.path.join("elements", "elements.json")) as fptr:
            import json
            data: dict = json.load(fptr)
            labels = list(data.keys())
        fp = os.path.join(os.path.dirname(__file__), "maps", "data1.xml")
        filedata = None
        with open(fp, 'r') as file:
            filedata = file.read()
            file.close()
        fp = os.path.join(os.path.dirname(__file__), "maps", "data1tmp.xml")
        for label in labels:
            filedata_one = filedata.replace("el1", label)
            for label_p in labels:
                filedata_two = filedata_one.replace("el2", label_p)
                with open(fp, 'w') as file:
                    file.write(filedata_two)
                    file.close()
                self.parent().rmap = RailMap(fp)
                self.parent().rmap.set_visible(True)
                self.parent().draw_map()
                self.__capture(f".{label}.{label_p}.", "captures_dataset", False)

    def __capture(self, infix="", root_dir="captures", date=True):
        if not os.path.exists(root_dir):
            os.mkdir(root_dir)
        if date:
            infix+=datetime.now().strftime("%d_%m_%y_%H_%M_%S")
        folder = os.path.join(root_dir, "captures" + infix)
        os.mkdir(folder)
        map: RailMap = self.parent().rmap
        x = 180
        xhalf = x // 2
        y = 50
        x0 = 50
        y0 = 50
        w_s_y = y0
        w_s_x = x0 + x

        hours = [[dt_time(h), dt_time(h, 30)] for h in list(range(map.start, map.end))]
        hours = [jj for ii in hours for jj in ii]
        for idx, way in enumerate(map.ways):
            for hour in hours:
                try:
                    if hour.minute == 0:
                        hour_e = dt_time(hour.hour, 30)
                    else:
                        hour_e = dt_time(hour.hour + 1, 0)
                    elems = map.elements[idx]
                    flags = [el['time_e'].time() > hour and el['time_s'].time() < hour_e for el in elems]
                    if True in flags:
                        area = QRect(w_s_x, w_s_y, xhalf, y)
                        pixmap = QtGui.QPixmap(90 * 3, 50 * 3)
                        pixmap.fill(QtGui.QColor("white"))

                        painter = QPainter(pixmap)
                        self.parent().scene.render(painter, QRectF(pixmap.rect()), QRectF(area))
                        painter.end()

                        image = pixmap.toImage()
                        image.save(os.path.join(folder, f"{idx}_{way[0]}_{hour.strftime('%H_%M')}" + ".png"))
                except Exception:
                    pass
                w_s_x += xhalf
            w_s_y += y
            w_s_x = x0 + x


class DashPen(QPen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        space = 5
        dashes = [2, space]
        self.setDashPattern(dashes)


class EditorTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.parent = parent
        self.layout = QVBoxLayout()
        self.button_layout = QHBoxLayout()
        self.popUps = []
        self.rmap = RailMap()

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
           min-height: 40px;
           color:white;
       }
       QPushButton:hover {
        background-color: #B22222;
       }
       """

        save_map_button = QPushButton("Сохранить")
        save_map_button.setStyleSheet(button_style)
        save_map_button.clicked.connect(self.save_map)

        load_map_button = QPushButton("Загрузить")
        load_map_button.setStyleSheet(button_style)
        load_map_button.clicked.connect(self.load_map)

        new_map_button = QPushButton("Новый файл")
        new_map_button.setStyleSheet(button_style)
        new_map_button.clicked.connect(self.new_map)

        add_row_button = QPushButton("Добавить путь")
        add_row_button.setStyleSheet(button_style)
        add_row_button.clicked.connect(self.add_row)

        remove_row_button = QPushButton("Убрать путь")
        remove_row_button.setStyleSheet(button_style)
        remove_row_button.clicked.connect(self.remove_row)

        # save_map_button = QPushButton("Сохранить")
        # save_map_button.clicked.connect(self.save_map)
        # load_map_button = QPushButton("Загрузить")
        # load_map_button.clicked.connect(self.load_map)
        # new_map_button = QPushButton("Новый файл")
        # new_map_button.clicked.connect(self.new_map)
        # add_row_button = QPushButton("Добавить путь")
        # add_row_button.clicked.connect(self.add_row)
        # remove_row_button = QPushButton("Remove Row")
        # remove_row_button.clicked.connect(self.remove_row)

        self.button_layout.addWidget(save_map_button)
        self.button_layout.addWidget(load_map_button)
        self.button_layout.addWidget(new_map_button)
        self.button_layout.addWidget(add_row_button)
        self.button_layout.addWidget(remove_row_button)

        self.layout.addLayout(self.button_layout)

        self.scene = EditorScene(self, 0, 0, 4000, 1080)

        self.view = EditorView(self.scene, parent=self)
        self.view.setAcceptDrops(True)
        self.view.setRenderHint(QPainter.Antialiasing)
        # self.view.scale(2, 2)

        self.layout.addWidget(self.view)

        layout_bottom = QHBoxLayout()
        # layout_bottom.setSpacing(1000)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget(scroll)
        scroll.setFixedWidth(600)
        scroll.setFixedHeight(300)
        # scroll_content.setFixedHeight(200)
        # scroll_content.setFixedWidth(600)
        # left.setFixedWidth(600)
        # left.setFixedHeight(200)
        scroll_content.setStyleSheet("border: 1px solid black;")
        # layout_left = QGridLayout()
        # scroll_content.setLayout(layout_left)
        scrollLayout = QGridLayout(scroll_content)
        scroll_content.setLayout(scrollLayout)
        scrollLayout.setSpacing(2)

        layout_bottom.addWidget(scroll, Qt.AlignLeft)

        layout_right = QVBoxLayout()

        layout_bottom.addLayout(layout_right, Qt.AlignLeft)
        layout_bottom.addStretch()

        self.info_layout = layout_right
        self.bottom_layout = layout_bottom

        self.elements = []
        for i, el_in_panel in enumerate(self.rmap.el_config):
            element = DraggableLabel(self)
            element.text_ = self.rmap.el_config[el_in_panel]['name']
            element.uri_ = el_in_panel
            element.align_ = self.rmap.el_config[el_in_panel]['align']
            # element.setFixedSize(100, 67)
            pixmap = QPixmap(self.rmap.el_config[el_in_panel]['svg_label'])
            # pixmap = pixmap.scaled(100, 67)
            element.setPixmap(pixmap)
            self.elements.append(element)
            scrollLayout.addWidget(element, i // 3, i % 3, Qt.AlignLeft)
            # scrollLayout.addWidget(element)

        self.layout.addLayout(layout_bottom)
        scroll.setWidget(scroll_content)
        self.setLayout(self.layout)

    def open_other(self):
        fp = os.path.join(os.path.dirname(__file__), "maps", "other.xml")
        if not os.path.exists(fp):
            msg = PopUpMsg(self, op="Работа товарища не найдена!")
            msg.show()
        else:
            self.rmap = RailMap(fp)
            self.rmap.set_visible(True)
            self.draw_map()

    def open_mine(self):
        fp = os.path.join(os.path.dirname(__file__), "maps", "mine.xml")
        if not os.path.exists(fp):
            msg = PopUpMsg(self, op="Ваша работа не найдена!")
            msg.show()
        else:
            self.rmap = RailMap(fp)
            self.rmap.set_visible(True)
            self.draw_map()

    def do_union(self):
        fp1 = os.path.join(os.path.dirname(__file__), "maps", "other.xml")
        fp2 = os.path.join(os.path.dirname(__file__), "maps", "mine.xml")
        if not os.path.exists(fp1):
            msg = PopUpMsg(self, op="Работа товарища не найдена!")
            msg.show()
        elif not os.path.exists(fp2):
            msg = PopUpMsg(self, op="Ваша работа не найдена!")
            msg.show()
        else:
            self.rmap = RailMap(fp1)
            rmap_append = RailMap(fp2)
            self.rmap.unite(rmap_append)
            self.rmap.set_visible(True)
            self.draw_map()

    def story_load(self):
        fp = os.path.join(os.path.dirname(__file__), "maps", "level1.xml")
        self.rmap = RailMap(fp)
        self.rmap.set_visible(True)
        self.draw_map()
        label = QLabel("""
Вы управляющий на горной кузбасской станции.
Из-за снежной бури ,ночью , один из ваших железнодорожных путей засыпало снегом (1ый путь).
Машины не справляются с его уборкой, мало мощности.
НО, работа продолжается. На вашей станции должен остановиться гружёный углём локомотив в 15:15.
Подготовьте путь к его прибытию!
""")
        label.setStyleSheet(
            "QLabel { background-color:snow; min-width: 400px; border-radius: 20px; border-style: solid; border-color:red; border-width: 4px; color: dimgray} ")
        # label.setStyleSheet("color: dimgray;")
        label.setFont(QFont("Arial", 11, QFont.Bold))

        buttons_layout = QVBoxLayout()
        button_send = QPushButton("Отправить")
        # pushButtonStyle(button_send)
        # buttons_layout.addWidget(button_send)

        # self.button_layout.addLayout(buttons_layout)
        self.bottom_layout.addWidget(label)
        # self.bottom_layout.addWidget(button_send)

    def save_map(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)
            self.rmap.save(fileName)

    def load_map(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)
            self.rmap = RailMap(fileName)
            self.rmap.set_visible(True)
            self.draw_map()

    def new_map(self):
        self.rmap = RailMap()
        self.rmap.set_visible(True)
        self.draw_map()

    def edit_row(self, w_id: int):
        msg = PopUpEditWay(self, "edit_row", w_id)
        msg.show()
        self.popUps.append(msg)
        print(self.rmap.elements.keys())

    def add_row(self):
        if self.rmap.visible:  # and (len(self.popUps) == 0 or not isinstance(self.popUps[-1], PopUp)):
            msg = PopUpInput(self, "add_row")
            msg.show()
            self.popUps.append(msg)
            print(self.rmap.elements.keys())

    def remove_row(self):
        if self.rmap.visible:
            if len(self.rmap.ways) > 0:
                # index = self.rmap.ways.index(self.rmap.ways[-1])
                # print(index)
                try:
                    self.rmap.elements.pop(-1)
                except KeyError:
                    pass
                self.rmap.ways.pop()
                self.draw_map()
                print(self.rmap.elements.keys())

    def pop_up_handle(self, popUpObj: PopUp):
        if popUpObj.op == "add_row":
            self.rmap.ways.append([popUpObj.content['new name'], 1])
        elif popUpObj.op == "way_del":
            index = popUpObj.content['w_id']
            try:
                self.rmap.elements.pop(index)
            except KeyError:
                pass
            keys = sorted(self.rmap.elements.keys())
            for key in keys:
                if key > index:
                    el = self.rmap.elements.pop(key)
                    self.rmap.elements.update({key - 1: el})
            del self.rmap.ways[popUpObj.content['w_id']]
        elif popUpObj.op == "element_insert":
            new_el = {'uri': popUpObj.content['element'].uri_, 'name': popUpObj.content['element'].text(),
                      'time_s': popUpObj.content['time_s'],
                      'time_e': popUpObj.content['time_e'],
                      'align': popUpObj.content['element'].align_,
                      'text': popUpObj.edit_line.text()}
            i = popUpObj.content['w_id']
            try:
                way_list = self.rmap.elements[i]
                way_list.append(new_el)
            except KeyError:
                self.rmap.elements.update({i: [new_el]})
        try:
            self.popUps.remove(popUpObj)
        except ValueError:
            print("No such popup in list!")
        # print(self.layout.count())
        self.children()[-1].setParent(None)
        print("children: ", len(self.children()))
        for child in self.children():
            print(child, " children: ", len(child.children()))
        self.draw_map()

    def pop_up_temp_handle(self, popUpObj: PopUp):
        def exchange_el(iself, iother):
            try:
                fromself = self.rmap.elements[iself]
                try:
                    other = self.rmap.elements[iother]
                    self.rmap.elements.update({iother: fromself, iself: other})
                except KeyError:
                    self.rmap.elements.update({iother: fromself})
                    self.rmap.elements.pop(iself)
            except KeyError:
                try:
                    other = self.rmap.elements[iother]
                    self.rmap.elements.update({iself: other})
                    self.rmap.elements.pop(iother)
                except KeyError:
                    pass

        if popUpObj.op == "way_rename":
            i = popUpObj.content['w_id']
            self.rmap.ways[i][0] = popUpObj.content['new name']
        elif popUpObj.op == "way_up":
            idx = popUpObj.content['w_id']
            if idx > 0:
                tmp = self.rmap.ways[idx]
                self.rmap.ways[idx] = self.rmap.ways[idx - 1]
                self.rmap.ways[idx - 1] = tmp
                exchange_el(idx, idx - 1)
                popUpObj.content['w_id'] -= 1
        elif popUpObj.op == "way_down":
            idx = popUpObj.content['w_id']
            if idx < (len(self.rmap.ways) - 1):
                tmp = self.rmap.ways[idx]
                self.rmap.ways[idx] = self.rmap.ways[idx + 1]
                self.rmap.ways[idx + 1] = tmp
                exchange_el(idx, idx + 1)
                popUpObj.content['w_id'] += 1
        self.draw_map()

    def draw_map(self):
        if self.rmap.visible:
            self.scene.clear()
            print("popups: ", self.popUps)
            x = 180
            y = 50
            x0 = 50
            y0 = 50
            w_s_y = y0
            hours = self.rmap.end - self.rmap.start + 1
            # рендерит прямоугольники (пути)
            for w_id, way in enumerate(self.rmap.ways):
                height = way[1]
                name = way[0]
                self.scene.addPolygon(
                    QPolygonF(
                        [
                            QPointF(x0, w_s_y),
                            QPointF(x0 + hours * x, w_s_y),
                            QPointF(x0 + hours * x, w_s_y + y * height),
                            QPointF(x0, w_s_y + y * height),
                        ]),
                )
                # имя пути
                textitem = self.scene.addText(name)
                textitem.setPos(x0 + 3, w_s_y + height // 2)
                try:
                    elements = self.rmap.elements[w_id]
                    for el in elements:
                        # сделать функционал для отрисовки элементов, разных
                        x_s_el = x0 + x * (el['time_s'].hour - self.rmap.start + 1) + (x // 60) * el['time_s'].minute
                        x_e_el = x0 + x * (el['time_e'].hour - self.rmap.start + 1) + (x // 60) * el['time_e'].minute
                        svgWidget = QtSvg.QSvgWidget(self.rmap.el_config[el["uri"]]["svg_main"])
                        # print(self.rmap.el_config[el["uri"]]["svg_main"])
                        additional = (height * y) // 4
                        svgWidget.setGeometry(x_s_el, w_s_y + additional, x_e_el - x_s_el,
                                              (y * height) - 2 * additional)
                        # renderer = QtSvg.QSvgRenderer('elements\\anchoring.svg')
                        self.scene.addWidget(svgWidget)
                        textitem = self.scene.addText(el['text'])
                        text_y = w_s_y + y // 2 - textitem.boundingRect().height() // 2
                        if (el['align'] == 'center'):
                            text_x = x_s_el + (x_e_el - x_s_el) // 2 - textitem.boundingRect().width() // 2
                        elif (el['align'] == 'right'):
                            text_x = x_e_el
                        elif (el['align'] == 'left'):
                            text_x = x_s_el - textitem.boundingRect().width()
                        elif (el['align'] == 'right45'):
                            try:
                                angle = math.atan(((y * height) - 2 * additional) / (x_e_el - x_s_el))
                                textitem.setRotation(math.degrees(angle))
                                text_x = x_s_el + (x_e_el - x_s_el) // 2 - (
                                            textitem.boundingRect().width() // 2) * math.cos(angle) + (
                                                     textitem.boundingRect().height() * 0.7)
                                text_y = w_s_y + (y // 2) - (textitem.boundingRect().width() // 2) * math.sin(
                                    angle) - textitem.boundingRect().height() * 0.7
                            except Exception:
                                text_x = x_s_el
                        else:
                            text_x = x_s_el
                        textitem.setPos(text_x, text_y)
                        map_len = sum([need_integ[1] for need_integ in self.rmap.ways])
                        self.scene.addPolygon(
                            QPolygonF(
                                [
                                    QPointF(x_s_el, y0),
                                    QPointF(x_s_el, y0 + map_len * y),
                                ]), DashPen(Qt.darkGray, 1)
                        )
                        self.scene.addPolygon(
                            QPolygonF(
                                [
                                    QPointF(x_e_el, y0),
                                    QPointF(x_e_el, y0 + map_len * y),
                                ]), DashPen(Qt.darkGray, 1)
                        )
                except KeyError:
                    pass
                w_s_y += height * y
                # print((x0, w_s_y), (hours * x, w_s_y), (hours * x, w_s_y + y * height), (x0, w_s_y + y * height))
            # вертикальные линии
            for i in range(1, hours + 1):
                self.scene.addPolygon(
                    QPolygonF(
                        [
                            QPointF(x0 + i * x, y0),
                            QPointF(x0 + i * x, w_s_y),
                        ]),
                )
                if i < hours:
                    self.scene.addPolygon(
                        QPolygonF(
                            [
                                QPointF(x0 + i * x + x // 2, y0),
                                QPointF(x0 + i * x + x // 2, w_s_y),
                            ]), DashPen(Qt.black, 1)
                    )
                    # if (self.view.transform().m11() >= 2):
                    #     self.scene.addPolygon(
                    #         QPolygonF(
                    #             [
                    #                 QPointF(i * x + x // 4, y0),
                    #                 QPointF(i * x + x // 4, w_s_y),
                    #             ]), QPen(Qt.black, 1, Qt.DashLine)
                    #     )
                    #     self.scene.addPolygon(
                    #         QPolygonF(
                    #             [
                    #                 QPointF(i * x + (x // 4)*3, y0),
                    #                 QPointF(i * x + (x // 4)*3, w_s_y),
                    #             ]), QPen(Qt.black, 1, Qt.DashLine)
                    #     )
                textitem = self.scene.addText(str(self.rmap.start + i - 1) + ":00")
                textitem.setPos(x0 + i * x - 12, y0 - 17)

    def on_click(self, pos):
        if self.rmap.visible:  # and (len(self.popUps) == 0 or not isinstance(self.popUps[-1], PopUp)):
            x = 180
            y = 50
            x0 = 50
            y0 = 50
            w_s_y = y0
            if x + x0 > pos[0] > x0:
                for w_id, way in enumerate(self.rmap.ways):
                    if w_s_y + y * way[1] > pos[1] > w_s_y:
                        print(way[0])
                        self.edit_row(w_id)
                        break
                    w_s_y += y * way[1]
            else:
                for w_id, way in enumerate(self.rmap.ways):
                    if w_s_y + y * way[1] > pos[1] > w_s_y:
                        try:
                            elems = self.rmap.elements[w_id]
                            for elem in elems:
                                x_s_el = x0 + x * (elem['time_s'].hour - self.rmap.start + 1) + (x // 60) * elem[
                                    'time_s'].minute
                                x_e_el = x0 + x * (elem['time_e'].hour - self.rmap.start + 1) + (x // 60) * elem[
                                    'time_e'].minute
                                if x_e_el > pos[0] > x_s_el:
                                    self.edit_elem(w_id, elem)
                                    print(elem['name'])
                                    break
                        except KeyError:
                            pass
                    w_s_y += y * way[1]

    def drop_element(self, el: DraggableLabel, pos):
        if self.rmap.visible:
            x = 180
            y = 50
            x0 = 50
            y0 = 50
            w_s_y = y0
            for w_id, way in enumerate(self.rmap.ways):
                if w_s_y + y * way[1] > pos[1] > w_s_y:
                    msg = PopUpInsertElement(self, "element_insert", el, w_id)
                    msg.show()
                    self.popUps.append(msg)
                    break
                w_s_y += y * way[1]

    def edit_elem(self, w_id: int, elem: dict):
        msg = PopUpEditElement(self, "element_edit", w_id, elem)
        msg.show()
        self.popUps.append(msg)
        # self.edit_row(self.rmap.ways[0])

        # def dragEnterEvent(self, event):
    #     if event.mimeData().hasText():
    #         event.acceptProposedAction()
    #     else:
    #         event.ignore()
    #
    # def dragMoveEvent(self, event):
    #     if event.mimeData().hasText():
    #         event.acceptProposedAction()
    #     else:
    #         event.ignore()
    #
    # def dropEvent(self, event):
    #     if event.mimeData().hasText():
    #         text = event.mimeData().text()
    #         item = QTableWidgetItem(text)
    #         item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)
    #         index = self.table.indexAt(event.pos())
    #         self.table.setItem(index.row(), index.column(), item)
    #         event.acceptProposedAction()
    #     else:
    #         event.ignore()
