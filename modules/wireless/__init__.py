import os
import subprocess
import json
from core.ui import clear, draw_menu, print_info, print_warning, print_error, module_loading

from core.logger import save_report
from core.executor import run_command

def run(cmd_list):
    cmd_str = ' '.join(cmd_list) if isinstance(cmd_list, list) else cmd_list
    print_info(f"Running: {cmd_str}")
    print()
    code, output = run_command(cmd_list)
    print(output)
    filename = save_report("Wireless", cmd_str, output)

    print_info(f"Report saved: {filename}")
    input("\nPress Enter to continue...")

def scan_networks():
    print_info("Scanning nearby Wi-Fi networks...")
    try:
        result = subprocess.check_output(["termux-wifi-scaninfo"], stderr=subprocess.STDOUT, timeout=10)
        data = json.loads(result.decode())
       
        if isinstance(data, dict) and "error" in data:
            print_error(f"API Error: {data['error']}")
            print_warning("Make sure GPS/Location is ON.")

            input("\nPress Enter...")
            return
               
        if not isinstance(data, list):
            print_error("Unexpected output from Termux API.")

            input("\nPress Enter...")
            return

        if len(data) == 0:
            print_error("No networks found.")
            print_warning("Make sure GPS/Location is ON and try again.")
        else:
            print(f"\n[bold cyan]Found {len(data)} networks:[/bold cyan]\n")
            output = f"Found {len(data)} networks:\n\n"
            for net in data:
                if isinstance(net, dict):

                    ssid = net.get("SSID") or net.get("ssid") or "Hidden"
                    bssid = net.get("BSSID") or net.get("bssid") or "Unknown"
                    freq = net.get("frequency") or net.get("freq") or 0
                    level = net.get("level") or net.get("rssi") or 0
                   
                    print(f"📶 [bold yellow]SSID:[/bold yellow] {ssid}")
                    print(f"   BSSID: {bssid}")
                    print(f"   Frequency: {freq} MHz | Signal: {level} dBm\n")
                   
                    output += f"SSID: {ssid}\nBSSID: {bssid}\nFrequency: {freq} MHz | Signal: {level} dBm\n\n"
           
            filename = save_report("Wireless_Scan", "termux-wifi-scaninfo", output)

            print_info(f"Report saved: {filename}")
                   
    except subprocess.TimeoutExpired:
        print_error("Termux API timed out.")

    except Exception as e:
        print_error(f"Error: {e}")
    input("\nPress Enter to continue...")

def connection_info():
    print_info("Fetching current Wi-Fi connection info...")
    try:
        result = subprocess.check_output(["termux-wifi-connectioninfo"], stderr=subprocess.STDOUT, timeout=10)

        info = json.loads(result.decode())
       
        if isinstance(info, list) and len(info) > 0:
            info = info[0]
           
        if isinstance(info, dict) and "error" in info:
            print_error(f"Error: {info['error']}")
            input("\nPress Enter...")
            return

           
        ssid = info.get('SSID') or info.get('ssid') or 'Unknown'
        bssid = info.get('BSSID') or info.get('bssid') or 'Unknown'

        ip = info.get('ip') or info.get('IP') or 'Unknown'
       
        output = f"SSID: {ssid}\nBSSID: {bssid}\nIP Address: {ip}"

        print(f"\n[bold cyan]{output}[/bold cyan]")
       
        filename = save_report("Wireless_Connection", "termux-wifi-connectioninfo", output)

        print_info(f"Report saved: {filename}")
    except subprocess.TimeoutExpired:
        print_error("Termux API timed out.")

    except Exception as e:
        print_error(f"Error: {e}")
    input("\nPress Enter to continue...")

def scan_local_network():
    print_info("Scanning connected local network...")
    try:
        result = subprocess.check_output(["termux-wifi-connectioninfo"], timeout=10).decode()

        info = json.loads(result)
       
        if isinstance(info, list) and len(info) > 0:
            info = info[0]
           
        if isinstance(info, dict) and "error" in info:
            print_error(f"Error: {info['error']}")
            input("\nPress Enter...")

            return
           
        ip = info.get("ip") or info.get("IP") or ""
        if not ip or ip == "Unknown":
            print_error("Not connected to Wi-Fi.")
            input("Press Enter...")
            return
           
        subnet = ".".join(ip.split(".")[:3]) + ".0/24"
        print_info(f"Your subnet is {subnet}. Scanning with nmap...")
        run(["nmap", "-sn", subnet])
       
    except Exception as e:

        print_error(f"Error: {e}")
        input("Press Enter...")

def wireless_menu():
    module_loading("Wireless Tools")
    clear()
    print_warning("IMPORTANT: Android Privacy Restrictions")
    print("Android requires the following for Wi-Fi scanning to work:")
    print("  1. GPS / Location must be TURNED ON.")
    print("  2. 'Termux:API' app must have LOCATION permission.")
    print("  3. The 'Termux:API' app must be installed from F-Droid.\n")
    print_info("If you see 'Hidden' or 'Unknown', check the above settings.")
    input("Press Enter to continue to the menu...")


    while True:
        clear()
        options = {
            "1": "Scan Nearby Wi-Fi Networks",
            "2": "Current Connection Info",
            "3": "Scan Local Network Devices (nmap)",
            "4": "Monitor Mode (Root Required) ⚠️",
            "5": "Deauth Attack (Root Required) ⚠️",

            "0": "Back to Main Menu"
        }
        icons = {k: "»" for k in options}
        icons["0"] = "◀"
       
        draw_menu("WIRELESS TOOLS", options, icons)

        choice = input("➤ Choose: ")

        if choice == "1":
            scan_networks()
        elif choice == "2":
            connection_info()
        elif choice == "3":
            scan_local_network()
        elif choice == "4":
            print_warning("Monitor Mode requires ROOT.")

            input("\nPress Enter...")
        elif choice == "5":
            print_warning("Deauth Attack requires Monitor Mode and ROOT.")

            input("\nPress Enter...")
        elif choice == "0":
            break
        else:
            input("Wrong choice. Press Enter...")
