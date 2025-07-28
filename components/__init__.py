import os
import importlib.util
from kivy.lang import Builder

def load_all_components(path="components"):
    loaded_modules = []
    for root, _, files in os.walk(path):
        for file in files:
            full_path = os.path.join(root, file)

            if file.endswith(".kv"):
                Builder.load_file(full_path)
            elif file.endswith(".py") and file != "__init__.py":
                module_name = (
                    full_path.replace("/", ".")
                    .replace("\\", ".")
                    .replace(".py", "")
                )
                spec = importlib.util.spec_from_file_location(module_name, full_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                loaded_modules.append(module_name)

    return loaded_modules

