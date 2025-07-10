from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty, BooleanProperty

class FMSeparator(MDBoxLayout):

    label = StringProperty("")
    show_label = BooleanProperty(False)

    def on_label(self, instance, value):
        self.show_label = bool(value.strip())