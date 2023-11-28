from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextBrowser, QTreeWidget, QTreeWidgetItem, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class DocumentationTab(QWidget):
   def __init__(self):
       super().__init__()
       self.layout = QHBoxLayout()

       # Create a QTreeWidget for the headers
       self.tree = QTreeWidget()
       self.tree.setHeaderLabels(["Разделы документации"])

       # Add headers to the tree
       headers = ["Назначение программы", "Графический интерфейс", "Условные обозначения"]
       for header in headers:
           item = QTreeWidgetItem(self.tree)
           item.setText(0, header)

       # Connect the tree item clicked signal to a method
       self.tree.itemClicked.connect(self.on_tree_item_clicked)

       self.tree.setStyleSheet("""
            QTreeWidget {
            max-width: 300px;
            border-radius: 30px;
            background-color: red;
            font-weight: bold;
            color:white;
            }
            QTreeWidget::item {
            font-weight: bold;
            color:white;
            }
            QHeaderView::section {
            font-weight: bold;
            }
            """)

       self.tree.setFont(QFont("Arial", 10)) 
       # Create a QTextBrowser for the documentation
       self.textBrowser = QTextBrowser()
       self.textBrowser.setStyleSheet("QTextBrowser { background-color: white; }")

       # Add the documentation text to the QTextBrowser
       doc_text = """
        <h1>Назначение программы</h1>
        <p>Программа предназначена для автоматизации процессов проверки соблюдения всех необходимых условий формирования принципиальных и монтажных схем, проверки непротиворечивости информации в схемах, а также создание алгоритмов сверки различных видов схем между собой.</p>
        <p>Также предполагается создание и реализация алгоритмов автоматизированной корректировки принципиальных и монтажных схем после автоматизированной экспертизы.</p>
        <p>Применение данной программы должно обеспечить экономию трудозатрат эксплуатационного персонала, сократит время на проверку технической документации, ее корректировку и перевод в электронный вид.</p>
        <h1>Графический интерфейс программы</h1>
        <p>После запуска программы на экране появится стартовая страница, предназначенная для начала работы с программой и загрузки данных, окно показано на рисунке 1.1.</p>
        <p>Рис. 1.1</p>
        <img src="GamePics/doc1.jpg" alt="Рисунок 1.1 – Стартовая страница программы">
        <p>Данное окно разделено на следующие области:</p>
        <ol>
            <li>Панель управления</li>
            <li>Область меню операций над источниками данных</li>
        </ol>
        <h1>Условные обозначения технологических операций</h1>
        <p>Рис. 1.2</p>
        <img src="GamePics/doc2.jpg" alt="Условные обозначения технологических операций">
        """
       self.textBrowser.setHtml(doc_text)

       # Add the tree and the QTextBrowser to the layout
       self.layout.addWidget(self.tree)
       self.layout.addWidget(self.textBrowser)

       self.setLayout(self.layout)

   # When a tree item is clicked, scroll the QTextBrowser to the corresponding section
   def on_tree_item_clicked(self, item):
       section = item.text(0)
       self.textBrowser.find(section)
