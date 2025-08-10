from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.QtCore import pyqtSlot  # Slot функция реагирует на действие в программе.
from src.ui.MainMenu import MainMenu
from src.controllers.Teacher import View
from src.core.Logger import Logger


class MainWindow(QMainWindow):
    """Класс главного окна приложения."""

    # Конструктор класса.
    def __init__(self, parent=None):
        # Настройка главного окна.
        super().__init__(parent)

        # Инициализация логера.
        self.lg = Logger()
        self.lg.debug("Constructor launched in class MainMenu.")
        self.lg.debug("Logger created in class MainMenu().")

        self.setWindowTitle("Managing student assignments")

        # Настройка главного меню.
        # Parent=self установка родительского окна для главного меню.
        main_menu = MainMenu(parent=self)
        self.setMenuBar(main_menu)  # установка главного меню для окна.

        # Создание и установка Teacher.View как центрального виджета.
        self.teacher_view = View()
        self.setCentralWidget(self.teacher_view)

        # Настройка кнопок.
        # Меню Учителя.
        main_menu.add.triggered.connect(self.teacher_view.add)
        main_menu.update.triggered.connect(self.teacher_view.uppdate)
        main_menu.delete.triggered.connect(self.teacher_view.delete)
        # Меню помощи.
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
