from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.QtCore import pyqtSlot  # Slot функция реагирует на действие в программе.
from src.ui.MainMenu import MainMenu
from src.ui.widgets.TableView import TableView
from src.controllers.Teacher import View


class MainWindow(QMainWindow):
    """Класс главного окна приложения."""

    # Конструктор класса.
    def __init__(self, parent=None):
        # Настройка главного окна.
        super().__init__(parent)
        self.setWindowTitle("Managing student assignments")

        # Настройка главного меню.
        # Parent=self установка родительского окна для главного меню.
        main_menu = MainMenu(parent=self)
        self.setMenuBar(main_menu)  # установка главного меню для окна.
        # Настройка кнопок.
        # Меню Учителя.
        main_menu.add.triggered.connect(self.add)
        main_menu.update.triggered.connect(self.uppdate)
        main_menu.delete.triggered.connect(self.delete)

        # Меню помощи.
        main_menu.about.triggered.connect(self.about)
        main_menu.about_qt.triggered.connect(self.about_qt)
        # Создание и установка TableView как центрального виджета.
        self.table_view = TableView("Teacher")  # ! Имя таблицы в БД.
        self.setCentralWidget(self.table_view)

    @pyqtSlot()
    def add(self):
        teacher = View()
        teacher.add()

    @pyqtSlot()
    def uppdate(self):
        teacher = View()
        teacher.uppdate()

    @pyqtSlot()
    def delete(self):
        teacher = View()
        teacher.delete()

    @pyqtSlot()  # Декоратор, чтобы показать что это именно слот, а не просто функция.
    def about(self):
        title = "Managing student assignments"
        text = ("Program for managing assignments\n" +
                "and tasks for students school")
        QMessageBox.about(self, title, text)

    @pyqtSlot()
    def about_qt(self):
        QMessageBox.aboutQt(self, "Managing student assignments")
