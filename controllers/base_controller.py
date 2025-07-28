class BaseController:

    screen_name = None

    def __init__(self, app):
        self.app = app
        self.screen_name = None

    def set_form(self, screen_name):
        self.screen_name = screen_name

    def form_value(self, name, default = None):
        if not self.screen_name:
            raise ValueError(self.app.T("global.errors.no_screen"))
        # Gets the ids from the specific screen for the form
        ids = self.app.root.ids.screen_manager.get_screen(self.screen_name).ids
        try:
            return ids[name].text.strip()
        except (KeyError, AttributeError):
            return default

    def form_item(self, name):
        try:
            ids = self.app.root.ids.screen_manager.get_screen(self.screen_name).ids
            return ids[name]
        except (KeyError, AttributeError):
            return None

    def form_errors(self, response):
        try:
            if "errors" not in response: return True
            # Iterates through the errors to output them to the form
            for key, value in response["errors"].items():
                if self.form_item(key) is not None:
                    self.form_item(key).set_error(value[0])
            return True
        except (KeyError, AttributeError):
            return False

    def on_pre_enter(self, screen_name=None):
        # Called before a screen is shown
        pass

    def on_leave(self, screen_name=None):
        # Called when leaving a screen
        pass