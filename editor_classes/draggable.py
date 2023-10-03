from PyQt5 import QtSvg, QtGui
from PyQt5.QtCore import QMimeData, Qt
from PyQt5.QtGui import QDrag, QPixmap, QImage, QPainter, QCursor
from PyQt5.QtWidgets import QLabel, QWidget, QMessageBox, QVBoxLayout
from typing import Union


class DraggableLabel(QLabel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.setAcceptDrops(True)
        self.text_ : Union[str, None] = None
        self.msg : Union[QLabel, None] = None
        # renderer = QtSvg.QSvgRenderer('elements\\anchoring.svg')
        # self.resize(renderer.defaultSize())
        # pixmap = QPixmap()
        # painter = QPainter(pixmap)
        # renderer.render(painter)
        # self.setPixmap(pixmap)
        # renderer.render(self)
        # self.setPixmap(renderer)

    # def mousePressEvent(self, event):
    #     pixmap = QPixmap(self.size())
    #     self.render(pixmap)
    #
    #     mime_data = QMimeData()
    #     mime_data.setText(self.text())
    #
    #     drag = QDrag(self)
    #     drag.setMimeData(mime_data)
    #     drag.setPixmap(pixmap)
    #     drag.setHotSpot(event.pos())
    #
    #     drag.exec_(Qt.MoveAction)
    def mouseMoveEvent(self, event):
        drag = QDrag(self)
        mime = QMimeData()
        pixmap = QPixmap(self.size())
        self.render(pixmap)
        drag.setMimeData(mime)
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())
        drag.exec_(Qt.MoveAction)

    def enterEvent(self, event):
        msg = QLabel(self.text())
        self.parent.info_layout.addWidget(msg)
        # msg = QWidget()
        # msg.setWindowFlags(Qt.FramelessWindowHint)
        # msg.setGeometry(0, 0, 150, 100)
        # layout = QVBoxLayout()
        # label = QLabel("qfdfqwf")
        # label.setStyleSheet("border: 1px solid black;")
        # layout.addWidget(QLabel("qfdfqwf"))
        # msg.move(QCursor().pos().x(), QCursor().pos().y())
        # msg.setLayout(layout)
        # # msg.setAttribute(Qt.WA_TranslucentBackground)
        msg.show()
        self.msg = msg

    def leaveEvent(self, event):
        self.parent.info_layout.removeWidget(self.msg)
        self.msg = None

    def text(self) -> str:
        return self.text_
