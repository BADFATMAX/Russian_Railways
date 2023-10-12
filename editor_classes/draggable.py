import os

from PyQt5 import QtSvg, QtGui
from PyQt5.QtCore import QMimeData, Qt, QRect, QSize
from PyQt5.QtGui import QDrag, QPixmap, QImage, QPainter, QCursor, QMovie
from PyQt5.QtWidgets import QLabel, QWidget, QMessageBox, QVBoxLayout, QSizePolicy
from typing import Union


class DraggableLabel(QLabel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.setAcceptDrops(True)
        self.text_ : Union[str, None] = None
        self.uri_: Union[str, None] = None
        self.msg : Union[QLabel, None] = None
        self.mov_label = None
        self.movie = None
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

        label = QLabel()
        gif_p = os.path.join("elements", "gifs", self.uri_ + ".gif")
        if os.path.exists(gif_p):
            movie = QMovie(gif_p)
        else:
            movie = QMovie(os.path.join("elements", "gifs", "wagon.gif"))
        movie.setScaledSize(QSize(300, 280))
        label.setMovie(movie)
        label.setGeometry(QRect(0, 0, 300, 280))
        label.setMaximumSize(QSize(300, 280))
        sp = label.sizePolicy()
        sp.setHorizontalStretch(0)
        label.setSizePolicy(sp)
        label.setStyleSheet("border: 1px solid black;")
        self.parent.info_layout.addWidget(label)
        self.parent.info_layout.addWidget(msg)
        # self.parent.info_layout.addStretch(200)
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
        label.show()
        movie.start()
        self.msg = msg
        self.mov_label = label
        self.movie = movie

    def leaveEvent(self, event):
        self.movie.stop()
        self.msg.close()
        self.mov_label.close()
        self.parent.info_layout.removeWidget(self.msg)
        self.parent.info_layout.removeWidget(self.mov_label)
        self.msg = None
        self.mov_label = None
        self.movie = None

    def text(self) -> str:
        return self.text_
