from kivymd.uix.button import MDTextButton
from kivy.properties import ObjectProperty, StringProperty
from utils.theme.colors import COLORS
import webbrowser

class FMLink(MDTextButton):

    text_value = StringProperty("Click here")
    url = StringProperty("")
    on_click = ObjectProperty(None, allownone=True)
    target_screen = StringProperty("")
    color_name = StringProperty("link")
    halign = StringProperty("left")

    def on_kv_post(self, base_widget):
        # Set the text color using your custom theme
        self.text_color = COLORS.get(self.color_name, COLORS["link"])

    def on_release(self):
        if self.on_click:
            self.on_click()
        elif self.target_screen:
            from kivy.app import App
            App.get_running_app().nav.go_to(self.target_screen)
        elif self.url:
            webbrowser.open(self.url)