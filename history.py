from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QInputDialog, QMessageBox, QLineEdit
from PyQt5.QtCore import Qt
import os

class HistoryTab(QWidget):
   def __init__(self):
       super().__init__()
       self.layout = QVBoxLayout()
       self.files_box = QFileDialog()
       self.files_box.setFileMode(QFileDialog.FileMode.ExistingFiles)
       self.files_box.setNameFilter('*.xml')
       self.files_box.setDirectory('maps') # Set default directory to "maps"
       self.layout.addWidget(self.files_box)

       self.create_button = QPushButton("Create File")
       self.create_button.setStyleSheet("""
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
           QPushButton:pressed {
               background-color: rgb(224, 0, 0);
               border-style: inset;
           }
       """)
       self.create_button.clicked.connect(self.create_file)
       self.layout.addWidget(self.create_button)

       self.delete_button = QPushButton("Delete File")
       self.delete_button.setStyleSheet("""
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
           QPushButton:pressed {
               background-color: rgb(224, 0, 0);
               border-style: inset;
           }
       """)
       self.delete_button.clicked.connect(self.delete_file)
       self.layout.addWidget(self.delete_button)

       self.setStyleSheet("background-color: white;")
       self.setLayout(self.layout)

   def create_file(self):
       text, okPressed = QInputDialog.getText(self, "Create File", "Enter file name:", QLineEdit.Normal, "")
       if okPressed and text != '':
           with open(os.path.join('maps', f'{text}.xml'), 'w') as file: # Use 'maps' as the directory
               pass

   def delete_file(self):
       selected_files = self.files_box.selectedFiles()
       if selected_files:
           file_to_delete = selected_files[0]
           os.remove(file_to_delete)
       else:
           QMessageBox.warning(self, "Warning", "No file selected for deletion.")
