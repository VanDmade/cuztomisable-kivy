from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty, ListProperty
from kivy.animation import Animation
from utils.theme.colors import COLORS

class FMNavigation(MDBoxLayout):

    color = StringProperty("primary")
    dropup_color = ListProperty([0.25, 0.25, 0.25, 1])

    def on_kv_post(self, base_widget):
        self.dropup_color = COLORS.get(self.color, COLORS["primary"])

    def toggle_dropup(self):
        dropup = self.ids.get("navigation_dropup")
        if not dropup:
            return
        if dropup.height == 0:
            Animation(height=200, opacity=1, duration=0.25, t="out_quad").start(dropup)
        else:
            Animation(height=0, opacity=0, duration=0.2, t="in_quad").start(dropup)