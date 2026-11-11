from core.menu import show_main_menu
from core.ui import loading_animation, set_proxy_env
from core.settings_manager import animations_enabled

def main():
    set_proxy_env()
    
    if animations_enabled():
        loading_animation("Starting Sword", 1.5)
    
    while True:
        choice = show_main_menu()
        
        if choice == "1":
            from modules.network import network_menu
            network_menu()
        elif choice == "2":
            from modules.web import web_menu
            web_menu()
        elif choice == "3":
            from modules.osint import osint_menu
            osint_menu()
        elif choice == "4":
            from modules.wireless import wireless_menu
            wireless_menu()
        elif choice == "5":
            from modules.crypto import crypto_menu
            crypto_menu()
        elif choice == "6":
            from modules.forensics import forensics_menu
            forensics_menu()
        elif choice == "7":
            from modules.custom import custom_menu
            custom_menu()
        elif choice == "8":
            from modules.reports import reports_menu
            reports_menu()
        elif choice == "9":
            from modules.settings import settings_menu
            settings_menu()
        elif choice == "0":
            break
        else:
            input("Wrong choice. Press Enter...")

if __name__ == "__main__":
    main()
