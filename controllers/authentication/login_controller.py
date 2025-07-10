from controllers.base_controller import BaseController

class LoginController(BaseController):

    def __init__(self, app):
        self.app = app
        self.set_form("login")

    def login(self):
        username = self.form("username")
        password = self.form("password")
        if not username or not password:
            self.app.notifier.show("Username and password are required.", "danger")
            return
        response = self.app.api.post("login", {"username": username, "password": password})
        code = response.status_code
        response = response.json()
        if code != 200:
            self.app.notifier.show(response['message'], "danger")
            return
        # Checks to see if the user needs to be sent to MFA or if they can be logged in
        if response['multi_factor_authentication'] == True:
            # Redirect the user to the MFA page
            self.app.nav.go_to('mfa')
        else:
            self.app.auth.set_data(response);
            # Redirect the user to the portal
            self.app.nav.go_to('portal')