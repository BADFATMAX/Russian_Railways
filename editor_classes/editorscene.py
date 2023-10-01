from PyQt5.QtWidgets import QGraphicsScene


class EditorScene(QGraphicsScene):
    def __init__(self, parent, *args):
        super().__init__(*args)
        self.parent = parent

    def mousePressEvent(self, event):
        pos = (event.scenePos().x(), event.scenePos().y())
        print(pos)
        self.parent.on_click(pos)
