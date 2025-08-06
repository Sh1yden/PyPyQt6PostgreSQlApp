from PyQt6.QtWidgets import QMenuBar
from src.core.Logger import Logger


class MainMenu(QMenuBar):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Инициализация логера.
        self.lg = Logger()
        self.lg.debug("Constructor launched in class MainMenu.")
        self.lg.debug("Logger created in class MainMenu().")

        teacher_menu = self.addMenu("Teacher")
        self.add = teacher_menu.addAction("Add")
        self.update = teacher_menu.addAction("Update")
        self.delete = teacher_menu.addAction("Delete")

        help_menu = self.addMenu("Help")
        self.about = help_menu.addAction("About program...")
        self.about_qt = help_menu.addAction("About qt...")
