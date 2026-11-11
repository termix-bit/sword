import shutil
import os
import socket
import ssl
from urllib.parse import urlsplit
from core.ui import clear, draw_menu, print_info, print_error, module_loading
from core.logger import save_report
from core.executor import run_command
from core.validators import validate_url

def run(cmd_list):
    cmd_str = ' '.join(cmd_list) if isinstance(cmd_list, list) else cmd_list
    print_info(f"Running: {cmd_str}")
    print()
    code, output = run_command(cmd_list)
    print(output)
    if code != 0:
        print_error(f"Command failed (exit code: {code})")
    filename = save_report("Web", cmd_str, output)
    print_info(f"Report saved: {filename}")
    input("\nPress Enter to continue...")

def check_ssl(domain, port=443):
    context = ssl.create_default_context()
    try:
        with socket.create_connection((domain, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as tls:
                cert = tls.getpeercert()
                return f"Not Before: {cert.get('notBefore')}\nNot After: {cert.get('notAfter')}"
    except (OSError, ssl.SSLError, ValueError) as e:
        return f"SSL Error: {e}"

SQLMAP_PATH = os.path.expanduser("~/sqlmap")
FFUF_PATH = shutil.which("ffuf")
WHATWEB_PATH = shutil.which("whatweb")

def web_menu():
    module_loading("Web Tools")
    while True:
        clear()
        options = {
            "1": "SQL Injection Scan (sqlmap)",
            "2": "Directory Bruteforce (ffuf)",
            "3": "Technology Detection (whatweb)",
            "4": "Subdomain Finder (nslookup NS)",
            "5": "Header Scanner (curl -I)",
            "6": "SSL/TLS Check",
            "0": "Back to Main Menu"
        }
        icons = {k: "»" for k in options}
        icons["0"] = "◀"
        
        draw_menu("WEB TOOLS", options, icons)
        choice = input("➤ Choose: ")

        try:
            if choice == "1":
                url = validate_url(input("Target URL: "))
                run(["python", f"{SQLMAP_PATH}/sqlmap.py", "-u", url, "--batch", "--dbs"])
            elif choice == "2":
                url = validate_url(input("Target URL: "))
                wordlist = input("Wordlist path: ")
                run([FFUF_PATH, "-u", f"{url}/FUZZ", "-w", wordlist])
            elif choice == "3":
                url = validate_url(input("Target URL: "))
                run([WHATWEB_PATH, url])
            elif choice == "4":
                domain = input("Domain: ")
                run(["nslookup", "-type=ns", domain])
            elif choice == "5":
                url = validate_url(input("Target URL: "))
                run(["curl", "-I", "--", url])
            elif choice == "6":
                domain = input("Domain or URL: ").strip()
                if domain:
                    parsed = urlsplit(domain if "://" in domain else "https://" + domain)
                    hostname = parsed.hostname
                    if hostname:
                        print_info(f"Checking SSL for {hostname}...")
                        ssl_result = check_ssl(hostname)
                        print(f"\n[bold cyan]{ssl_result}[/bold cyan]")
                        filename = save_report("Web_SSL", f"SSL Check for {hostname}", ssl_result)
                        print_info(f"Report saved: {filename}")
                input("\nPress Enter...")
            elif choice == "0":
                break
            else:
                input("Wrong choice. Press Enter...")
        except ValueError as e:
            print_error(f"Invalid input: {e}")
            input("Press Enter...")
