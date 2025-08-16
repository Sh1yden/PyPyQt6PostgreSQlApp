# ===== MAIN MENU CLASS / КЛАСС ГЛАВНОГО МЕНЮ =====

# ===== IMPORTS / ИМПОРТЫ =====
# PyQt6 UI framework imports / Импорты фреймворка UI PyQt6
from PyQt6.QtWidgets import QMenuBar

# Local logging system import / Импорт локальной системы логирования
from src.core.Logger import Logger


# ===== MAIN MENU CLASS / КЛАСС ГЛАВНОГО МЕНЮ =====
class MainMenu(QMenuBar):
    """
    Main menu class for application navigation / Класс главного меню для навигации по приложению

    Creates and manages the complete menu structure including:
    Создает и управляет полной структурой меню, включая:
    - Entity management menus (Teacher, Student, Group) / Меню управления сущностями (Учитель, Студент, Группа)
    - CRUD operation actions / Действия CRUD операций
    - Help and information menus / Меню справки и информации
    """

    # ===== INITIALIZATION / ИНИЦИАЛИЗАЦИЯ =====
    def __init__(self, parent=None):
        """
        Initialize main menu with all navigation options / Инициализация главного меню со всеми опциями навигации

        Args:
            parent: Parent widget (usually MainWindow) / Родительский виджет (обычно MainWindow)
        """
        # Initialize parent QMenuBar class / Инициализация родительского класса QMenuBar
        super().__init__(parent)

        # ===== LOGGING SETUP / НАСТРОЙКА ЛОГИРОВАНИЯ =====
        # Initialize logger for menu operations / Инициализация логгера для операций меню
        self.lg = Logger()
        self.lg.debug("Constructor launched in class MainMenu.")
        self.lg.debug("Logger created in class MainMenu().")

        # ===== MENU STRUCTURE CREATION / СОЗДАНИЕ СТРУКТУРЫ МЕНЮ =====
        # Create all menu sections in logical order / Создание всех секций меню в логическом порядке
        self._create_teacher_menu()
        self._create_student_menu()
        self._create_group_menu()
        self._create_help_menu()

    # ===== TEACHER MENU SECTION / СЕКЦИЯ МЕНЮ УЧИТЕЛЯ =====
    def _create_teacher_menu(self):
        """Create teacher management menu with CRUD operations / Создание меню управления учителями с CRUD операциями"""
        # Create main teacher menu / Создание основного меню учителя
        teacher_menu = self.addMenu("Teacher")

        # Add CRUD operation actions / Добавление действий CRUD операций
        self.teacher_add = teacher_menu.addAction("Add")          # Add new teacher / Добавить нового учителя
        self.teacher_update = teacher_menu.addAction("Update")    # Update existing teacher / Обновить существующего учителя
        self.teacher_delete = teacher_menu.addAction("Delete")    # Delete selected teacher / Удалить выбранного учителя

        self.lg.debug("MainMenu teacher_menu add successfully. In DEF _create_teacher_menu().")

    # ===== STUDENT MENU SECTION / СЕКЦИЯ МЕНЮ СТУДЕНТА =====
    def _create_student_menu(self):
        """Create student management menu with CRUD operations / Создание меню управления студентами с CRUD операциями"""
        # Create main student menu / Создание основного меню студента
        student_menu = self.addMenu("Student")

        # Add CRUD operation actions / Добавление действий CRUD операций
        self.student_add = student_menu.addAction("Add")          # Add new student / Добавить нового студента
        self.student_update = student_menu.addAction("Update")    # Update existing student / Обновить существующего студента
        self.student_delete = student_menu.addAction("Delete")    # Delete selected student / Удалить выбранного студента

        self.lg.debug("MainMenu student_menu add successfully. In DEF _create_student_menu().")

    # ===== GROUP MENU SECTION / СЕКЦИЯ МЕНЮ ГРУППЫ =====
    def _create_group_menu(self):
        """Create group management menu with CRUD operations / Создание меню управления группами с CRUD операциями"""
        # Create main group menu / Создание основного меню группы
        st_group_menu = self.addMenu("Group")

        # Add CRUD operation actions / Добавление действий CRUD операций
        self.st_group_add = st_group_menu.addAction("Add")          # Add new group / Добавить новую группу
        self.st_group_update = st_group_menu.addAction("Update")    # Update existing group / Обновить существующую группу
        self.st_group_delete = st_group_menu.addAction("Delete")    # Delete selected group / Удалить выбранную группу

        self.lg.debug("MainMenu st_group_menu add successfully. In DEF _create_group_menu().")

    # ===== HELP MENU SECTION / СЕКЦИЯ МЕНЮ СПРАВКИ =====
    def _create_help_menu(self):
        """Create help and information menu / Создание меню справки и информации"""
        # Create main help menu / Создание основного меню справки
        help_menu = self.addMenu("Help")

        # Add information actions / Добавление информационных действий
        self.about = help_menu.addAction("About program...")    # Show program information / Показать информацию о программе
        self.about_qt = help_menu.addAction("About qt...")      # Show Qt framework information / Показать информацию о фреймворке Qt

        self.lg.debug("MainMenu help_menu add successfully. In DEF _create_help_menu().")