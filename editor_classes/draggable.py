from PyQt5.QtCore import QMimeData, Qt
from PyQt5.QtGui import QDrag, QPixmap
from PyQt5.QtWidgets import QLabel


class DraggableLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptDrops(True)

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