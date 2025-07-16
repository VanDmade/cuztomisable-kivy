class BaseController:

    def __init__(self, app):
        self.app = app
        self.screen_name = None

    def set_form(self, screen_name):
        self.screen_name = screen_name

    def form(self, name, default = None):
        if not self.screen_name:
            raise ValueError(self.app.T("global.errors.no_screen"))
        # Gets the ids from the specific screen for the form
        ids = self.app.root.ids.screen_manager.get_screen(self.screen_name).ids
        try:
            return ids[name].text.strip()
        except (KeyError, AttributeError):
            return default

    def item(self, name):
        try:
            ids = self.app.root.ids.screen_manager.get_screen(self.screen_name).ids
            return ids[name]
        except (KeyError, AttributeError):
            return None