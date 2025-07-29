from PyQt6.QtWidgets import QMenuBar


class MainMenu(QMenuBar):

    def __init__(self, parent=None):
        super().__init__(parent)

        teacher_menu = self.addMenu("Teacher")
        self.add = teacher_menu.addAction("Add")
        self.update = teacher_menu.addAction("Update")
        self.delete = teacher_menu.addAction("Delete")

        help_menu = self.addMenu("Help")
        self.about = help_menu.addAction("About program...")
        self.about_qt = help_menu.addAction("About qt...")

        # TODO нужно чтобы внутренние переменные экземпляра класса были закрытыми, но пока что это не важно.
        # self.__about = help_menu.addAction("About program...")

    # TODO
    # @property
    # def about(self):
    #     return self.__about
