from assets.languages import en

LANGUAGES = {
    "en": en.STRINGS,
}

# Default language
CURRENT_LANGUAGE = "en"

def set_language(lang_code):
    global CURRENT_LANGUAGE
    if lang_code in LANGUAGES:
        CURRENT_LANGUAGE = lang_code
    else:
        print(f"Language '{lang_code}' not found. Falling back to English.")
        CURRENT_LANGUAGE = "en"

def T(path, default=""):
    keys = path.split(".")
    data = LANGUAGES.get(CURRENT_LANGUAGE, {})
    try:
        for key in keys:
            if key.isdigit():
                key = int(key)
            data = data[key]
        return data
    except (KeyError, IndexError, TypeError):
        return default