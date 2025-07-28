from controllers.base_controller import BaseController
from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty

class LoginController(BaseController, EventDispatcher):

    submitting = BooleanProperty(False)

    def __init__(self, app):
        super().__init__(app)
        self.set_form("login")

    def login(self):

        def handle_response(response, error = False):
            self.submitting = False
            if error: return self.form_errors(response)
            if response.get("multi_factor_authentication"):
                self.app.storage.write("mfa.token", response['token'], file="auth.json")
                self.app.nav.go_to("mfa_send")
            else:
                self.app.auth.set_data(response)
                self.app.nav.go_to("portal")

        username = self.form_value("username")
        password = self.form_value("password")
        # Verifies the username and password exist
        if not username or not password:
            self.app.notifier.show("Username and password are required.", "danger")
        else:
            self.submitting = True
            response = self.app.api.request(
                "POST",
                "login",
                {"username": username, "password": password},
                callback=handle_response,
                require_auth=False
            )

    def on_leave(self, screen_name=None):
        self.form_item("username").text = ""
        self.form_item("password").text = ""