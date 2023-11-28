import os
import shutil
import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QApplication, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDragEnterEvent, QDragMoveEvent, QDropEvent

class AdminTab(QWidget):
  def __init__(self):
      super().__init__()
      self.initUI()

  def initUI(self):
      self.setWindowTitle("Image Dropper")
      self.setGeometry(200, 200, 800, 800)

      self.layout = QVBoxLayout()
      self.setLayout(self.layout)

      self.folderButton = QPushButton('ВЫБОР ДИРЕКТОРИИ')
      self.folderButton.setStyleSheet("background-color: red; border-radius: 20px;color:white;min-height:80px; text-align:center;font-size: 22px;")
      self.folderButton.clicked.connect(self.chooseFolder)
      self.folderButton.setStyleSheet("""
    QPushButton {
        background-color: red;
        border-radius: 20px;
        color: white;
        min-height: 120px;
        text-align: center;
        font-size: 22px;
        font-weight: bold; 
    }
    QPushButton:hover {
        background-color: #B22222;
    }
""")
      self.layout.addWidget(self.folderButton)

      self.imageLayout = QHBoxLayout()
      self.layout.addLayout(self.imageLayout)

      self.imageBox = ImageBox()
      self.imageLayout.addWidget(self.imageBox)

      self.imageLabel = QLabel()
      self.imageLabel.setPixmap(QPixmap("GamePics/admin.png").scaled(750, 750, Qt.KeepAspectRatio))
      self.layout.addWidget(self.imageLabel)
      self.layout.setAlignment(self.imageLabel, Qt.AlignCenter)


      self.show()

  def chooseFolder(self):
      folder = QFileDialog.getExistingDirectory(self, "Choose folder", "games/CardGame/images")
      if folder:
          self.imageBox.target_folder = folder

class ImageBox(QWidget):
  def __init__(self):
      super().__init__()
      self.setAcceptDrops(True)
      self.initUI()

  def initUI(self):
      self.layout = QVBoxLayout()
      self.setLayout(self.layout)
      self.layout.setAlignment(Qt.AlignTop)

      self.label = QLabel('<font color="red" size="45">ПЕРЕНЕСИТЕ ЭЛЕМЕНТ В ЭТУ ОБЛАСТЬ</font>')
      self.layout.addWidget(self.label)

      self.setStyleSheet("border: 20px solid red;")

  def dragEnterEvent(self, event: QDragEnterEvent):
      if event.mimeData().hasUrls():
          event.acceptProposedAction()

  def dragMoveEvent(self, event: QDragMoveEvent):
      event.acceptProposedAction()

  def dropEvent(self, event: QDropEvent):
      if event.mimeData().hasUrls():
          event.setDropAction(Qt.CopyAction)
          event.accept()

          for url in event.mimeData().urls():
              filepath = url.toLocalFile()
              if os.path.isfile(filepath):
                self.saveImage(filepath)

  def saveImage(self, filepath):
      target_folder = self.target_folder
      image_count = len(os.listdir(target_folder))
      target_path = os.path.join(target_folder, f"img{image_count+1}.png")
      shutil.copy(filepath, target_path)

      self.label.setText('<font color="red" size="45">ЭЛЕМЕНТ УСПЕШНО ДОБАВЛЕН!</font>')

if __name__ == "__main__":
  app = QApplication(sys.argv)
  adminTab = AdminTab()
  sys.exit(app.exec_())
