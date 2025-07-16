from controllers.base_controller import BaseController
from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty

class RegistrationController(BaseController, EventDispatcher):

    submitting = BooleanProperty(False)

    def __init__(self, app):
        super().__init__(app)

    def register(self):

        def handle_response(response, error = False):
            self.submitting = False
            if error:
                print(response)
                if "errors" in response:
                    for key, value in response["errors"].items():
                        if self.item(key) is not None:
                            self.item(key).set_error(value[0])
                return
            self.app.notifier.show(response["message"], "success")
            # Navigates the user to the password reset
            self.app.nav.go_to("login")

        self.submitting = True
        self.set_form("registration")
        response = self.app.api.request(
            "POST",
            "register",
            {
                "name": self.form("name"),
                "email": self.form("email"),
                "password": self.form("password"),
                "phone": self.item("phone").ids.number.text,
                "country_code": self.form("country_code", "+1").replace("+", "")
            },
            callback=handle_response
        )
