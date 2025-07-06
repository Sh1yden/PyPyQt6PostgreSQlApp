from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.QtCore import pyqtSlot  # Slot функция реагирует на действие в программе

from MainMenu import MainMenu


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        # parent=self установка родительского окна для главного меню
        main_menu = MainMenu(parent=self)
        self.setMenuBar(main_menu)  # установка главного меню для окна

        main_menu.about.triggered.connect(self.about)
        main_menu.about_qt.triggered.connect(self.about_qt)

    @pyqtSlot()  # Декоратор, чтобы показать что это именно слот, а не просто функция
    def about(self):
        title = "Managing student assignments"
        text = ("Program for managing assignments\n" +
                "and tasks for students school")
        QMessageBox.about(self, title, text)

    @pyqtSlot()
    def about_qt(self):
        QMessageBox.aboutQt(self, "Managing student assignments")
