from kivymd.uix.textfield import MDTextField
from kivy.properties import StringProperty, BooleanProperty
from kivy.clock import Clock
from utils.theme.colors import COLORS

class FMTextField(MDTextField):

    label = StringProperty("")
    is_password = BooleanProperty(False)
    color_name = StringProperty("primary")
    form_key = StringProperty("")
    mask = StringProperty("")
    backspace_pressed = False
    disabled = BooleanProperty(False)
    error_text = StringProperty("")
    has_error = BooleanProperty(False)
    helper_mode = StringProperty("on_focus")

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        color = COLORS.get(self.color_name, COLORS["primary"])
        self.line_color_focus = color
        self.hint_text_color_focus = color
        self.helper_text_color_normal = COLORS["danger"]
        self.helper_text_color_focus = COLORS["danger"]
        if self.mask:
            self.bind(text=self._apply_mask)

    def _apply_mask(self, instance, value):
        # Prevent recursion
        self.unbind(text=self._apply_mask)
        # Keep only digits
        digits = ''.join(filter(str.isdigit, value))
        new_text = ''
        digit_index = 0
        # Makes it so that masked chars are skipped and erased with the numbers
        skip_mask_chars = self.backspace_pressed
        text_len = len(self.text)
        # Prevents leaving the first non-digit in the string
        if not digits:
            self.text = ''
            self.bind(text=self._apply_mask)
            return
        # Iterates through the mask to allow for the replacing of the # characters
        for i, char in enumerate(self.mask):
            if char == '#':
                if digit_index < len(digits):
                    new_text += digits[digit_index]
                    digit_index += 1
                else:
                    break
            else:
                # Only skip mask chars at the end of the old text when backspacing
                if skip_mask_chars and i >= len(self.text) - 1:
                    continue
                new_text += char
        # Only update if changed
        if self.text != new_text:
            self.text = new_text
        # This allows for the cursor to be placed in the correct spot, otherwise it will not move correctly
        Clock.schedule_once(lambda dt: setattr(self, 'cursor', (len(new_text), 0)), 0)
        self.bind(text=self._apply_mask)

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if keycode[1] == 'backspace':
            self.backspace_pressed = True
        else:
            self.backspace_pressed = False
        return super().keyboard_on_key_down(window, keycode, text, modifiers)

    def set_error(self, message):
        self.error_text = message
        self.has_error = True
        self.helper_mode = "persistent"

    def clear_error(self):
        self.error_text = ""
        self.has_error = False
        self.helper_mode = "on_focus"

    def on_text(self, *args):
        if self.has_error:
            self.clear_error()