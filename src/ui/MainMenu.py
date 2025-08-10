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
        self.add = teacher_menu.addAction("Add")          # Add action / Действие добавления
        self.update = teacher_menu.addAction("Update")    # Update action / Действие обновления
        self.delete = teacher_menu.addAction("Delete")    # Delete action / Действие удаления

        # Help menu / Меню помощи
        help_menu = self.addMenu("Help")
        self.about = help_menu.addAction("About program...")    # About program action / Действие "О программе"
        self.about_qt = help_menu.addAction("About qt...")      # About Qt action / Действие "О Qt"