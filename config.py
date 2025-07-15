from kivy.utils import platform

APP_NAME = "Cuztomisable"

APP_VERSION = "v1.0"

APP_LANGUAGE = "en"

DEBUG = True

DEVICE_TYPE = (
    "Android" if platform == "android"
    else "iOS" if platform == "ios"
    else "Other"
)

API_BASE_URL = "http://localhost:8000/api/"

HEADERS = {
    "X-App-Platform": "mobile",
    "User-Agent": f"{APP_NAME}/{APP_VERSION} ({DEVICE_TYPE})",
    "Accept": "application/json"
}
