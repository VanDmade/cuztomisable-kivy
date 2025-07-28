from controllers.base_controller import BaseController
from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty

class MfaController(BaseController, EventDispatcher):

    submitting = BooleanProperty(False)
    # List of screens that can be reset within this controller
    screens = ["mfa_send", "mfa_verify"]

    def __init__(self, app):
        super().__init__(app)
        self._token = None

    def on_pre_enter(self, screen_name=None):
        if screen_name == "mfa_send":
            self.verify()

    def send(self, type=None):

        def handle_response(response, error = False):
            self.submitting = False
            self.app.loading.hide()
            if error:
                # The code couldn't be sent for some reason and there is nothing the user can do unless logging in again
                self.app.nav.go_to("login")
                return
            self.app.notifier.show(response["message"], "success")
            self.app.nav.go_to("mfa_verify")

        self.submitting = True
        self.set_form("mfa_send")
        # Gets the type if the user has more than one option and it isn't sent in
        if type is None:
            type = "email" if self.form_item("email_checkbox").active else "phone"

        response = self.app.api.request(
            "POST",
            f"login/mfa/{self.get_token()}/send",
            { "type": type },
            callback=handle_response,
            require_auth=False
        )

    def verify(self):

        def handle_response(response, error = False):
            self.submitting = False
            if error:
                # The token was not verified and now needs to be retried
                self.app.nav.go_to("login")
                return
            if response["email"] is None or response["phone"] is None:
                if response["phone"] is None:
                    self.send("email")
                else:
                    self.send("phone")
                self.app.nav.go_to("mfa_verify")
            else:
                self.app.loading.hide()
                self.app.notifier.show(response["message"], "success")
                self.form_item("email_checkbox").ids.label.text = response["email"]
                self.form_item("phone_checkbox").ids.label.text = response["phone"]

        self.submitting = True
        self.set_form("mfa_send")
        self.app.loading.show()
        response = self.app.api.request(
            "GET",
            f"login/mfa/{self.get_token()}/verify",
            callback=handle_response,
            require_auth=False
        )

    def save(self):

        def handle_response(response, error = False):
            self.submitting = False
            if error: return self.form_errors(response)
            self.app.storage.delete("mfa.token", "auth.json")
            self.app.notifier.show(response["message"], "success")
            self.app.nav.go_to("portal")

        self.submitting = True
        self.set_form("mfa_verify")
        code = self.form_value("code")
        remember = 1 if self.form_item("remember").active else 0
        response = self.app.api.request(
            "POST",
            f"login/mfa/{self.get_token()}",
            {"code": code, "remember": remember},
            callback=handle_response,
            require_auth=False
        )

    def get_token(self):
        if not self._token:
            self._token = self.app.storage.get("mfa.token", file="auth.json")
        return self._token

    def on_leave(self, screen_name=None):
        self.set_form(screen_name)
        if not screen_name or screen_name == "mfa_send":
            self.form_item("email_checkbox").active = True
            self.form_item("phone_checkbox").active = False
        else:
            self.form_item("code").text = ""