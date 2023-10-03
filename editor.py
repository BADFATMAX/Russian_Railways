from PyQt5.QtCore import QPointF
from PyQt5.QtCore import QPointF
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag, QPixmap, QPainter, QPolygonF, QPen, QBrush
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGraphicsScene, QGraphicsView, \
    QFileDialog

from editor_classes.draggable import DraggableLabel
from editor_classes.editorscene import EditorScene
from editor_classes.popup import PopUpInput, PopUp, PopUpEditWay, deleteItemsOfLayout, PopUpInsertElement, PopUpEditElement
from map_class import RailMap


class EditorTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.button_layout = QHBoxLayout()
        self.popUps = []
        self.rmap = RailMap()

        save_map_button = QPushButton("Save")
        save_map_button.clicked.connect(self.save_map)
        load_map_button = QPushButton("Load")
        load_map_button.clicked.connect(self.load_map)
        new_map_button = QPushButton("New")
        new_map_button.clicked.connect(self.new_map)
        add_row_button = QPushButton("Add Row")
        add_row_button.clicked.connect(self.add_row)
        remove_row_button = QPushButton("Remove Row")
        remove_row_button.clicked.connect(self.remove_row)

        self.button_layout.addWidget(save_map_button)
        self.button_layout.addWidget(load_map_button)
        self.button_layout.addWidget(new_map_button)
        self.button_layout.addWidget(add_row_button)
        self.button_layout.addWidget(remove_row_button)

        self.layout.addLayout(self.button_layout)

        self.scene = EditorScene(self, 0, 0, 4000, 1080)

        self.view = QGraphicsView(self.scene)
        self.view.setAcceptDrops(True)
        self.view.setRenderHint(QPainter.Antialiasing)

        self.layout.addWidget(self.view)

        self.elements = []
        for i in range(5):
            element = DraggableLabel(f"Element {i + 1}")
            element.setFixedSize(100, 50)
            element.setStyleSheet("border: 1px solid black;")
            self.elements.append(element)
            self.layout.addWidget(element)

        self.setLayout(self.layout)

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
            new_el = {'name': popUpObj.content['element'].text(), 'time_s': popUpObj.content['time_s'],
                      'time_e': popUpObj.content['time_e']}
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
        self.scene.clear()
        print("popups: ", self.popUps)
        x = 180
        y = 50
        x0 = 0
        y0 = 17
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
                        QPointF(hours * x, w_s_y),
                        QPointF(hours * x, w_s_y + y * height),
                        QPointF(x0, w_s_y + y * height),
                    ]),
            )
            # имя пути
            textitem = self.scene.addText(name)
            textitem.setPos(3, w_s_y + height // 2)
            try:
                elements = self.rmap.elements[w_id]
                for el in elements:
                    # сделать функционал для отрисовки элементов, разных
                    x_s_el = x0 + x * (el['time_s'].hour - self.rmap.start + 1) + (x // 60) * el['time_s'].minute
                    x_e_el = x0 + x * (el['time_e'].hour - self.rmap.start + 1) + (x // 60) * el['time_e'].minute
                    self.scene.addPolygon(
                        QPolygonF(
                            [
                                QPointF(x_s_el, w_s_y),
                                QPointF(x_e_el, w_s_y),
                                QPointF(x_e_el, w_s_y + y * height),
                                QPointF(x_s_el, w_s_y + y * height),
                            ]),
                        brush=QBrush(Qt.lightGray)
                    )
                    textitem = self.scene.addText(el['name'])
                    textitem.setPos(x_s_el, w_s_y + (y // 2))
            except KeyError:
                pass
            w_s_y += height * y
            # print((x0, w_s_y), (hours * x, w_s_y), (hours * x, w_s_y + y * height), (x0, w_s_y + y * height))
        # вертикальные линии
        for i in range(1, hours + 1):
            self.scene.addPolygon(
                QPolygonF(
                    [
                        QPointF(i * x, y0),
                        QPointF(i * x, w_s_y),
                    ]),
            )
            if i < hours:
                self.scene.addPolygon(
                    QPolygonF(
                        [
                            QPointF(i * x + x // 2, y0),
                            QPointF(i * x + x // 2, w_s_y),
                        ]), QPen(Qt.black, 1, Qt.DotLine)
                )
            textitem = self.scene.addText(str(self.rmap.start + i - 1) + ":00")
            textitem.setPos(i * x - 12, 0)

    def on_click(self, pos):
        if self.rmap.visible:  # and (len(self.popUps) == 0 or not isinstance(self.popUps[-1], PopUp)):
            x = 180
            y = 50
            x0 = 0
            y0 = 17
            w_s_y = y0
            if x > pos[0] > x0:
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
            x0 = 0
            y0 = 17
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
