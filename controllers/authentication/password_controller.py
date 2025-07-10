class PasswordController:

    def __init__(self, app):
        self.app = app

    def forgot(self):
        print("Forgot called!")