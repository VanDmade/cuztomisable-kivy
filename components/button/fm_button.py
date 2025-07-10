from kivymd.uix.button import MDRaisedButton
from kivy.properties import StringProperty, ListProperty, NumericProperty, ObjectProperty
from utils.theme.colors import COLORS

class FMButton(MDRaisedButton):

    label = StringProperty("Button")
    color_name = StringProperty("primary")
    font_size_sp = NumericProperty(18)
    on_press_callback = ObjectProperty(None)

    def on_kv_post(self, base_widget):
        self.md_bg_color = COLORS.get(self.color_name, COLORS["primary"])