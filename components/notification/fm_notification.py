from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty, BooleanProperty, ListProperty, NumericProperty
from kivy.clock import Clock
from kivy.animation import Animation
from utils.theme.colors import COLORS

class FMNotification(MDBoxLayout):

    text = StringProperty("Message")
    visible = BooleanProperty(False)
    auto_dismiss = BooleanProperty(True)
    duration = NumericProperty(3)
    color_name = StringProperty("primary")
    background_color = ListProperty([0.1, 0.1, 0.1, 0.9])
    _dismiss_event = None

    def on_kv_post(self, base_widget):
        if self.color_name in COLORS:
            self.background_color = COLORS[self.color_name]

    def show(self, message, color_name=None):
        self.text = message
        if color_name and color_name in COLORS:
            self.background_color = COLORS[color_name]
        # Gets the total words in the message and then calculates how long the message should stay
        word_count = len(message.split())
        self.duration = word_count * 0.75
        self.opacity = 0
        self.visible = True
        Animation.cancel_all(self)
        Animation(opacity=1, d=0.3).start(self)
        # Cancel any previous scheduled hide
        if self._dismiss_event:
            self._dismiss_event.cancel()
        if self.auto_dismiss:
            self._dismiss_event = Clock.schedule_once(lambda *args: self.hide(), self.duration)

    def hide(self):
        Animation.cancel_all(self)
        def finish(*_):
            self.visible = False
        anim = Animation(opacity=0, d=0.3)
        anim.bind(on_complete=finish)
        anim.start(self)
