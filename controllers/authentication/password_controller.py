from controllers.base_controller import BaseController
from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty

class PasswordController(BaseController, EventDispatcher):

    submitting = BooleanProperty(False)
\
    def __init__(self, app):
        super().__init__(app)
        self.token = ""
        self.code = ""

    def forgot(self):

        def handle_response(response, error = False):
            self.submitting = False
            if error: return
            self.app.notifier.show(response["message"], "success")
            # Sets the token for the process to continue. This will allow for ease of use
            self.token = response["token"]
            # Navigates the user to verify the code that was sent
            self.app.nav.go_to("password_verify")

        self.submitting = True
        self.set_form("password_forgot")
        response = self.app.api.request(
            "POST",
            "password/forgot",
            {"username": self.form("username")},
            callback=handle_response
        )

    def send(self):

        def handle_response(response, error = False):
            self.submitting = False
            if error: return
            self.app.notifier.show(response["message"], "success")

        self.submitting = True
        response = self.app.api.request(
            "GET",
            f"password/forgot/{self.token}/send",
            None,
            callback=handle_response
        )

    def verify(self):

        def handle_response(response, error = False):
            self.submitting = False
            if error: return
            self.app.notifier.show(response["message"], "success")
            # Navigates the user to the password reset
            self.app.nav.go_to("password_reset")

        self.submitting = True
        self.set_form("password_verify")
        code = self.form("code")
        response = self.app.api.request(
            "GET",
            f"password/forgot/{self.token}/verify/{code}",
            None,
            callback=handle_response
        )

    def reset(self):

        def handle_response(response, error = False):
            self.submitting = False
            if error: return
            self.app.notifier.show(response["message"], "success")
            # Navigates the user to the login page to login to the app
            self.app.nav.go_to("login")

        self.submitting = True
        self.set_form("password_reset")
        response = self.app.api.request(
            "POST",
            f"password/forgot/{self.token}",
            {"code": self.code, "password": self.form("password")},
            callback=handle_response
        )