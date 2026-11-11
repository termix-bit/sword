import os
import time
import json
from rich.console import Console
from rich.panel import Panel
from rich.theme import Theme
from rich.box import ROUNDED

custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
    "menu_title": "bold magenta",
    "menu_item": "bright_white",
})

console = Console(theme=custom_theme)

def clear():
    console.clear()

def show_logo():
    clear()
    logo = """
   ███████╗██╗    ██╗ ██████╗ ██████╗ ██████╗ 
   ██╔════╝██║    ██║██╔═══██╗██╔══██╗██╔══██╗
   ███████╗██║ █╗ ██║██║   ██║██████╔╝██║  ██║
   ╚════██║██║███╗██║██║   ██║██╔══██╗██║  ██║
   ███████║╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝
   ╚══════╝ ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝ 
    """
    console.print(logo, style="bold cyan", justify="center")
    console.print("[italic bright_black]Termux Security Framework[/italic bright_black]", justify="center")
    console.print()

def loading_animation(text="Loading", duration=1.5):
    chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        print(f"\r\033[K \033[96m{chars[i % len(chars)]} {text}...\033[0m", end="", flush=True)
        time.sleep(0.1)
        i += 1
    print("\r\033[K", end="", flush=True)

def module_loading(module_name):
    from core.settings_manager import animations_enabled
    if animations_enabled():
        loading_animation(f"Loading {module_name}", 0.6)

def set_proxy_env():
    from core.paths import SETTINGS_FILE
    import os
    import json
    keys = ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy")
    for key in keys:
        os.environ.pop(key, None)
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            settings = json.load(f)
        proxy = settings.get("proxy", "").strip()
        if proxy:
            for key in keys:
                os.environ[key] = proxy
            return True
    except (OSError, ValueError, AttributeError):
        pass
    return False

def print_success(msg):
    console.print(f"[success]✔ {msg}[/success]")

def print_error(msg):
    console.print(f"[error]✘ {msg}[/error]")

def print_warning(msg):
    console.print(f"[warning]⚠ {msg}[/warning]")

def print_info(msg):
    console.print(f"[info]ℹ {msg}[/info]")

def draw_menu(title, options, icons=None):
    console.print(Panel.fit(f"[bold magenta]{title}[/bold magenta]", border_style="magenta", box=ROUNDED))
    
    if icons is None:
        icons = {}
    
    for key, value in options.items():
        icon = icons.get(key, "•")
        if value.startswith("---"):
            console.print("[dim cyan]" + "-" * 40 + "[/dim cyan]")
        else:
            console.print(f"[bold yellow] [{key}] [/bold yellow] [bright_white]{icon} {value}[/bright_white]")
    
    console.print("[magenta]" + "═" * 45 + "[/magenta]")
