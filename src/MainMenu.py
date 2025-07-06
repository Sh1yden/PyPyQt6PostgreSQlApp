from PyQt6.QtWidgets import QMenuBar


class MainMenu(QMenuBar):

    def __init__(self, parent=None):
        super().__init__(parent)

        help_menu = self.addMenu("Help")
        self.about = help_menu.addAction("About program...")

        # нужно чтобы внутренние переменные экземпляра класса были закрытыми,
        # но пока что это не важно
        # self.__about = help_menu.addAction("About program...")
        self.about_qt = help_menu.addAction("About qt...")

    # @property
    # def about(self):
    #     return self.__about
