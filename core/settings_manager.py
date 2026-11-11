from core.paths import SETTINGS_FILE
import json
import os

def get_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "language": "English",
        "animations": True,
        "proxy": "",
        "safe_mode": False
    }

def animations_enabled():
    settings = get_settings()
    return settings.get("animations", True)
