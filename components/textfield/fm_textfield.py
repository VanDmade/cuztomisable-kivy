from kivymd.uix.textfield import MDTextField
from kivy.properties import StringProperty, BooleanProperty
from utils.theme.colors import COLORS

class FMTextField(MDTextField):

    label = StringProperty("Label")
    is_password = BooleanProperty(False)
    color_name = StringProperty("primary")
    form_key = StringProperty("")

    def on_kv_post(self, base_widget):
        color = COLORS.get(self.color_name, COLORS["primary"])
        self.line_color_focus = color
        self.hint_text_color_focus = color