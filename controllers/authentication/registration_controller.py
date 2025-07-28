from controllers.base_controller import BaseController
from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty

class RegistrationController(BaseController, EventDispatcher):

    submitting = BooleanProperty(False)

    def __init__(self, app):
        super().__init__(app)
        self.set_form("registration")

    def register(self):

        def handle_response(response, error = False):
            self.submitting = False
            if error: return self.form_errors(response)
            self.app.notifier.show(response["message"], "success")
            # Navigates the user to the password reset
            self.app.nav.go_to("login")

        self.submitting = True
        response = self.app.api.request(
            "POST",
            "register",
            {
                "name": self.form_value("name"),
                "email": self.form_value("email"),
                "password": self.form_value("password"),
                "phone": self.form_item("phone").ids.number.text,
                "country_code": self.form_value("country_code", "+1").replace("+", "")
            },
            callback=handle_response,
            require_auth=False
        )

    def on_leave(self, screen_name=None):
        self.form_item("name").text = ""
        self.form_item("email").text = ""
        self.form_item("password").text = ""
        self.form_item("phone").ids.number.text = ""
        country_code = self.form_item("country_code")
        if country_code is not None:
            country_code.text = "+1"
        # Moves the user back to the top of the screen
        scroll = self.form_item("registration_scroll_view")
        if scroll:
            scroll.scroll_y = 1
