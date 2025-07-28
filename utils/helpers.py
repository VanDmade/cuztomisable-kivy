from types import SimpleNamespace

def rgba_to_hex(rgba):
    if not rgba:
        return "FFFFFF"  # default to white if invalid
    r, g, b = [int(x * 255) for x in rgba[:3]]
    return f"{r:02X}{g:02X}{b:02X}"

def resolve_controller(controllers, path):
    if not path:
        return None
    ref = controllers
    for part in path.split("."):
        if isinstance(ref, dict):
            ref = ref.get(part)
        elif isinstance(ref, SimpleNamespace):
            ref = getattr(ref, part, None)
        else:
            return None
    return ref