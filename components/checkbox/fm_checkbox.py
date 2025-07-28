from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty, BooleanProperty
from utils.theme.colors import COLORS

class FMCheckbox(MDBoxLayout):

    text = StringProperty("Option")
    active = BooleanProperty(False)

    def on_kv_post(self, base_widget):
        checkbox = self.ids.checkbox
        checkbox.color_active = COLORS.get("secondary")

    def on_checkbox_active(self, checkbox, value):
        self.active = value