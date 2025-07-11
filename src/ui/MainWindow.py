from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.QtCore import pyqtSlot  # Slot функция реагирует на действие в программе.
from src.ui.MainMenu import MainMenu


class MainWindow(QMainWindow):
    """Класс главного окна приложения."""

    # Конструктор класса.
    def __init__(self, parent=None):
        # Настройка главного окна.
        super().__init__(parent)
        self.setWindowTitle("Managing student assignments")

        # Настройка главного меню.
        # parent=self установка родительского окна для главного меню.
        main_menu = MainMenu(parent=self)
        self.setMenuBar(main_menu)  # установка главного меню для окна.
        # Настройка кнопок.
        main_menu.about.triggered.connect(self.about)
        main_menu.about_qt.triggered.connect(self.about_qt)

    @pyqtSlot()  # Декоратор, чтобы показать что это именно слот, а не просто функция.
    def about(self):
        title = "Managing student assignments"
        text = ("Program for managing assignments\n" +
                "and tasks for students school")
        QMessageBox.about(self, title, text)

    @pyqtSlot()
    def about_qt(self):
        QMessageBox.aboutQt(self, "Managing student assignments")
