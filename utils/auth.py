from time import time
from kivy.storage.jsonstore import JsonStore

class AuthManager:

    def __init__(self, app):
        self.app = app
        self.store = JsonStore("auth.json")
        self.auth_key = "auth"

    def is_authenticated(self):
        return self.store.exists(self.auth_key) and self.get_access_token() is not None

    def get_access_token(self):
        return self.store.get(self.auth_key).get("access_token")

    def get_refresh_token(self):
        return self.store.get(self.auth_key).get("refresh_token")

    def get_user(self):
        return self.store.get(self.auth_key).get("user")

    def set_data(self, data):
        self.store.put(self.auth_key,
            access_token=data["access_token"],
            refresh_token=data["refresh_token"],
            expires_in=data["expires_in"],
            issued_at=time(),
            user=data["user"]
        )

    def logout(self):
        if self.store.exists(self.auth_key):
            self.store.delete(self.auth_key)

    def is_token_expired(self):
        if not self.store.exists(self.auth_key):
            return True
        auth = self.store.get(self.auth_key)
        return (time() - auth["issued_at"]) >= auth["expires_in"]

    def refresh_token(self):
        refresh_token = self.get_refresh_token()
        if not refresh_token:
            return False
        response = self.app.api.post("refresh", json={"refresh_token": refresh_token})
        if "access_token" in response:
            self.set_auth_data(response)
            return True
        return False