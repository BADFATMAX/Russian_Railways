import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from editor import EditorTab
from history import HistoryTab
from rhythm_game import RhythmGameTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQT Tabs")
        self.tab_widget = QTabWidget()

        editor_tab = EditorTab()
        history_tab = HistoryTab()
        rhythm_game = RhythmGameTab()

        self.tab_widget.addTab(editor_tab, "Editor")
        self.tab_widget.addTab(history_tab, "History")
        self.tab_widget.addTab(rhythm_game, "Rhythm Game")

        self.setCentralWidget(self.tab_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
