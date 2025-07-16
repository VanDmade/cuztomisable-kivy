from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty
from kivymd.uix.menu import MDDropdownMenu
from utils.theme.colors import COLORS

class FMPhone(BoxLayout):

    label = StringProperty("Number")
    default_code = StringProperty("+1")
    show_country_code = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu = None

    def show_country_menu(self):
        if not self.menu:
            self.menu = MDDropdownMenu(
                caller=self.ids.country_code,
                items=[
                    {"text": "(+1) USA", "on_release": lambda: self.set_country_code("+1")},
                ],
                width_mult=4,
            )
        self.menu.open()

    def set_country_code(self, code):
        self.ids.country_code.text = code
        self.menu.dismiss()

    def set_error(self, error):
        self.ids.phone_error.text_color = COLORS["danger"]
        self.ids.phone_error.text = error

    def clear_errors(self):
        self.ids.phone_error.text = ""
