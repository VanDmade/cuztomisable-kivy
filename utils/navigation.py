from types import SimpleNamespace
from utils.helpers import resolve_controller
from kivy.clock import Clock

class NavigationManager:

    def __init__(self, app, screen_manager, controller_map):
        self.app = app
        self.sm = screen_manager
        self.controller_map = controller_map

    def go_to(self, screen_name):
        # Call on_leave on current controller
        current = self.get_current_controller()
        if current and hasattr(current, "on_leave"):
            current_screen = self.sm.current
            Clock.schedule_once(lambda dt: current.on_leave(current_screen), 0.25)
        # Switch screen
        if not self.sm.has_screen(screen_name):
            print(f"Screen '{screen_name}' not found.")
            return
        self.sm.current = screen_name
        # Call on_pre_enter on new controller
        new = self.get_controller(screen_name)
        if new and hasattr(new, "on_pre_enter"):
            new.on_pre_enter(screen_name)

    def get_current_controller(self):
        return self.get_controller(self.sm.current)

    def get_controller(self, screen_name):
        path = self.controller_map.get(screen_name)
        return resolve_controller(self.app.controllers, path) if path else None