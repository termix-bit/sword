import os
import json
import subprocess
import hashlib
from core.ui import clear, draw_menu, print_success, print_info, print_warning, print_error, module_loading, console, set_proxy_env
from core.logger import save_report
from core.executor import run_command

from core.paths import SETTINGS_FILE, PROJECT_DIR
SWORD_DIR = PROJECT_DIR

LANGUAGES = {"1": "Persian (فارسی)"}

def load_settings():
    default_settings = {"language": "English", "animations": True, "proxy": "", "safe_mode": False}
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                if isinstance(loaded, dict):
                    default_settings.update(loaded)
        except Exception:
            pass
    return default_settings

def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)

def get_lever(status):
    if status: return "[bold green]▐██████████▌ ON [/bold green]"
    else: return "[bold red]▐░░░░░░░░░░▌ OFF[/bold red]"

def update_sword():
    clear()
    print_info("Checking for updates...")
    try:
        fetch_res = subprocess.run(["git", "fetch"], cwd=SWORD_DIR, capture_output=True, text=True)
        if fetch_res.returncode != 0:
            print_error("Failed to fetch. Check your internet/proxy.")
            input("\nPress Enter..."); return
        status = subprocess.run(["git", "status", "-uno"], cwd=SWORD_DIR, capture_output=True, text=True)
        if "Your branch is up to date" in status.stdout:
            print_success("Sword is up to date!")
        else:
            print_warning("New updates found! Pulling...")
            pull_res = subprocess.run(["git", "pull"], cwd=SWORD_DIR, capture_output=True, text=True)
            if pull_res.returncode == 0: print_success("Updated! Please restart.")
            else: print_error("Update failed.")
    except Exception as e: print_error(f"Error: {e}")
    input("\nPress Enter...")

def run_cmd(cmd_list):
    cmd_str = ' '.join(cmd_list) if isinstance(cmd_list, list) else cmd_list
    code, output = run_command(cmd_list)
    return output

# --- پروفایل ۱: تست وب‌سایت ---
def preset_website_audit():
    clear(); print_info("Full Website Audit")
    url = input("Enter target URL: ")
    if not url: return
    print_info(f"Starting audit for {url}...\n")
    full_report = f"--- WEBSITE AUDIT ---\nTarget: {url}\n\n"
    print("[1/5] Headers..."); full_report += f"--- HEADERS ---\n{run_cmd(['curl', '-s', '-I', url])}\n\n"
    print("[2/5] Tech..."); full_report += f"--- TECHNOLOGY ---\n{run_cmd(['whatweb', url])}\n\n"
    print("[3/5] SSL...")
    domain = url.replace("https://", "").replace("http://", "").split("/")[0]
    from modules.web import check_ssl
    full_report += f"--- SSL ---\n{check_ssl(domain)}\n\n"
    print("[4/5] DNS..."); full_report += f"--- DNS ---\n{run_cmd(['dig', domain, 'ANY', '+noall', '+answer'])}\n\n"
    print("[5/5] Subdomains...")
    found_subs = ""
    for sub in ["www", "mail", "admin", "dev", "api"]:
        ip = run_cmd(["host", f"{sub}.{domain}"])
        if "has address" in ip: found_subs += ip
    full_report += f"--- SUBDOMAINS ---\n{found_subs}\n\n"
    filename = save_report("Preset_WebAudit", f"Audit for {url}", full_report)
    print_success(f"\nAudit finished! Report: {filename}"); input("Press Enter...")

