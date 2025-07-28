import requests
from utils.threading import executor
from time import time
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
from config import API_BASE_URL, HEADERS

class AuthManager:

    def __init__(self, app):
        self.app = app
        self.store = JsonStore("auth.json")
        self.auth_key = "auth"

    def is_authenticated(self):
        if self.store.exists(self.auth_key) is False:
            return False
        return self.store.exists(self.auth_key) and self.get_access_token() is not None

    def get_access_token(self):
        if self.store.exists(self.auth_key) is False:
            return False
        return self.store.get(self.auth_key).get("access_token")

    def get_refresh_token(self):
        if self.store.exists(self.auth_key) is False:
            return False
        return self.store.get(self.auth_key).get("refresh_token")

    def get_user(self):
        if self.store.exists(self.auth_key is False):
            return False
        return self.store.get(self.auth_key).get("user")

    def set_data(self, data):
        payload = {
            "access_token": data["access_token"],
            "expires_in": data["expires_in"],
            "issued_at": time(),
        }
        payload["user"] = data.get("user") or self.get_user()
        payload["refresh_token"] = data.get("refresh_token") or self.get_refresh_token()
        self.store.put(self.auth_key, **payload)

    def logout(self):
        if self.store.exists(self.auth_key):
            self.store.delete(self.auth_key)
        current_screen = self.app.nav.sm.current
        self.app.loading.hide()
        self.app.notifier.show("Session expired. Please log in again.", "danger")
        if current_screen != "login":
            self.app.nav.go_to("login")
        else:
            controller = self.app.controllers.authentication.login
            if controller:
                controller.submitting = False

    def is_token_expired(self):
        if self.store.exists(self.auth_key) is False:
            return True
        auth = self.store.get(self.auth_key)
        return (time() - auth["issued_at"]) >= auth["expires_in"]

    def refresh(self, callback=None):
        def _refresh_task():
            # Background work here
            success = False
            try:
                # Tries to refresh the token
                response = requests.post(
                    f"{API_BASE_URL}refresh/token",
                    headers=HEADERS,
                    json={"token": self.get_refresh_token()}
                )
                if response.status_code == 200:
                    self.set_data(response.json())
                    success = True
            except Exception as e:
                print("Refresh failed:", e)
            def done_callback(*_):
                # The refresh could not occur
                if not success:
                    self.logout()
                if callback: callback(success)
            # Schedule UI-safe callback
            Clock.schedule_once(done_callback)
        executor.submit(_refresh_task)