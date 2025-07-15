from controllers.base_controller import BaseController
from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty

class RegistrationController(BaseController, EventDispatcher):

    submitting = BooleanProperty(False)

    def __init__(self, app):
        super().__init__(app)

    def register(self):

        def handle_response(response):
            self.submitting = False

        self.submitting = True
        self.set_form("registration")
