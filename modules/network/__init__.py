import os
import subprocess
import json
from core.ui import clear, draw_menu, print_warning, print_info, print_success, print_error, module_loading
from core.logger import save_report
from core.executor import run_command
from core.validators import validate_ip, validate_subnet, validate_port

def run(cmd_list, module_name="Network"):
    cmd_str = ' '.join(cmd_list) if isinstance(cmd_list, list) else cmd_list
    print_info(f"Running: {cmd_str}")
    print()
    code, output = run_command(cmd_list)
    print(output)
    if code != 0:
        print_error(f"Command failed (exit code: {code})")
    filename = save_report(module_name, cmd_str, output)
    print_success(f"Report saved: {filename}")
    input("\nPress Enter to continue...")

def run_with_warning(cmd_list, warning_msg):
    print_warning(warning_msg)
    print("If your device is not rooted, this will fail.\n")
    confirm = input("Continue? (y/n): ")
    if confirm.lower() == "y":
        run(cmd_list)
    else:
        print("Cancelled.")
        input("Press Enter...")

def network_menu():
    module_loading("Network Tools")
    while True:
        clear()
        options = {
            "1": "Scan Network (nmap -sn)",
            "2": "Scan Ports (nmap -sV)",
            "3": "Aggressive Scan (nmap -A)",
            "4": "Full Port Scan (nmap -p-) (Root Required) ⚠️",
            "5": "OS Detection (nmap -O) (Root Required) ⚠️",
            "6": "Ping Host",
            "7": "Traceroute",
            "8": "My IP",
            "9": "DNS Lookup (dig)",
            "10": "hping3 (Custom Packets) (Root Required) ⚠️",
            "11": "RustScan (Fast Port Scan)",
            "0": "Back to Main Menu"
        }
        icons = {k: "»" for k in options}
        icons["0"] = "◀"
        
        draw_menu("NETWORK TOOLS", options, icons)
        choice = input("➤ Choose: ")

        try:
            if choice == "1":
                net = validate_subnet(input("Network (e.g. 192.168.1.0/24): "))
                run(["nmap", "-sn", net])
            elif choice == "2":
                ip = validate_ip(input("IP: "))
                run(["nmap", "-sV", ip])
            elif choice == "3":
                ip = validate_ip(input("IP: "))
                run(["nmap", "-A", ip])
            elif choice == "4":
                ip = validate_ip(input("IP: "))
                run_with_warning(["nmap", "-p-", ip], "Full port scan requires ROOT.")
            elif choice == "5":
                ip = validate_ip(input("IP: "))
                run_with_warning(["nmap", "-O", ip], "OS Detection requires ROOT.")
            elif choice == "6":
                target = input("IP or domain: ")
                run(["ping", "-c", "4", target])
            elif choice == "7":
                target = input("IP or domain: ")
                run(["traceroute", target])
            elif choice == "8":
                print_info("Fetching your IP address...")
                try:
                    result = subprocess.check_output(["termux-wifi-connectioninfo"], stderr=subprocess.STDOUT, timeout=10)
                    info = json.loads(result.decode())
                    if isinstance(info, list) and len(info) > 0:
                        info = info[0]
                    if isinstance(info, dict) and "error" in info:
                        print_error(f"API Error: {info['error']}")
                    else:
                        ip = info.get('ip') or info.get('IP') or 'Unknown'
                        ssid = info.get('SSID') or info.get('ssid') or 'Unknown'
                        output = f"SSID: {ssid}\nIP: {ip}"
                        print_success(output)
                        filename = save_report("Network_MyIP", "termux-wifi-connectioninfo", output)
                        print_success(f"Report saved: {filename}")
                except subprocess.TimeoutExpired:
                    print_error("Termux API timed out.")
                except Exception as e:
                    print_error(f"Error: {e}")
                input("\nPress Enter to continue...")
            elif choice == "9":
                domain = input("Domain: ")
                run(["dig", domain, "+short"])
            elif choice == "10":
                ip = validate_ip(input("Target IP: "))
                port = validate_port(input("Port: "))
                run_with_warning(["hping3", "-S", "-p", port, "-c", "5", ip], "hping3 requires ROOT.")
            elif choice == "11":
                ip = validate_ip(input("IP: "))
                run(["rustscan", "-a", ip])
            elif choice == "0":
                break
            else:
                input("Wrong choice. Press Enter...")
        except ValueError as e:
            print_error(f"Invalid input: {e}")
            input("Press Enter...")
