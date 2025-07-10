class NavigationManager:

    def __init__(self, screen_manager):
        self.sm = screen_manager

    def go_to(self, screen_name):
        if self.sm.has_screen(screen_name):
            self.sm.current = screen_name
        else:
            print(f"Screen '{screen_name}' not found.")