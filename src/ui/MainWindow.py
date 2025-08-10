# ===== MAIN WINDOW CLASS / КЛАСС ГЛАВНОГО ОКНА =====

# ===== IMPORTS / ИМПОРТЫ =====
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.QtCore import pyqtSlot  # Slot function responds to program actions / Slot функция реагирует на действие в программе
from src.ui.MainMenu import MainMenu
from src.controllers.Teacher import View
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
        self.setWindowTitle("Managing student assignments")

        # ===== MAIN MENU SETUP / НАСТРОЙКА ГЛАВНОГО МЕНЮ =====
        # Parent=self sets parent window for main menu / Parent=self установка родительского окна для главного меню
        main_menu = MainMenu(parent=self)
        self.setMenuBar(main_menu)  # Set main menu for window / установка главного меню для окна

        # ===== CENTRAL WIDGET SETUP / НАСТРОЙКА ЦЕНТРАЛЬНОГО ВИДЖЕТА =====
        # Create and set Teacher.View as central widget / Создание и установка Teacher.View как центрального виджета
        self.teacher_view = View()
        self.setCentralWidget(self.teacher_view)

        # ===== SIGNAL CONNECTIONS / ПОДКЛЮЧЕНИЕ СИГНАЛОВ =====
        # Teacher menu connections / Меню Учителя
        main_menu.add.triggered.connect(self.teacher_view.add)
        main_menu.update.triggered.connect(self.teacher_view.uppdate)
        main_menu.delete.triggered.connect(self.teacher_view.delete)

        # Help menu connections / Меню помощи
        main_menu.about.triggered.connect(self.about)
        main_menu.about_qt.triggered.connect(self.about_qt)

    # ===== SLOT METHODS / МЕТОДЫ-СЛОТЫ =====
    # Decorator to show this is a slot, not just a function /
    # Декоратор, чтобы показать что это именно слот, а не просто функция
    @pyqtSlot()
    def about(self):
        title = "Managing student assignments"
        text = ("Program for managing assignments\n" +
                "and tasks for students school")
        QMessageBox.about(self, title, text)

    @pyqtSlot()
    def about_qt(self):
        QMessageBox.aboutQt(self, "Managing student assignments")
