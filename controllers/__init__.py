import os
import importlib.util
import inspect
from types import SimpleNamespace

def dict_to_namespace(d):
    return SimpleNamespace(**{
        k: dict_to_namespace(v) if isinstance(v, dict) else v
        for k, v in d.items()
    })

def load_all_controllers(app, root_path="controllers"):
    controller_tree = {}

    for dirpath, _, filenames in os.walk(root_path):
        for file in filenames:
            if not file.endswith("_controller.py"):
                continue

            module_path = os.path.join(dirpath, file)
            module_name = (
                module_path.replace("/", ".")
                .replace("\\", ".")
                .replace(".py", "")
            )

            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            for name, obj in inspect.getmembers(module, inspect.isclass):
                if name.endswith("Controller"):
                    instance = obj(app)

                    # Build nested keys: e.g., authentication.login
                    rel_path = os.path.relpath(module_path, root_path).replace("\\", "/")
                    parts = rel_path.split("/")[:-1]  # ['authentication']
                    controller_name = name.replace("Controller", "").lower()  # 'login'
                    parts.append(controller_name)

                    ref = controller_tree
                    for part in parts[:-1]:
                        ref = ref.setdefault(part, {})
                    ref[parts[-1]] = instance

    return dict_to_namespace(controller_tree)