from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty
from utils.theme.colors import COLORS
from utils.helpers import rgba_to_hex
import re

class PasswordRequirements(BoxLayout):

    password = StringProperty("")
    is_valid = BooleanProperty(False)
    length_text = StringProperty("")
    upper_text = StringProperty("")
    lower_text = StringProperty("")
    number_text = StringProperty("")
    special_text = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_requirements(self.password)

    def on_kv_post(self, base_widget):
        self.update_requirements(self.password)

    def on_password(self, instance, value):
        self.update_requirements(value)

    def update_requirements(self, value):
        length_ok = len(value) >= 8
        upper_ok = bool(re.search(r"[A-Z]", value))
        lower_ok = bool(re.search(r"[a-z]", value))
        number_ok = bool(re.search(r"[0-9]", value))
        special_ok = bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", value))
        self.is_valid = all([length_ok, upper_ok, lower_ok, number_ok, special_ok])
        # Update label texts
        self.length_text = self._format(length_ok, "At least 8 characters")
        self.upper_text = self._format(upper_ok, "At least 1 uppercase letter")
        self.lower_text = self._format(lower_ok, "At least 1 lowercase letter")
        self.number_text = self._format(number_ok, "At least 1 number")
        self.special_text = self._format(special_ok, "At least 1 special character")

    def _format(self, passed, text):
        color = rgba_to_hex(COLORS.get("success") if passed else COLORS.get("danger"))
        return f"[color={color}]{text}[/color]"

    def reset(self):
        self.password = ""
        self.is_valid = False
        self.length_text = self._format(False, "At least 8 characters")
        self.upper_text = self._format(False, "At least 1 uppercase letter")
        self.lower_text = self._format(False, "At least 1 lowercase letter")
        self.number_text = self._format(False, "At least 1 number")
        self.special_text = self._format(False, "At least 1 special character")