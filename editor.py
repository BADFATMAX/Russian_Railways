from PyQt5.QtCore import QPointF
from PyQt5.QtCore import QPointF
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag, QPixmap, QPainter, QPolygonF, QPen
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGraphicsScene, QGraphicsView, \
    QFileDialog

from editor_classes.popupinput import PopUpInput
from map_class import RailMap


class DraggableLabel(QLabel):
    def mousePressEvent(self, event):
        pixmap = QPixmap(self.size())
        self.render(pixmap)

        mime_data = QMimeData()
        mime_data.setText(self.text())

        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())

        drag.exec_(Qt.MoveAction)


class EditorTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.button_layout = QHBoxLayout()
        self.popUps = []
        self.rmap = None

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

        # self.add_column_button = QPushButton("Add Column")
        # self.add_column_button.clicked.connect(self.add_column)
        #
        # self.remove_column_button = QPushButton("Remove Column")
        # self.remove_column_button.clicked.connect(self.remove_column)

        self.button_layout.addWidget(save_map_button)
        self.button_layout.addWidget(load_map_button)
        self.button_layout.addWidget(new_map_button)
        self.button_layout.addWidget(add_row_button)
        self.button_layout.addWidget(remove_row_button)
        # button_layout.addWidget(self.add_column_button)
        # button_layout.addWidget(self.remove_column_button)

        # self.table = CustomTableWidget()
        # self.table.setRowCount(5)
        # self.table.setColumnCount(4)
        # self.table.setSelectionMode(QTableWidget.SingleSelection)
        # self.table.setDragDropMode(QTableWidget.DragDrop)

        self.layout.addLayout(self.button_layout)
        # self.layout.addWidget(self.table)

        self.scene = QGraphicsScene(0, 0, 4000, 1080)
        # self.draw_map()

        self.view = QGraphicsView(self.scene)
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

    def pop_up_input_handle(self, popUpInputObj: PopUpInput):
        if popUpInputObj.op == "add_row":
            self.rmap.ways.append([popUpInputObj.content, 1])
        self.popUps.remove(popUpInputObj)
        self.draw_map()

    def add_row(self):
        if self.rmap is not None:
            msg = PopUpInput(self, "add_row")
            msg.show()
            self.popUps.append(msg)
        # current_row_count = self.table.rowCount()
        # self.table.setRowCount(current_row_count + 1)

    def remove_row(self):
        if self.rmap is not None:
            if len(self.rmap.ways) > 0:
                self.rmap.ways.pop()
                self.draw_map()
        # current_row_count = self.table.rowCount()
        # if current_row_count > 0:
        #     self.table.setRowCount(current_row_count - 1)

    def new_map(self):
        self.rmap = RailMap()
        self.draw_map()

    def file_save(self):
        pass

    # def add_column(self):
    #     current_column_count = self.table.columnCount()
    #     self.table.setColumnCount(current_column_count + 1)
    #
    # def remove_column(self):
    #     current_column_count = self.table.columnCount()
    #     if current_column_count > 0:
    #         self.table.setColumnCount(current_column_count - 1)

    def draw_map(self):
        self.scene.clear()
        print("popups: ", self.popUps)
        x = 150
        y = 50
        x0 = 0
        y0 = 17
        w_s_y = y0
        hours = self.rmap.end - self.rmap.start + 1
        # рендерит прямоугольники (пути)
        for way in self.rmap.ways:
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
            w_s_y += height * y
            print((x0, w_s_y), (hours * x, w_s_y), (hours * x, w_s_y + y * height), (x0, w_s_y + y * height))
        # вертикальные линии
        for i in range(1, hours+1):
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
                            QPointF(i * x + x//2, y0),
                            QPointF(i * x + x//2, w_s_y),
                        ]), QPen(Qt.black, 1, Qt.DotLine)
                )
            textitem = self.scene.addText(str(self.rmap.start + i - 1) + ":00")
            textitem.setPos(i * x - 12, 0)
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
