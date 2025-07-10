import os
from kivy.lang import Builder

def load_all_views(path="views"):
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith("_screen.kv"):  # Optional filter to only load screen views
                kv_path = os.path.join(root, file)
                Builder.load_file(kv_path)