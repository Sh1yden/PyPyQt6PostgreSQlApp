from src.controllers.base_controller import BaseDialog

class Login(BaseDialog):

    def __init__(self, parent=None):
        super().__init__("Login", ["username", "password"], parent)