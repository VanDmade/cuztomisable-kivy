import os
import importlib.util
from kivy.lang import Builder

def load_all_components(path="components"):
    for root, _, files in os.walk(path):
        for file in files:
            full_path = os.path.join(root, file)

            # Load .kv files
            if file.endswith(".kv"):
                Builder.load_file(full_path)

            # Import .py files
            elif file.endswith(".py") and file != "__init__.py":
                module_name = (
                    full_path.replace("/", ".")
                    .replace("\\", ".")   # Windows support
                    .replace(".py", "")
                )

                spec = importlib.util.spec_from_file_location(module_name, full_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
