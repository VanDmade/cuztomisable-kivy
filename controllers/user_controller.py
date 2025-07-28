from controllers.base_controller import BaseController
from kivy.event import EventDispatcher

class UserController(BaseController, EventDispatcher):

    def __init__(self, app):
        self.app = app