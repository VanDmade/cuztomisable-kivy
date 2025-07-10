from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.utils import get_color_from_hex
from kivy.uix.screenmanager import ScreenManager
from components import load_all_components
from controllers import load_all_controllers
from views import load_all_views
from utils.api import ApiManager
from utils.auth import AuthManager
from utils.navigation import NavigationManager
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
        self.controllers = load_all_controllers(self)
        # Load main app.kv which contains ScreenManager
        root = Builder.load_file("app.kv")
        self.api = ApiManager(root)
        self.auth = AuthManager(root)
        self.nav = NavigationManager(root.ids.screen_manager)
        self.notifier = root.ids.notifier
        return root;

MyApp().run()