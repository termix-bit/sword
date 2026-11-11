import os
from core.ui import clear, draw_menu, print_info, print_error, module_loading
from core.logger import save_report
from core.executor import run_command
from core.validators import validate_file_path

def run(cmd_list):
    cmd_str = ' '.join(cmd_list) if isinstance(cmd_list, list) else cmd_list
    print_info(f"Running: {cmd_str}")
    print()
    code, output = run_command(cmd_list)
    print(output)
    if code != 0:
        print_error(f"Command failed (exit code: {code})")
    filename = save_report("Forensics", cmd_str, output)
    print_info(f"Report saved: {filename}")
    input("\nPress Enter to continue...")

def forensics_menu():
    module_loading("Forensics Tools")
    while True:
        clear()
        options = {
            "1": "Identify File Type (file)",
            "2": "Extract Strings (strings)",
            "3": "Extract Metadata (exiftool)",
            "4": "Hex Dump (xxd - first 320 bytes)",
            "0": "Back to Main Menu"
        }
        icons = {k: "»" for k in options}
        icons["0"] = "◀"
        
        draw_menu("FORENSICS TOOLS", options, icons)
        choice = input("➤ Choose: ")

        try:
            if choice == "1":
                filepath = validate_file_path(input("Enter full path to file: "))
                run(["file", filepath])
            elif choice == "2":
                filepath = validate_file_path(input("Enter full path to file: "))
                run(["strings", "-n", "6", filepath])
            elif choice == "3":
                filepath = validate_file_path(input("Enter full path to file: "))
                run(["exiftool", filepath])
            elif choice == "4":
                filepath = validate_file_path(input("Enter full path to file: "))
                run(["xxd", "-l", "320", filepath])
            elif choice == "0":
                break
            else:
                input("Wrong choice. Press Enter...")
        except (ValueError, OSError) as e:
            print_error(f"Invalid file: {e}")
            input("Press Enter...")
