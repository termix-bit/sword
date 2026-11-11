import os
import json
import subprocess
import time
from pathlib import Path
from rich.text import Text
from core.ui import clear, draw_menu, print_info, print_error, print_success, module_loading, console
from core.paths import REPORTS_DIR
from core.report_server import open_html_report

def get_reports():
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)
    reports = [f for f in os.listdir(REPORTS_DIR) if f.endswith(".json")]
    return sorted(reports, reverse=True)

def delete_all_reports():
    json_reports = [f for f in os.listdir(REPORTS_DIR) if f.endswith(".json")]
    html_reports = [f for f in os.listdir(REPORTS_DIR) if f.endswith(".html")]
    
    if not json_reports and not html_reports:
        print_error("No reports to delete.")
        input("Press Enter...")
        return
        
    confirm = input("Are you sure you want to DELETE ALL reports (JSON & HTML)? (y/n): ")
    if confirm.lower() == "y":
        report_dir = Path(REPORTS_DIR).resolve()
        for path in report_dir.iterdir():
            if path.suffix.lower() not in (".json", ".html"):
                continue
            resolved = path.resolve()
            if resolved.parent == report_dir and resolved.is_file():
                resolved.unlink()
        print_success("All reports (JSON & HTML) deleted.")
    else:
        print("Cancelled.")
    input("Press Enter...")

def delete_single_report(report_name):
    confirm = input(f"Delete '{report_name}'? (y/n): ")
    if confirm.lower() == "y":
        filepath = os.path.join(REPORTS_DIR, report_name)
        html_path = filepath.replace(".json", ".html")
        
        if os.path.exists(filepath): os.remove(filepath)
        if os.path.exists(html_path): os.remove(html_path)
        
        print_success(f"Report '{report_name}' deleted.")
    else:
        print("Cancelled.")
    input("Press Enter...")

def generate_html(report_name, report_data):
    from html import escape
    safe_module = escape(str(report_data.get('module', '')))
    safe_date = escape(str(report_data.get('date', '')))
    safe_command = escape(str(report_data.get('command', '')))
    safe_output = escape(str(report_data.get('output', '')))

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sword Security Report - {safe_module}</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #121212; color: #e0e0e0; padding: 30px; margin: 0; }}
        .container {{ max-width: 900px; margin: auto; background-color: #1e1e1e; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }}
        h1 {{ color: #00e5ff; border-bottom: 2px solid #00e5ff; padding-bottom: 10px; text-align: center; }}
        .meta {{ display: flex; justify-content: space-between; background-color: #2d2d2d; padding: 15px; border-radius: 8px; margin-bottom: 20px; font-size: 0.9em; }}
        .meta span {{ color: #bb86fc; font-weight: bold; }}
        .output {{ background-color: #000000; padding: 20px; border-radius: 8px; white-space: pre-wrap; font-family: 'Courier New', Courier, monospace; color: #4caf50; border-left: 4px solid #4caf50; overflow-x: auto; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>⚔️ Sword Security Report</h1>
        <div class="meta">
            <div><span>Module:</span> {safe_module}</div>
            <div><span>Date:</span> {safe_date}</div>
        </div>
        <div style="margin-bottom: 10px;"><span style="color: #bb86fc; font-weight: bold;">Command:</span> {safe_command}</div>
        <h3>Output:</h3>
        <div class="output">{safe_output}</div>
    </div>
</body>
</html>
    """
    html_filename = report_name.replace(".json", ".html")
    html_filepath = os.path.join(REPORTS_DIR, html_filename)
    
    with open(html_filepath, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    return html_filepath

def reports_menu():
    module_loading("Reports")
    while True:
        clear()
        reports = get_reports()
        
        options = {}
        icons = {}
        
        if not reports:
            options["1"] = "No reports found."
            icons["1"] = "X"
        else:
            for index, report in enumerate(reports, 1):
                options[str(index)] = report
                icons[str(index)] = "»"
        
        options["D"] = "Delete ALL reports"
        icons["D"] = "X"
        
        options["0"] = "Back to Main Menu"
        icons["0"] = "◀"
        
        draw_menu("SAVED REPORTS", options, icons)
        
        if not reports:
            input("Run a scan from any module to generate a report.\nPress Enter...")
            break
            
        choice = input("➤ Choose: ").upper()

        if choice == "0":
            break
        elif choice == "D":
            delete_all_reports()
        elif choice.isdigit() and 1 <= int(choice) <= len(reports):
            report_name = reports[int(choice) - 1]
            report_path = os.path.join(REPORTS_DIR, report_name)
            
            clear()
            print_info(f"Viewing: {report_name}\n")
            try:
                with open(report_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    
                console.print("[bold cyan]Module:[/bold cyan]")
                console.print(Text(str(data.get("module", ""))))
                console.print("[bold cyan]Date:[/bold cyan]")
                console.print(Text(str(data.get("date", ""))))
                console.print("[bold cyan]Command:[/bold cyan]")
                console.print(Text(str(data.get("command", ""))))
                console.print("\n[bold green]Output:[/bold green]")
                console.print(Text(str(data.get("output", ""))))
                
                print("\n[1] Open as HTML in Browser")
                print("[2] Delete this report")
                print("[0] Back")
                action = input("➤ Choose: ")
                
                if action == "1":
                    print_info("Generating HTML and opening in browser...")
                    html_path = generate_html(report_name, data)
                    open_html_report(html_path)
                    print_success("HTML Report opened!")
                    input("Press Enter...")
                elif action == "2":
                    delete_single_report(report_name)
                    
            except Exception as e:
                print_error(f"Error reading report: {e}")
                input("\nPress Enter...")
        else:
            input("Wrong choice. Press Enter...")
