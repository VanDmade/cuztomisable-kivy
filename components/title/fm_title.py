from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import BooleanProperty, StringProperty

class FMTitle(MDBoxLayout):

    use_logo = BooleanProperty(True)
    title = StringProperty("Welcome")
    subtitle = StringProperty("Please log in to continue")
    title_style = StringProperty("H5")
    subtitle_style = StringProperty("Subtitle1")