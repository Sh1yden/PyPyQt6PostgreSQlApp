from PyQt6.QtWidgets import QApplication
from src.database.Connection import Connection
from src.core.Logger import Logger


class Application(QApplication):

    def __init__(self, argv):
        # Инициализация логера.
        self.lg = Logger()
        self.lg.debug("Constructor launched in class Application.")
        self.lg.debug("Logger created in class Application().")

        super().__init__(argv)
        self.con = Connection()

