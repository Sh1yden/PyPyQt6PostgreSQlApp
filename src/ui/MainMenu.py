# ===== MAIN MENU CLASS / КЛАСС ГЛАВНОГО МЕНЮ =====
from PyQt6.QtCore import pyqtSlot, pyqtSignal
from PyQt6.QtGui import QActionGroup

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

    teacher_mode_request = pyqtSignal()
    student_mode_request = pyqtSignal()
    st_group_mode_request = pyqtSignal()

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
        self.lg.debug("Constructor launched.")
        self.lg.debug("Logger created.")

        # ===== MENU STRUCTURE CREATION / СОЗДАНИЕ СТРУКТУРЫ МЕНЮ =====
        # Create all menu sections in logical order / Создание всех секций меню в логическом порядке
        self._create_teacher_menu()
        self._create_student_menu()
        self._create_group_menu()
        self._create_mod_menu()
        self.set_mode_default()
        self._create_help_menu()

    # ===== TEACHER MENU SECTION / СЕКЦИЯ МЕНЮ УЧИТЕЛЯ =====
    def _create_teacher_menu(self) -> None:
        """Create teacher management menu with CRUD operations / Создание меню управления учителями с CRUD операциями"""
        # Create main teacher menu / Создание основного меню учителя
        teacher_menu = self.addMenu("Teacher")
        self.__teacher_menu_action = teacher_menu.menuAction()

        # Add CRUD operation actions / Добавление действий CRUD операций
        self.__teacher_add = teacher_menu.addAction(
            "Add"
        )  # Add new teacher / Добавить нового учителя
        self.__teacher_update = teacher_menu.addAction(
            "Update"
        )  # Update existing teacher / Обновить существующего учителя
        self.__teacher_delete = teacher_menu.addAction(
            "Delete"
        )  # Delete selected teacher / Удалить выбранного учителя

        self.lg.debug("Teacher_menu add successfully.")

    # ===== STUDENT MENU SECTION / СЕКЦИЯ МЕНЮ СТУДЕНТА =====
    def _create_student_menu(self) -> None:
        """Create student management menu with CRUD operations / Создание меню управления студентами с CRUD операциями"""
        # Create main student menu / Создание основного меню студента
        student_menu = self.addMenu("Student")
        self.__student_menu_action = student_menu.menuAction()

        # Add CRUD operation actions / Добавление действий CRUD операций
        self.__student_add = student_menu.addAction(
            "Add"
        )  # Add new student / Добавить нового студента
        self.__student_update = student_menu.addAction(
            "Update"
        )  # Update existing student / Обновить существующего студента
        self.__student_delete = student_menu.addAction(
            "Delete"
        )  # Delete selected student / Удалить выбранного студента

        self.lg.debug("Student_menu add successfully.")

    # ===== GROUP MENU SECTION / СЕКЦИЯ МЕНЮ ГРУППЫ =====
    def _create_group_menu(self) -> None:
        """Create group management menu with CRUD operations / Создание меню управления группами с CRUD операциями"""
        # Create main group menu / Создание основного меню группы
        st_group_menu = self.addMenu("Group")
        self.__st_group_menu_action = st_group_menu.menuAction()

        # Add CRUD operation actions / Добавление действий CRUD операций
        self.__st_group_add = st_group_menu.addAction(
            "Add"
        )  # Add new group / Добавить новую группу
        self.__st_group_update = st_group_menu.addAction(
            "Update"
        )  # Update existing group / Обновить существующую группу
        self.__st_group_delete = st_group_menu.addAction(
            "Delete"
        )  # Delete selected group / Удалить выбранную группу

        self.lg.debug("St_group_menu add successfully.")

    def _create_mod_menu(self) -> None:
        mode_menu = menu = self.addMenu("Mods")
        mode_action_group = ag = QActionGroup(self)

        self.__teacher_mod = tm = menu.addAction("Teacher Mod")
        tm.setCheckable(True)
        tm.toggled.connect(self.toggle_teacher_mode)
        ag.addAction(tm)

        self.__student_mod = sm = menu.addAction("Student Mod")
        sm.setCheckable(True)
        sm.toggled.connect(self.toggle_student_mode)
        ag.addAction(sm)

        self._st_group_mod = sgm = menu.addAction("StGroup Mod")
        sgm.setCheckable(True)
        sgm.toggled.connect(self.toggle_st_group_mode)
        ag.addAction(sgm)

    # ===== HELP MENU SECTION / СЕКЦИЯ МЕНЮ СПРАВКИ =====
    def _create_help_menu(self) -> None:
        """Create help and information menu / Создание меню справки и информации"""
        # Create main help menu / Создание основного меню справки
        help_menu = self.addMenu("Help")

        # Add information actions / Добавление информационных действий
        self.__about = help_menu.addAction(
            "About program..."
        )  # Show program information / Показать информацию о программе
        self.__about_qt = help_menu.addAction(
            "About qt..."
        )  # Show Qt framework information / Показать информацию о фреймворке Qt

        self.lg.debug("Help_menu add successfully.")

    # property's
    @property
    def about(self):
        return self.__about

    @property
    def about_qt(self):
        return self.__about_qt

    @pyqtSlot(bool)
    def toggle_teacher_mode(self, enable):
        self.lg.debug(f"Teacher = {enable}")
        if not enable:
            self.lg.debug("Teacher set False")
            self.__teacher_menu_action.setEnabled(False)
            self.__teacher_menu_action.setVisible(False)
            self.__teacher_add.setEnabled(False)
            self.__teacher_update.setEnabled(False)
            self.__teacher_delete.setEnabled(False)
        else:
            self.lg.debug("Teacher emit")
            self.teacher_mode_request.emit()

    @pyqtSlot(bool)
    def toggle_student_mode(self, enable):
        self.lg.debug(f"Student = {enable}")
        if not enable:
            self.__student_menu_action.setEnabled(False)
            self.__student_menu_action.setVisible(False)
            self.__student_add.setEnabled(False)
            self.__student_update.setEnabled(False)
            self.__student_delete.setEnabled(False)
        else:
            self.student_mode_request.emit()

    @pyqtSlot(bool)
    def toggle_st_group_mode(self, enable):
        self.lg.debug(f"StGroup = {enable}")
        if not enable:
            self.__st_group_menu_action.setEnabled(False)
            self.__st_group_menu_action.setVisible(False)
            self.__st_group_add.setEnabled(False)
            self.__st_group_update.setEnabled(False)
            self.__st_group_delete.setEnabled(False)
        else:
            self.st_group_mode_request.emit()

    # mods
    def set_mode_default(self) -> None:
        self.__teacher_menu_action.setEnabled(False)
        self.__teacher_menu_action.setVisible(False)
        self.__teacher_add.setEnabled(False)
        self.__teacher_update.setEnabled(False)
        self.__teacher_delete.setEnabled(False)

        self.__student_menu_action.setEnabled(False)
        self.__student_menu_action.setVisible(False)
        self.__student_add.setEnabled(False)
        self.__student_update.setEnabled(False)
        self.__student_delete.setEnabled(False)

        self.__st_group_menu_action.setEnabled(False)
        self.__st_group_menu_action.setVisible(False)
        self.__st_group_add.setEnabled(False)
        self.__st_group_update.setEnabled(False)
        self.__st_group_delete.setEnabled(False)

        self.lg.debug("Set DEFAULT mode success.")

    def set_mode_teacher(self, widget) -> None:
        self.__teacher_add.triggered.connect(widget.add)
        self.__teacher_update.triggered.connect(widget.uppdate)
        self.__teacher_delete.triggered.connect(widget.delete)

        self.__teacher_menu_action.setEnabled(True)
        self.__teacher_menu_action.setVisible(True)
        self.__teacher_add.setEnabled(True)
        self.__teacher_update.setEnabled(True)
        self.__teacher_delete.setEnabled(True)

        self.__student_menu_action.setEnabled(False)
        self.__student_menu_action.setVisible(False)
        self.__student_add.setEnabled(False)
        self.__student_update.setEnabled(False)
        self.__student_delete.setEnabled(False)

        self.__st_group_menu_action.setEnabled(False)
        self.__st_group_menu_action.setVisible(False)
        self.__st_group_add.setEnabled(False)
        self.__st_group_update.setEnabled(False)
        self.__st_group_delete.setEnabled(False)

        self.lg.debug("Set mode success.")

    def set_mode_student(self, widget) -> None:
        self.__student_add.triggered.connect(widget.add)
        self.__student_update.triggered.connect(widget.uppdate)
        self.__student_delete.triggered.connect(widget.delete)

        self.__teacher_menu_action.setEnabled(False)
        self.__teacher_menu_action.setVisible(False)
        self.__teacher_add.setEnabled(False)
        self.__teacher_update.setEnabled(False)
        self.__teacher_delete.setEnabled(False)

        self.__student_menu_action.setEnabled(True)
        self.__student_menu_action.setVisible(True)
        self.__student_add.setEnabled(True)
        self.__student_update.setEnabled(True)
        self.__student_delete.setEnabled(True)

        self.__st_group_menu_action.setEnabled(False)
        self.__st_group_menu_action.setVisible(False)
        self.__st_group_add.setEnabled(False)
        self.__st_group_update.setEnabled(False)
        self.__st_group_delete.setEnabled(False)

        self.lg.debug("Set mode success.")

    def set_mode_st_group(self, widget) -> None:
        self.__st_group_add.triggered.connect(widget.add)
        self.__st_group_update.triggered.connect(widget.uppdate)
        self.__st_group_delete.triggered.connect(widget.delete)

        self.__teacher_menu_action.setEnabled(False)
        self.__teacher_menu_action.setVisible(False)
        self.__teacher_add.setEnabled(False)
        self.__teacher_update.setEnabled(False)
        self.__teacher_delete.setEnabled(False)

        self.__student_menu_action.setEnabled(False)
        self.__student_menu_action.setVisible(False)
        self.__student_add.setEnabled(False)
        self.__student_update.setEnabled(False)
        self.__student_delete.setEnabled(False)

        self.__st_group_menu_action.setEnabled(True)
        self.__st_group_menu_action.setVisible(True)
        self.__st_group_add.setEnabled(True)
        self.__st_group_update.setEnabled(True)
        self.__st_group_delete.setEnabled(True)

        self.lg.debug("Set mode success.")
