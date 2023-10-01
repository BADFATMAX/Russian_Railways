from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLabel
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag, QPixmap


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

class CustomTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        
    def dropEvent(self, event):
        if event.mimeData().hasText():
            text = event.mimeData().text()
            item = QTableWidgetItem(text)
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)
            index = self.indexAt(event.pos())
            self.setItem(index.row(), index.column(), item)
            event.acceptProposedAction()
        else:
            event.ignore()

class EditorTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        button_layout = QHBoxLayout()

        self.add_row_button = QPushButton("Add Row")
        self.add_row_button.clicked.connect(self.add_row)

        self.remove_row_button = QPushButton("Remove Row")
        self.remove_row_button.clicked.connect(self.remove_row)

        self.add_column_button = QPushButton("Add Column")
        self.add_column_button.clicked.connect(self.add_column)

        self.remove_column_button = QPushButton("Remove Column")
        self.remove_column_button.clicked.connect(self.remove_column)

        button_layout.addWidget(self.add_row_button)
        button_layout.addWidget(self.remove_row_button)
        button_layout.addWidget(self.add_column_button)
        button_layout.addWidget(self.remove_column_button)

        self.table = CustomTableWidget()
        self.table.setRowCount(5)
        self.table.setColumnCount(4)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setDragDropMode(QTableWidget.DragDrop)

        self.layout.addLayout(button_layout)
        self.layout.addWidget(self.table)

        self.elements = []
        for i in range(5):
            element = DraggableLabel(f"Element {i+1}")
            element.setFixedSize(100, 50)
            element.setStyleSheet("border: 1px solid black;")
            self.elements.append(element)
            self.layout.addWidget(element)

        self.setLayout(self.layout)

    def add_row(self):
        current_row_count = self.table.rowCount()
        self.table.setRowCount(current_row_count + 1)

    def remove_row(self):
        current_row_count = self.table.rowCount()
        if current_row_count > 0:
            self.table.setRowCount(current_row_count - 1)

    def add_column(self):
        current_column_count = self.table.columnCount()
        self.table.setColumnCount(current_column_count + 1)

    def remove_column(self):
        current_column_count = self.table.columnCount()
        if current_column_count > 0:
            self.table.setColumnCount(current_column_count - 1)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            text = event.mimeData().text()
            item = QTableWidgetItem(text)
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)
            index = self.table.indexAt(event.pos())
            self.table.setItem(index.row(), index.column(), item)
            event.acceptProposedAction()
        else:
            event.ignore()