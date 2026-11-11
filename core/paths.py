from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
HOME = Path.home()
SETTINGS_FILE = PROJECT_DIR / "core" / "settings.json"
REPORTS_DIR = PROJECT_DIR / "reports"
CUSTOM_SCRIPTS_DIR = PROJECT_DIR / "custom_scripts"
SQLMAP_PATH = HOME / "sqlmap"
WHATWEB_PATH = HOME / "WhatWeb"
