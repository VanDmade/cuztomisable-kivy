from kivy.utils import platform
import requests

class ApiManager:

    def __init__(self, app):
        self.app = app
        self.base_url = "http://localhost:8000/api/"
        device_type = "Android" if platform == "android" else "iOS" if platform == "ios" else "Other"
        self.headers = {
            "X-App-Platform": "mobile",
            "User-Agent": f"Cuztomisable/1.0 ({device_type})",
            "Accept": "application/json"
        }

    def post(self, route, json=None):
        try:
            return requests.post(
                f"{self.base_url}{route}",
                json=json,
                headers=self.headers
            )
        except requests.exceptions.HTTPError as e:
            self.app.notifier.show(response.reason, "danger")
        except requests.exceptions.RequestException as e:
            self.app.notifier.show(str(e), "danger")