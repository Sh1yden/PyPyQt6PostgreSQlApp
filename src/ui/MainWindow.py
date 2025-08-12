# ===== MAIN WINDOW CLASS / КЛАСС ГЛАВНОГО ОКНА =====

# ===== IMPORTS / ИМПОРТЫ =====
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QStyle
from PyQt6.QtCore import pyqtSlot  # Slot function responds to program actions / Slot функция реагирует на действие в программе
from PyQt6.QtGui import QIcon

# ! Смена класса отображения
from src.controllers.Teacher import View # Teacher
# from src.controllers.Student import View # Student
# from src.controllers.StGroup import View # Group

from src.ui.MainMenu import MainMenu
from src.core.Logger import Logger


# ===== MAIN WINDOW CLASS / КЛАСС ГЛАВНОГО ОКНА =====
class MainWindow(QMainWindow):
    """
    Main application window class / Класс главного окна приложения
    Manages the primary user interface and coordinates application components / Управляет основным пользовательским интерфейсом и координирует компоненты приложения
    """

    # ===== INITIALIZATION / ИНИЦИАЛИЗАЦИЯ =====
    def __init__(self, parent=None):
        """
        Class constructor / Конструктор класса

        Args:
            parent: Parent widget / Родительский виджет
        """
        # Main window setup / Настройка главного окна
        super().__init__(parent)

        # ===== LOGGER INITIALIZATION / ИНИЦИАЛИЗАЦИЯ ЛОГГЕРА =====
        self.lg = Logger()
        self.lg.debug("Constructor launched in class MainMenu.")
        self.lg.debug("Logger created in class MainMenu().")

        # ===== WINDOW CONFIGURATION / КОНФИГУРАЦИЯ ОКНА =====
        # Window title / Имя окна
        self.setWindowTitle("Managing student assignments")
        # Window icon / Иконка окна
        # TODO добавить свою иконку
        self._icon: QIncon = QIcon()
        if self._icon.isNull():
            self._icon: QIncon = QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))
        self.setWindowIcon(self._icon)

        # ===== MAIN MENU SETUP / НАСТРОЙКА ГЛАВНОГО МЕНЮ =====
        # Parent=self sets parent window for main menu / Parent=self установка родительского окна для главного меню
        main_menu = MainMenu(parent=self)
        self.setMenuBar(main_menu)  # Set main menu for window / установка главного меню для окна

        # ===== CENTRAL WIDGET SETUP / НАСТРОЙКА ЦЕНТРАЛЬНОГО ВИДЖЕТА =====
        # Create and set Teacher.View as central widget / Создание и установка Teacher.View как центрального виджета
        # Teacher
        self.teacher_view = View()
        self.setCentralWidget(self.teacher_view)

        # Student
        # self.student_view = View()
        # self.setCentralWidget(self.student_view)

        # Group
        # self.st_group_view = View()
        # self.setCentralWidget(self.st_group_view)

        # ===== SIGNAL CONNECTIONS / ПОДКЛЮЧЕНИЕ СИГНАЛОВ =====
        # Teacher menu connections / Меню Учителя
        main_menu.teacher_add.triggered.connect(self.teacher_view.add)
        main_menu.teacher_update.triggered.connect(self.teacher_view.uppdate)
        main_menu.teacher_delete.triggered.connect(self.teacher_view.delete)

        # Student menu connections / Меню Ученика
        # main_menu.student_add.triggered.connect(self.student_view.add)
        # main_menu.student_update.triggered.connect(self.student_view.uppdate)
        # main_menu.student_delete.triggered.connect(self.student_view.delete)

        # Group menu connections / Меню Группы
        # main_menu.st_group_add.triggered.connect(self.st_group_view.add)
        # main_menu.st_group_update.triggered.connect(self.st_group_view.uppdate)
        # main_menu.st_group_delete.triggered.connect(self.st_group_view.delete)

        # Help menu connections / Меню помощи
        main_menu.about.triggered.connect(self.about)
        main_menu.about_qt.triggered.connect(self.about_qt)

    # ===== SLOT METHODS / МЕТОДЫ-СЛОТЫ =====
    # Decorator to show this is a slot, not just a function /
    # Декоратор, чтобы показать что это именно слот, а не просто функция
    @pyqtSlot()
    def about(self):
        """Show information about the program / Показать информацию о программе"""
        QMessageBox.about(self, "About program",
                         "School management application\n"
                         "Version 1.0\n"
                         "Built with PyQt6 and PostgreSQL")
        self.lg.debug("MainWindow about program dialog shown. In DEF about().")

    @pyqtSlot()
    def about_qt(self):
        """Show information about Qt / Показать информацию о Qt"""
        QMessageBox.aboutQt(self, "About Qt")
        self.lg.debug("MainWindow about Qt dialog shown. In DEF about_qt().")