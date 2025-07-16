import requests
from concurrent.futures import ThreadPoolExecutor
from kivy.clock import Clock
from config import API_BASE_URL, HEADERS

executor = ThreadPoolExecutor(max_workers=4)

class ApiManager:

    def __init__(self, app):
        self.app = app

    def request(self, method, route, data=None, callback=None):
        def task():
            try:
                url = f"{API_BASE_URL}{route}"
                func = getattr(requests, method.lower(), None)
                if not func:
                    # Method is not supported
                    raise ValueError(f"Unsupported HTTP method: {method}")
                kwargs = {"headers": HEADERS}
                # Appends the JSON string to the post request
                if method.upper() == "POST":
                    kwargs["json"] = data
                response = func(url, **kwargs)
                code = response.status_code
                res_data = response.json()
                def handle(*_):
                    if code != 200:
                        # Checks for form error, errors will show beneath the fields
                        if code != 422:
                            # Default functionality when some error occurs
                            self.app.notifier.show(res_data.get('message', 'Something went wrong'), "danger")
                        if callback:
                            callback(res_data, True)
                    else:
                        if callback:
                            callback(res_data, False)
                Clock.schedule_once(handle)
            except requests.exceptions.RequestException as e:
                Clock.schedule_once(lambda *_: self.app.notifier.show(str(e), "danger"))
                if callback:
                    Clock.schedule_once(lambda *_: callback(False))
        executor.submit(task)