from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.spinner import MDSpinner
from kivy.lang import Builder
from kivy.animation import Animation
from utils.theme.colors import COLORS

class FMLoading(MDFloatLayout):

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.ids.spinner.color = COLORS["primary"]

    def on_touch_down(self, touch):
        if self.opacity == 0 or self.disabled:
            return False  # Let touch events pass through
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.opacity == 0 or self.disabled:
            return False
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.opacity == 0 or self.disabled:
            return False
        return super().on_touch_up(touch)

    def hide(self):
        self.disabled = True  # Disable interactions
        anim = Animation(opacity=0, duration=0.35)
        anim.start(self)

    def show(self):
        self.disabled = False
        anim = Animation(opacity=1, duration=0.05)
        anim.start(self)