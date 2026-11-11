import json
import os
from core.paths import SETTINGS_FILE
from core.locales.fa import FA

EN = {
    "main_menu": "MAIN MENU",
    "network": "Network Tools",
    "web": "Web Tools",
    "osint": "OSINT Tools",
    "wireless": "Wireless Tools",
    "crypto": "Crypto Tools",
    "forensics": "Forensics Tools",
    "custom": "Custom Tools",
    "settings": "Settings",
    "view_logs": "View Logs",
    "clear_logs": "Clear Logs",
    "exit": "Exit",
    "choose": "➤ Choose: ",
    "settings_menu": "SETTINGS",
    "change_lang": "Change Language",
    "change_theme": "Change Color Theme",
    "toggle_anim": "Toggle Animations",
    "back": "Back",
    "lang_set": "Language changed successfully.",
}

def get_current_lang():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                settings = json.load(f)
                return settings.get("language", "English")
        except Exception:
            pass
    return "English"

def t(key):
    lang = get_current_lang()
    if lang == "Persian (فارسی)":
        return FA.get(key, key)
    return EN.get(key, key)
