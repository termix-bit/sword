import os
import json
import urllib.request
import subprocess
import shutil
from urllib.parse import quote
from core.ui import clear, draw_menu, print_info, print_error, module_loading
from core.logger import save_report
from core.executor import run_command
from core.validators import validate_domain, validate_username, validate_ip

def run(cmd_list):
    cmd_str = ' '.join(cmd_list) if isinstance(cmd_list, list) else cmd_list
    print_info(f"Running: {cmd_str}")
    print()
    code, output = run_command(cmd_list)
    print(output)
    if code != 0:
        print_error(f"Command failed (exit code: {code})")
    filename = save_report("OSINT", cmd_str, output)
    print_info(f"Report saved: {filename}")
    input("\nPress Enter to continue...")

def get_json(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        print_error(f"Error: {e}")
        return None

WHOIS_PATH = shutil.which("whois")
NSLOOKUP_PATH = shutil.which("nslookup")
MAIGRET_PATH = shutil.which("maigret")

def osint_menu():
    module_loading("OSINT Tools")
    while True:
        clear()
        options = {
            "1": "WHOIS Lookup",
            "2": "DNS Lookup",
            "3": "IP Geolocation",
            "4": "Email Breach Check",
            "5": "Username Search (Maigret)",
            "0": "Back to Main Menu"
        }
        icons = {k: "»" for k in options}
        icons["0"] = "◀"
        
        draw_menu("OSINT TOOLS", options, icons)
        choice = input("➤ Choose: ")

        try:
            if choice == "1":
                domain = validate_domain(input("Domain (e.g. example.com): "))
                if not WHOIS_PATH:
                    print_error("whois is not installed. Run: pkg install whois")
                    input("Press Enter...")
                    continue
                run([WHOIS_PATH, domain])
            elif choice == "2":
                domain = validate_domain(input("Domain: "))
                if not NSLOOKUP_PATH:
                    print_error("nslookup is not installed. Run: pkg install dnsutils")
                    input("Press Enter...")
                    continue
                run([NSLOOKUP_PATH, domain])
            elif choice == "3":
                ip = validate_ip(input("IP address: "))
                data = get_json(f"https://ip-api.com/json/{ip}")
                if data:
                    output = f"IP: {data.get('query')}\nCountry: {data.get('country')}\nCity: {data.get('city')}\nISP: {data.get('isp')}"
                    print(f"\n[bold cyan]{output}[/bold cyan]")
                    filename = save_report("OSINT_IP", f"IP Geolocation for {ip}", output)
                    print_info(f"Report saved: {filename}")
                input("\nPress Enter...")
            elif choice == "4":
                email = input("Email: ").strip()
                if email:
                    url = "https://haveibeenpwned.com/account/" + quote(email, safe="")
                    subprocess.run(["termux-open-url", url], shell=False, check=False)
                input("\nPress Enter...")
            elif choice == "5":
                username = validate_username(input("Username: "))
                if not MAIGRET_PATH:
                    print_error("maigret is not installed. Run: pip install maigret")
                    input("Press Enter...")
                    continue
                run([MAIGRET_PATH, username, "--top-sites", "100", "--dns-resolver", "threaded"])
            elif choice == "0":
                break
            else:
                input("Wrong choice. Press Enter...")
        except ValueError as e:
            print_error(f"Invalid input: {e}")
            input("Press Enter...")
