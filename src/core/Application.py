from PyQt6.QtWidgets import QApplication
from src.database.Connection import Connection
from src.core.Logger import Logger


class Application(QApplication):

    def __init__(self, argv):
        super().__init__(argv)
        self.lg = Logger()
        self.lg.debug("Logger created at Application.")

        self.con = Connection(lg=self.lg)
        self.lg.debug("self.con created")

