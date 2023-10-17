from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtCore import QUrl
import os
class DocumentationTab(QWidget):
    def __init__(self):
        super().__init__()
        self.webView = QWebEngineView()
        self.webView.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.webView.settings().setAttribute(QWebEngineSettings.PdfViewerEnabled, True)
        #pdf_path = os.path.abspath("/Russian_Railways/docs.pdf")
        pdf_path = os.path.abspath("../Russian_Railways/docs.pdf")
        self.webView.setUrl(QUrl.fromLocalFile(pdf_path))
        layout = QVBoxLayout()
        layout.addWidget(self.webView)
        self.setLayout(layout)