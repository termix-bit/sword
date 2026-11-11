import os
import sys
import subprocess
from pathlib import Path

from core.ui import clear, draw_menu, print_info, print_error, module_loading
from core.logger import save_report

SCRIPTS_DIR = (Path(__file__).resolve().parents[2] / "custom_scripts")

def get_custom_scripts():
    if not SCRIPTS_DIR.exists():
        SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    scripts = [f.name for f in SCRIPTS_DIR.glob("*.py")]
    return scripts

def custom_menu():
    module_loading("Custom Tools")
    while True:
        clear()
        scripts = get_custom_scripts()
        options = {}
        icons = {}
        if not scripts:
            options["1"] = "No scripts found in 'custom_scripts' folder"
            icons["1"] = "X"
        else:
            for index, script in enumerate(scripts, 1):
                options[str(index)] = script
                icons[str(index)] = "»"
        options["0"] = "Back to Main Menu"
        icons["0"] = "◀"
       
        draw_menu("CUSTOM TOOLS (Plugins)", options, icons)
       
        if not scripts:
            input("Create a .py file inside ~/sword/custom_scripts to see it here.\nPress Enter...")
            break

           
        choice = input("➤ Choose: ")

        if choice == "0":
            break
        elif choice.isdigit() and 1 <= int(choice) <= len(scripts):
            script_name = scripts[int(choice) - 1]
            script_path = (SCRIPTS_DIR / script_name).resolve()
           
            if script_path.suffix != ".py" or script_path.parent != SCRIPTS_DIR.resolve() or not script_path.is_file():
                print_error("Invalid plugin path!")

                input("Press Enter...")
                continue
               
            print_info(f"Executing {script_name}...")
            print()
           
            try:
                result = subprocess.run(
                    [sys.executable, str(script_path)],
                    shell=False,
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                output = result.stdout + result.stderr
                print(output)
               
                filename = save_report("Custom_Script", f"Script: {script_name}", output)

                print_info(f"Report saved: {filename}")
            except subprocess.TimeoutExpired:
                print_error("Script timed out (120 seconds).")
            except Exception as e:
                print_error(f"Error executing script: {e}")

               
            input("\nPress Enter to continue...")
        else:
            input("Wrong choice. Press Enter...")
