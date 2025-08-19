# ===== MAIN WINDOW CLASS FOR APPLICATION UI / КЛАСС ГЛАВНОГО ОКНА ДЛЯ UI ПРИЛОЖЕНИЯ =====
# Primary application window managing user interface and component coordination
# Основное окно приложения, управляющее пользовательским интерфейсом и координацией компонентов

# ===== IMPORTS / ИМПОРТЫ =====
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QStyle
from PyQt6.QtCore import pyqtSlot  # Slot function responds to program actions / Slot функция реагирует на действие в программе
from PyQt6.QtGui import QIcon

# ===== VIEW IMPORTS - ENTITY CONTROLLERS / ИМПОРТЫ ПРЕДСТАВЛЕНИЙ - КОНТРОЛЛЕРЫ СУЩНОСТЕЙ =====
# ! Change display class here / ! Смена класса отображения здесь
import src.controllers.Teacher as Teacher  # Teacher view / Представление учителя
import src.controllers.Student as Student  # Student view / Представление ученика
import src.controllers.StGroup as StGroup  # Group view / Представление группы

# ===== UI COMPONENT IMPORTS / ИМПОРТЫ КОМПОНЕНТОВ UI =====
from src.ui.MainMenu import MainMenu
from src.core.Logger import Logger


# ===== MAIN WINDOW CLASS / КЛАСС ГЛАВНОГО ОКНА =====
class MainWindow(QMainWindow):
    """
    Main application window class / Класс главного окна приложения
    Manages the primary user interface and coordinates application components / Управляет основным пользовательским интерфейсом и координирует компоненты приложения

    This class serves as the main container for the application's user interface.
    It manages the menu system, central widget display, window properties, and user interactions.
    Acts as the coordinator between different UI components and business logic.

    Этот класс служит основным контейнером для пользовательского интерфейса приложения.
    Он управляет системой меню, отображением центрального виджета, свойствами окна и взаимодействиями пользователя.
    Действует как координатор между различными компонентами UI и бизнес-логикой.
    """

    # ===== INITIALIZATION METHOD / МЕТОД ИНИЦИАЛИЗАЦИИ =====
    def __init__(self, parent=None):
        """
        Class constructor and main window setup / Конструктор класса и настройка главного окна

        Initializes the main window with all necessary components including menu system,
        central widget, window properties, and signal connections.
        Sets up logging and configures the primary user interface.

        Инициализирует главное окно со всеми необходимыми компонентами, включая систему меню,
        центральный виджет, свойства окна и подключения сигналов.
        Настраивает логирование и конфигурирует основной пользовательский интерфейс.

        Args:
            parent: Parent widget (typically None for main window) / Родительский виджет (обычно None для главного окна)
        """
        # ===== PARENT CLASS INITIALIZATION / ИНИЦИАЛИЗАЦИЯ РОДИТЕЛЬСКОГО КЛАССА =====
        super().__init__(parent)

        # ===== LOGGER INITIALIZATION / ИНИЦИАЛИЗАЦИЯ ЛОГЕРА =====
        self.lg = Logger()
        self.lg.debug("Constructor launched.")
        self.lg.debug("Logger created.")

        # ===== WINDOW CONFIGURATION / КОНФИГУРАЦИЯ ОКНА =====
        self._setup_window_properties()

        # ===== MENU SYSTEM SETUP / НАСТРОЙКА СИСТЕМЫ МЕНЮ =====
        self._setup_menu_system()

        # ===== SIGNAL CONNECTIONS / ПОДКЛЮЧЕНИЕ СИГНАЛОВ =====
        self._connect_menu_signals()

        self.lg.debug("Initialization completed successfully.")

    # ===== PRIVATE METHODS - INITIALIZATION HELPERS / ПРИВАТНЫЕ МЕТОДЫ - ПОМОЩНИКИ ИНИЦИАЛИЗАЦИИ =====

    def _setup_window_properties(self) -> None:
        """
        Configure main window properties / Настройка свойств главного окна

        Sets up window title, icon, and other display properties.
        Configures the basic appearance and behavior of the main window.

        Настраивает заголовок окна, иконку и другие свойства отображения.
        Конфигурирует основной внешний вид и поведение главного окна.
        """
        # ===== WINDOW TITLE / ЗАГОЛОВОК ОКНА =====
        self.setWindowTitle("Managing student assignments")

        # ===== WINDOW ICON SETUP / НАСТРОЙКА ИКОНКИ ОКНА =====
        # TODO: Add custom icon / TODO добавить свою иконку
        self._icon = QIcon()
        if self._icon.isNull():
            # Use system default computer icon if custom icon not available / Использовать системную иконку компьютера, если пользовательская недоступна
            self._icon = QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))
        self.setWindowIcon(self._icon)

        self.lg.debug("Window properties configured successfully.")

    def _setup_menu_system(self) -> None:
        """
        Initialize and configure the main menu system / Инициализация и настройка системы главного меню

        Creates the main menu bar with all necessary menu items.
        Sets up the hierarchical menu structure for the application.

        Создает главную строку меню со всеми необходимыми элементами меню.
        Настраивает иерархическую структуру меню для приложения.
        """
        # ===== MAIN MENU CREATION / СОЗДАНИЕ ГЛАВНОГО МЕНЮ =====
        # Parent=self sets parent window for main menu / Parent=self установка родительского окна для главного меню
        self.main_menu = MainMenu(parent=self)
        self.setMenuBar(self.main_menu)  # Set main menu for window / установка главного меню для окна

        self.lg.debug("Menu system configured successfully.")

    def _connect_menu_signals(self) -> None:
        """
        Connect menu actions to their respective handlers / Подключение действий меню к соответствующим обработчикам

        Establishes signal-slot connections between menu items and their functionality.
        Links user interface actions to business logic operations.

        Устанавливает связи сигнал-слот между элементами меню и их функциональностью.
        Связывает действия пользовательского интерфейса с операциями бизнес-логики.
        """
        # ===== TEACHER MENU CONNECTIONS / ПОДКЛЮЧЕНИЯ МЕНЮ УЧИТЕЛЯ =====
        self.main_menu.teacher_mode_request.connect(self.teacher_mode_on)

        # ===== STUDENT MENU CONNECTIONS / ПОДКЛЮЧЕНИЯ МЕНЮ УЧЕНИКА =====
        self.main_menu.student_mode_request.connect(self.student_mode_on)

        # ===== GROUP MENU CONNECTIONS / ПОДКЛЮЧЕНИЯ МЕНЮ ГРУППЫ =====
        self.main_menu.st_group_mode_request.connect(self.st_group_mode_on)

        # ===== HELP MENU CONNECTIONS / ПОДКЛЮЧЕНИЯ МЕНЮ ПОМОЩИ =====
        # Connect Help menu actions to information dialogs / Подключение действий меню помощи к информационным диалогам
        self.main_menu.about.triggered.connect(self.about)
        self.main_menu.about_qt.triggered.connect(self.about_qt)

        self.lg.debug("Menu signals connected successfully.")

    # ===== SLOT METHODS - MENU ACTION HANDLERS / МЕТОДЫ-СЛОТЫ - ОБРАБОТЧИКИ ДЕЙСТВИЙ МЕНЮ =====

    @pyqtSlot()
    def about(self) -> None:
        """
        Show information about the program / Показать информацию о программе

        Displays an "About" dialog with application information including version,
        description, and technology stack used.

        Отображает диалог "О программе" с информацией о приложении, включая версию,
        описание и используемый технологический стек.
        """
        QMessageBox.about(self, "About program",
                         "School management application\n"
                         "Приложение для управления школой\n\n"
                         "Version / Версия: 1.0\n"
                         "Built with PyQt6 and PostgreSQL\n"
                         "Создано с использованием PyQt6 и PostgreSQL\n\n"
                         "Features / Возможности:\n"
                         "• Teacher management / Управление учителями\n"
                         "• Student management / Управление учениками\n"  
                         "• Group management / Управление группами\n"
                         "• Database integration / Интеграция с базой данных")
        self.lg.debug("About program dialog shown.")

    @pyqtSlot()
    def about_qt(self) -> None:
        """
        Show information about Qt framework / Показать информацию о фреймворке Qt

        Displays the standard Qt "About Qt" dialog with information about
        the Qt framework version and licensing.

        Отображает стандартный диалог Qt "О Qt" с информацией о
        версии фреймворка Qt и лицензировании.
        """
        QMessageBox.aboutQt(self, "About Qt")
        self.lg.debug("About Qt dialog shown.")

    @pyqtSlot()
    def teacher_mode_on(self) -> None:
        old = self.centralWidget()
        v = Teacher.View(parent=self)
        self.setCentralWidget(v)
        self.menuBar().set_mode_teacher(v)
        if old is not None:
            old.deleteLater()

    @pyqtSlot()
    def student_mode_on(self) -> None:
        old = self.centralWidget()
        v = Student.View(parent=self)
        self.setCentralWidget(v)
        self.menuBar().set_mode_student(v)
        if old is not None:
            old.deleteLater()

    @pyqtSlot()
    def st_group_mode_on(self) -> None:
        old = self.centralWidget()
        v = StGroup.View(parent=self)
        self.setCentralWidget(v)
        self.menuBar().set_mode_st_group(v)
        if old is not None:
            old.deleteLater()


# ===== MAIN EXECUTION BLOCK - FOR TESTING / БЛОК ГЛАВНОГО ВЫПОЛНЕНИЯ - ДЛЯ ТЕСТИРОВАНИЯ =====
if __name__ == '__main__':
    # This block can be used for testing MainWindow functionality independently
    # Этот блок может использоваться для независимого тестирования функциональности MainWindow
    from PyQt6.QtWidgets import QApplication
    import sys

    print("=== MainWindow Testing Mode / Режим тестирования MainWindow ===")

    # Create test application / Создание тестового приложения
    app = QApplication(sys.argv)

    # Create and show main window / Создание и отображение главного окна
    window = MainWindow()
    window.showMaximized()

    print("MainWindow created and displayed successfully.")
    print("MainWindow создано и отображено успешно.")

    # Run application / Запуск приложения
    sys.exit(app.exec())