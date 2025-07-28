from kivymd.uix.button import MDTextButton
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy.clock import Clock
from utils.theme.colors import COLORS
import webbrowser

class FMLink(MDTextButton):

    text_value = StringProperty("Click here")
    url = StringProperty("")
    callback = ObjectProperty(None, allownone=True)
    target_screen = StringProperty("")
    color_name = StringProperty("link")
    halign = StringProperty("left")
    is_loading = BooleanProperty(False)
    loading_text = StringProperty("Loading...")

    def on_kv_post(self, base_widget):
        # Set the text color using your custom theme
        self.text_color = COLORS.get(self.color_name, COLORS["link"])

    def on_release(self):
        if self.is_loading:
            return
        if self.callback:
            self.text = self.loading_text
            self.disabled = True
            self.is_loading = True
            self.callback()
        else:
            if self.target_screen:
                from kivy.app import App
                App.get_running_app().nav.go_to(self.target_screen)
            elif self.url:
                webbrowser.open(self.url)