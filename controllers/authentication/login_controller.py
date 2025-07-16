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
            if error:
                if "errors" in response:
                    for key, value in response["errors"].items():
                        if self.item(key) is not None:
                            self.item(key).set_error(value[0])
                return
            if response.get("multi_factor_authentication"):
                self.app.nav.go_to("mfa")
            else:
                self.app.auth.set_data(response)
                self.app.nav.go_to("portal")

        username = self.form("username")
        password = self.form("password")
        # Verifies the username and password exist
        if not username or not password:
            self.app.notifier.show("Username and password are required.", "danger")
        else:
            self.submitting = True
            response = self.app.api.request(
                "POST",
                "login",
                {"username": username, "password": password},
                callback=handle_response
            )