from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.uix.screenmanager import ScreenManager, NoTransition
from components import load_all_components
from controllers import load_all_controllers
from views import load_all_views
from utils.api import ApiManager
from utils.auth import AuthManager
from utils.navigation import NavigationManager
from utils.storage import StorageManager
from assets.languages import T
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

Window.size = (360, 640)

class MyApp(MDApp):

    def build(self):
        load_all_components()
        load_all_views()
        self.T = T
        self.controllers, self.controller_map = load_all_controllers(self)
        # Load main app.kv which contains ScreenManager
        root = Builder.load_file("app.kv")
        self.nav = NavigationManager(self, root.ids.screen_manager, self.controller_map)
        self.notifier = root.ids.notifier
        self.api = ApiManager(self)
        self.auth = AuthManager(self)
        self.storage = StorageManager(self)
        self.loading = root.ids.global_loading
        # Verifies if the user is logged in or not
        Clock.schedule_once(self.check_auth_and_navigate, 0)
        return root;

    def check_auth_and_navigate(self, *args):

        def handle_response(response):
            self.nav.go_to("login" if not response else "portal")
            Clock.schedule_once(lambda dt: self.loading.hide(), 0.25)

        if self.auth.is_authenticated():
            if self.auth.is_token_expired():
                # Refreshes the token to make sure everything is good to go
                self.auth.refresh(callback=handle_response)
                return
            self.nav.go_to("portal")
        else:
            self.nav.go_to("login")
        # Displays the app so that there is no jumping when navigating
        Clock.schedule_once(lambda dt: self.loading.hide(), 2)

MyApp().run()