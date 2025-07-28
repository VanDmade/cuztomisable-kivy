from controllers.base_controller import BaseController
from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty

class PasswordController(BaseController, EventDispatcher):

    submitting = BooleanProperty(False)
    # List of screens that can be reset within this controller
    screens = ["password_forgot", "password_verify", "password_reset"]

    def __init__(self, app):
        super().__init__(app)
        self._token = None
        self._code = None

    def forgot(self):

        def handle_response(response, error = False):
            self.submitting = False
            if error: return self.form_errors(response)
            self.app.notifier.show(response["message"], "success")
            # Sets the token for the process to continue. This will allow for ease of use
            self._token = response["token"]
            # Stores the token just incase it was somehow lost
            self.app.storage.write("token", self._token, file="auth.json")
            # Navigates the user to verify the code that was sent
            self.app.nav.go_to("password_verify")

        self.submitting = True
        self.set_form("password_forgot")
        response = self.app.api.request(
            "POST",
            "password/forgot",
            {"username": self.form_value("username")},
            callback=handle_response,
            require_auth=False
        )

    def send(self):

        def handle_response(response, error = False):
            self.submitting = False
            if error: return self.form_errors(response)
            self.app.notifier.show(response["message"], "success")

        self.submitting = True
        response = self.app.api.request(
            "GET",
            f"password/forgot/{self.get_token()}/send",
            None,
            callback=handle_response,
            require_auth=False
        )

    def verify(self):

        def handle_response(response, error = False):
            self.submitting = False
            if error: return self.form_errors(response)
            self.app.notifier.show(response["message"], "success")
            # Navigates the user to the password reset
            self.app.nav.go_to("password_reset")

        self.set_form("password_verify")
        code = self.form_value("code")
        if not code:
            self.app.notifier.show("The code is required.", "danger")
        else:
            self._code = self.form_value("code")
            self.submitting = True
            response = self.app.api.request(
                "GET",
                f"password/forgot/{self.get_token()}/verify/{self.get_code()}",
                None,
                callback=handle_response,
                require_auth=False
            )

    def reset(self):

        def handle_response(response, error = False):
            self.submitting = False
            if error: return self.form_errors(response)
            # Removes the token/codes
            self.app.storage.delete("token", "auth.json")
            self.app.storage.delete("code", "auth.json")
            self._token = None
            self._code = None
            self.app.notifier.show(response["message"], "success")
            # Navigates the user to the login page to login to the app
            self.app.nav.go_to("login")

        self.submitting = True
        self.set_form("password_reset")
        response = self.app.api.request(
            "POST",
            f"password/forgot/{self.get_token()}",
            {"code": self.get_code(), "password": self.form_value("reset_password")},
            callback=handle_response,
            require_auth=False
        )

    def get_token(self):
        if not self._token:
            self._token = self.app.storage.get("token", file="auth.json")
        return self._token

    def get_code(self):
        if not self._code:
            self._code = self.app.storage.get("code", file="auth.json")
        return self._code

    def on_leave(self, screen_name=None):
        self.set_form(screen_name)
        if not screen_name or screen_name == "password_forgot":
            self.form_item("username").text = ""
        elif screen_name == "password_reset":
            self.form_item("reset_password").text = ""
        else:
            self.form_item("code").text = ""