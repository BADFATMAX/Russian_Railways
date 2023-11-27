import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from editor import EditorTab
from history import HistoryTab
from story import StoryTab
from games_tab import GamesTab
from documentation import DocumentationTab
from leaderboard import LeaderboardTab

from editor_classes import popup

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQT Tabs")
        self.tab_widget = QTabWidget()

        editor_tab = EditorTab()
        history_tab = HistoryTab()
        story_tab = StoryTab()
        rhythm_game = GamesTab(self)
        docs_tab = DocumentationTab()
        leaderboard_tab = LeaderboardTab() 

        self.tab_widget.addTab(editor_tab, "Editor")
        self.tab_widget.addTab(history_tab, "История Карт")
        self.tab_widget.addTab(story_tab, "Сюжет")
        self.tab_widget.addTab(rhythm_game, "Игры")
        self.tab_widget.addTab(docs_tab, "Документация")
        self.tab_widget.addTab(leaderboard_tab, "Статистика")

        self.setCentralWidget(self.tab_widget)
        
        msg = popup.PopUp(self, "login")
        msg.show()
        # self.popUps.append(msg)
    
    def pop_up_handle(self, popUpObj: popup.PopUp):
        self.children()[-1].setParent(None)
        print("children: ", len(self.children()))
        for child in self.children():
            print(child, " children: ", len(child.children()))

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())