def preset_osint():
    clear(); print_info("OSINT Profile")
    target = input("Enter IP or Username: ").strip()
    if not target: return
    full_report = f"--- OSINT ---\nTarget: {target}\n\n"
    is_ip = target.replace(".", "").isdigit()
    if is_ip:
        print("[*] Fetching IP Geolocation...")
        geo = run_cmd(["curl", "-s", f"http://ip-api.com/json/{target}"])
        if "invalid query" in geo: print_error("Invalid IP.")
        else: full_report += f"--- IP GEOLOCATION ---\n{geo}\n\n"; print_success("IP Info fetched.")
    else:
        print("[*] Checking social media...")
        sites = {"GitHub": f"https://github.com/{target}", "Twitter": f"https://twitter.com/{target}", "Instagram": f"https://instagram.com/{target}", "Reddit": f"https://reddit.com/user/{target}", "Telegram": f"https://t.me/{target}"}
        found = ""
        for name, site_url in sites.items():
            status = run_cmd(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-L", site_url])
            if status.strip() in ["200", "301", "302"]: found += f"{name}: {site_url}\n"; print_success(f"Found on {name}")
            else: print(f"[-] Not found on {name}")
        full_report += f"--- SOCIAL MEDIA ---\n{found}\n\n" if found else "--- SOCIAL MEDIA ---\nNone found.\n\n"
    filename = save_report("Preset_OSINT", f"OSINT for {target}", full_report)
    print_success(f"\nOSINT finished! Report: {filename}"); input("Press Enter...")

# --- پروفایل ۳: اسکن شبکه محلی ---
def preset_network_scan():
    clear(); print_info("Quick Local Network Scan")
    subnet = input("Enter subnet (e.g. 192.168.1.0/24) or press Enter for auto-detect: ")
    if not subnet: subnet = "192.168.1.0/24"
    print_info(f"Scanning {subnet}...\n")
    full_report = f"--- NETWORK SCAN ---\nSubnet: {subnet}\n\n"
    print("[1/2] Finding live hosts...")
    full_report += f"--- LIVE HOSTS ---\n{run_cmd(['nmap', '-sn', subnet])}\n\n"
    print("[2/2] Quick port scan on common ports...")
    full_report += f"--- COMMON PORTS ---\n{run_cmd(['nmap', '-F', subnet])}\n\n"
    filename = save_report("Preset_NetworkScan", f"Scan for {subnet}", full_report)
    print_success(f"\nScan finished! Report: {filename}"); input("Press Enter...")

# --- پروفایل ۴: اسکن شبکه وای‌فای خاص ---
def preset_wifi_specific_scan():
    clear(); print_info("Specific Wi-Fi Scan (Find and Scan)")
    print("[1/2] Scanning nearby networks...")
    try:
        scan_result = subprocess.check_output(["termux-wifi-scaninfo"], stderr=subprocess.STDOUT, timeout=10).decode()
        networks = json.loads(scan_result)
        if isinstance(networks, dict) and "error" in networks:
            print_error(f"API Error: {networks['error']}"); input("Press Enter..."); return
        if not isinstance(networks, list) or len(networks) == 0:
            print_error("No networks found. Make sure GPS is ON."); input("Press Enter..."); return
        print("\nAvailable Networks:")
        options = {}; icons = {}
        for i, net in enumerate(networks, 1):
            ssid = net.get("SSID") or net.get("ssid") or "Hidden"
            bssid = net.get("BSSID") or net.get("bssid") or "Unknown"
            options[str(i)] = f"{ssid} ({bssid})"; icons[str(i)] = "»"
        options["0"] = "Cancel"; icons["0"] = "◀"
        draw_menu("SELECT TARGET WI-FI", options, icons)
        choice = input("➤ Choose: ")
        if choice == "0": return
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(networks):
            print_error("Invalid choice."); input("Press Enter..."); return
        selected_net = networks[int(choice) - 1]
        ssid = selected_net.get("SSID") or selected_net.get("ssid") or "Hidden"
        bssid = selected_net.get("BSSID") or selected_net.get("bssid") or "Unknown"
        print_success(f"Selected: {ssid} ({bssid})")
        print(f"\n[2/2] Scanning target {ssid}...")
        full_report = f"--- SPECIFIC WI-FI SCAN ---\nSSID: {ssid}\nBSSID: {bssid}\nFrequency: {selected_net.get('frequency', 'N/A')}\nSignal: {selected_net.get('level', 'N/A')}\n\n"
        filename = save_report("Preset_WiFi_Specific", f"Scan for {ssid}", full_report)
        print_success(f"\nScan finished! Report: {filename}")
    except Exception as e: print_error(f"Error: {e}")
    input("Press Enter...")

def preset_scan_all_nearby_devices():
    clear(); print_info("Deep Scan All Nearby Devices")
    print("[*] Detecting your local subnet...")
    try:
        result = subprocess.check_output(["termux-wifi-connectioninfo"], stderr=subprocess.STDOUT, timeout=10).decode()
        info = json.loads(result)
        if isinstance(info, list) and len(info) > 0: info = info[0]
        if isinstance(info, dict) and "error" in info:
            print_error(f"API Error: {info['error']}"); input("Press Enter..."); return
        ip = info.get("ip") or info.get("IP") or ""
        if not ip or ip == "Unknown":
            print_error("Not connected to Wi-Fi."); input("Press Enter..."); return
        subnet = ".".join(ip.split(".")[:3]) + ".0/24"
        print_success(f"Your subnet: {subnet}")
    except Exception as e:
        print_error(f"Failed to get IP: {e}")
        subnet = input("Enter subnet manually (e.g. 192.168.1.0/24): ")
        if not subnet: return
    print(f"\n[*] Starting Deep Scan on {subnet}...")
    nmap_output = run_cmd(["nmap", "-sV", "-T4", "--open", subnet])
    print("\n--- Devices & Services Found ---")
    for line in nmap_output.split("\n"):
        if "Nmap scan report for" in line or "MAC Address" in line or "/tcp" in line or "/udp" in line:
            print(line)
    full_report = f"--- DEEP NETWORK SCAN ---\nSubnet: {subnet}\n\n{nmap_output}\n"
    filename = save_report("Preset_DeepDevices", f"Deep Scan for {subnet}", full_report)
    print_success(f"\nDeep scan finished! Report: {filename}")
    input("Press Enter...")

def settings_menu():
    module_loading("Settings")
    while True:
        clear()
        settings = load_settings()
        proxy_status = "[green]Set[/green]" if settings.get("proxy") else "[red]Not Set[/red]"
        options = {
            "1": f"Change Language ({settings['language']})",
            "2": f"Animations        {get_lever(settings['animations'])}",
            "3": f"Set Proxy/VPN (Current: {proxy_status})",
            "4": "Update Sword (Check GitHub)",
            "5": "Reset to Defaults",
            "6": "--- PRESETS & PROFILES ---",
            "7": "Full Website Audit (5-step scan)",
            "8": "OSINT Profile (Username/IP)",
            "9": "Quick Network Scan",
            "10": "Specific Wi-Fi Scan",
            "11": "Scan All Nearby Devices",
            "0": "Back to Main Menu"
        }
        icons = {
            "1": "»", "2": "»", "3": "»", "4": "»", "5": "»",
            "6": "▪", "7": "»", "8": "»", "9": "»", "10": "»", "11": "»", "0": "◀"
        }
        draw_menu("SETTINGS & PRESETS", options, icons)
        choice = input("➤ Choose: ")
        if choice == "1":
            clear(); console.print("[bold cyan]Languages:[/bold cyan]")
            for k, v in LANGUAGES.items(): console.print(f"[bold yellow][{k}][/bold yellow] {v}")
            lang = input("\nChoose: ")
            if lang in LANGUAGES: 
                settings["language"] = LANGUAGES[lang]
                save_settings(settings); print_success(f"Set to {LANGUAGES[lang]}")
            input("Press Enter...")
        elif choice == "2":
            settings["animations"] = not settings.get("animations", True)
            save_settings(settings)
        elif choice == "3":
            clear(); print_info("Set Proxy (e.g. http://127.0.0.1:8080 or socks5://127.0.0.1:1080)")
            print("Leave empty to disable proxy.\n")
            current = settings.get("proxy", "")
            print(f"Current: {current if current else 'None'}")
            new_proxy = input("\nNew Proxy URL: ").strip()
            settings["proxy"] = new_proxy
            save_settings(settings)
            set_proxy_env()
            if new_proxy: print_success(f"Proxy set to: {new_proxy}")
            else: print_info("Proxy disabled.")
            input("Press Enter...")
        elif choice == "4": 
            update_sword()
        elif choice == "5":
            settings = {"language": "English", "animations": True, "proxy": "", "safe_mode": False}
            save_settings(settings)
            set_proxy_env()
            print_success("Settings reset to defaults.")
            input("Press Enter...")
        elif choice == "6": pass
        elif choice == "7": preset_website_audit()
        elif choice == "8": preset_osint()
        elif choice == "9": preset_network_scan()
        elif choice == "10": preset_wifi_specific_scan()
        elif choice == "11": preset_scan_all_nearby_devices()
        elif choice == "0": break
