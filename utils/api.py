import requests
from utils.threading import executor
from concurrent.futures import ThreadPoolExecutor
from kivy.clock import Clock
from config import API_BASE_URL, HEADERS

executor = ThreadPoolExecutor(max_workers=4)

class ApiManager:

    def __init__(self, app):
        self.app = app

    def request(
        self,
        method,
        route,
        data=None,
        callback=None,
        retrying=False,
        require_auth=True
    ):
        def task():
            try:
                url = f"{API_BASE_URL}{route}"
                print(url)
                func = getattr(requests, method.lower(), None)
                if not func:
                    # Method is not supported
                    raise ValueError(f"Unsupported HTTP method: {method}")
                kwargs = {"headers": HEADERS}
                # Appends the JSON string to the post request
                if method.upper() == "POST":
                    kwargs["json"] = data
                response = func(url, **kwargs)
                if callback is None:
                    return response
                code = response.status_code
                res_data = response.json()
                def handle(*_):
                    if code != 200:
                        # The access token has expired and needs to be refreshed
                        if code == 401 and not retrying and require_auth:
                            def retry_callback(success):
                                if success:
                                    # Retry the original request
                                    self.request(method, route, data, callback, retrying=True, require_auth=require_auth)
                                else:
                                    # Token refresh failed, notify and redirect
                                    Clock.schedule_once(lambda *_: self.app.notifier.show("Session expired. Please log in again.", "danger"))
                            self.app.auth.refresh(callback=retry_callback)
                            return
                        # Checks for form error, errors will show beneath the fields
                        if code != 422:
                            # Default functionality when some error occurs
                            self.app.notifier.show(res_data.get('message', 'Something went wrong'), "danger")
                    if callback:
                        callback(res_data, False if code == 200 else True)
                Clock.schedule_once(handle)
            except requests.exceptions.RequestException as e:
                error_message = str(e)
                print(error_message)
                Clock.schedule_once(lambda *_: self.app.notifier.show(error_message, "danger"))
                if callback:
                    Clock.schedule_once(lambda *_: callback(False))
        executor.submit(task)