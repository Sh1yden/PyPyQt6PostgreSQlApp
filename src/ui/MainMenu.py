# ===== MAIN MENU CLASS / КЛАСС ГЛАВНОГО МЕНЮ =====

# ===== IMPORTS / ИМПОРТЫ =====
from PyQt6.QtWidgets import QMenuBar
from src.core.Logger import Logger


# ===== MAIN MENU CLASS / КЛАСС ГЛАВНОГО МЕНЮ =====
class MainMenu(QMenuBar):
    """
    Main menu class for application / Класс главного меню для приложения
    Creates and manages application menu structure / Создает и управляет структурой меню приложения
    """

    # ===== INITIALIZATION / ИНИЦИАЛИЗАЦИЯ =====
    def __init__(self, parent=None):
        """
        Initialize main menu / Инициализация главного меню
        
        Args:
            parent: Parent widget / Родительский виджет
        """
        super().__init__(parent)

        # ===== LOGGER INITIALIZATION / ИНИЦИАЛИЗАЦИЯ ЛОГГЕРА =====
        self.lg = Logger()
        self.lg.debug("Constructor launched in class MainMenu.")
        self.lg.debug("Logger created in class MainMenu().")

        # ===== MENU CREATION / СОЗДАНИЕ МЕНЮ =====
        # Teacher menu / Меню учителя
        teacher_menu = self.addMenu("Teacher")
        self.teacher_add = teacher_menu.addAction("Add")          # Add action / Действие добавления
        self.teacher_update = teacher_menu.addAction("Update")    # Update action / Действие обновления
        self.teacher_delete = teacher_menu.addAction("Delete")    # Delete action / Действие удаления

        self.lg.debug("MainMenu teacher_menu add successfully. In DEF __init__().")

        # Student menu / Меню ученика
        student_menu = self.addMenu("Student")
        self.student_add = student_menu.addAction("Add")          # Add action / Действие добавления
        self.student_update = student_menu.addAction("Update")    # Update action / Действие обновления
        self.student_delete = student_menu.addAction("Delete")    # Delete action / Действие удаления

        self.lg.debug("MainMenu student_menu add successfully. In DEF __init__().")

        # Group menu / Меню группы
        st_group_menu = self.addMenu("Group")
        self.st_group_add = st_group_menu.addAction("Add")          # Add action / Действие добавления
        self.st_group_update = st_group_menu.addAction("Update")    # Update action / Действие обновления
        self.st_group_delete = st_group_menu.addAction("Delete")    # Delete action / Действие удаления

        self.lg.debug("MainMenu st_group_menu add successfully. In DEF __init__().")

        # Help menu / Меню помощи
        help_menu = self.addMenu("Help")
        self.about = help_menu.addAction("About program...")    # About program action / Действие "О программе"
        self.about_qt = help_menu.addAction("About qt...")      # About Qt action / Действие "О Qt"

        self.lg.debug("MainMenu help_menu add successfully. In DEF __init__().")