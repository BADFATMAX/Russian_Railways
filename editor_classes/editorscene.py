from PyQt5.QtWidgets import QGraphicsScene, QGraphicsSceneDragDropEvent

from .draggable import DraggableLabel


class EditorScene(QGraphicsScene):
    def __init__(self, parent, *args):
        super().__init__(*args)
        self.parent = parent

    def mousePressEvent(self, event):
        pos = (event.scenePos().x(), event.scenePos().y())
        print(pos)
        self.parent.on_click(pos)

    def dragEnterEvent(self, e):
        if isinstance(e.source(), DraggableLabel):
            e.accept()

    def dragMoveEvent(self, event):
        event.setAccepted(True)

    def dropEvent(self, event):
        # print(event.source().text())
        self.parent.drop_element(event.source(), (event.scenePos().x(), event.scenePos().y()))
