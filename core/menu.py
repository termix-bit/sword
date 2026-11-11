from core.ui import show_logo, draw_menu, console
from rich.panel import Panel

def show_main_menu():
    show_logo()
    
    options = {
        "1": "Network Tools",
        "2": "Web Tools",
        "3": "OSINT Tools",
        "4": "Wireless Tools",
        "5": "Crypto Tools",
        "6": "Forensics Tools",
        "7": "Custom Tools",
        "8": "Reports",
        "9": "Settings",
        "0": "Exit"
    }
    
    console.print(Panel("[bold cyan]MAIN MENU[/bold cyan]", border_style="cyan", expand=False))
    
    icons = {"0": "◀"}
    draw_menu("SELECT AN OPTION", options, icons)
    
    return console.input("\n[bold green]➤ Choose: [/bold green]")
