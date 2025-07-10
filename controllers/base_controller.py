class BaseController:

    def __init__(self, app):
        self.app = app
        self.screen_name = None

    def set_form(self, screen_name):
        self.screen_name = screen_name

    def form(self, name, screen_name=None):
        screen = screen_name or self.screen_name
        if not screen:
            raise ValueError(self.app.T("global.errors.no_screen"))
        # Gets the ids from the specific screen for the form
        ids = self.app.root.ids.screen_manager.get_screen(screen).ids
        try:
            return ids[name].text.strip()
        except (KeyError, AttributeError):
            return ""