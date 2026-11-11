import os
import uuid
from datetime import datetime
from core.paths import REPORTS_DIR

def ensure_reports_dir():
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

def save_report(module_name, command, output):
    ensure_reports_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"{module_name}_{timestamp}_{uuid.uuid4().hex[:6]}.json"
    filepath = os.path.join(REPORTS_DIR, filename)
    
    report_data = {
        "module": module_name,
        "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "command": command,
        "output": output
    }
    
    with open(filepath, "w", encoding="utf-8") as f:
        import json
        json.dump(report_data, f, indent=4)
        
    return filename
