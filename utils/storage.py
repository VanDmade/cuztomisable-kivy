from kivy.storage.jsonstore import JsonStore

class StorageManager:

    def __init__(self, app):
        self.app = app
        self.default_file = "global.json"
        self.store = JsonStore(self.default_file)

    def _get_store(self, file=None):
        return JsonStore(file or self.default_file)

    def get(self, key, file=None):
        store = self._get_store(file)
        if store.exists(key):
            data = store.get(key)
            return data.get("__value__", data)
        return None

    def write(self, key, contents, file=None):
        store = self._get_store(file)
        if isinstance(contents, dict):
            store.put(key, **contents)
        else:
            store.put(key, __value__=contents)

    def delete(self, key, file=None):
        store = self._get_store(file)
        if store.exists(key):
            store.delete(key)

    def get_nested(self, key, subkey, file=None):
        data = self.get(key, file=file)
        return data.get(subkey) if isinstance(data, dict) else None