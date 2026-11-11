import os
import hashlib
import base64
from core.ui import clear, draw_menu, print_info, print_error, module_loading
from core.logger import save_report

def crypto_menu():
    module_loading("Crypto Tools")
    while True:
        clear()
        options = {
            "1": "Hash Generator (MD5, SHA1, SHA256)",
            "2": "Base64 Encode",
            "3": "Base64 Decode",
            "4": "ROT13 Cipher",
            "5": "XOR Cipher",
            "0": "Back to Main Menu"
        }
        icons = {k: "»" for k in options}
        icons["0"] = "◀"
        
        draw_menu("CRYPTO TOOLS", options, icons)
        choice = input("➤ Choose: ")

        if choice == "1":
            text = input("Enter text: ")
            output = f"MD5:    {hashlib.md5(text.encode()).hexdigest()}\nSHA1:   {hashlib.sha1(text.encode()).hexdigest()}\nSHA256: {hashlib.sha256(text.encode()).hexdigest()}"
            print(f"\n[bold cyan]{output}[/bold cyan]")
            
            filename = save_report("Crypto_Hash", f"Hash for: {text}", output)
            print_info(f"Report saved: {filename}")
            input("\nPress Enter...")
        elif choice == "2":
            text = input("Enter text: ")
            output = base64.b64encode(text.encode()).decode()
            print(f"\n[bold cyan]Base64:[/bold cyan] {output}")
            
            filename = save_report("Crypto_Base64_Encode", f"Encode: {text}", output)
            print_info(f"Report saved: {filename}")
            input("\nPress Enter...")
        elif choice == "3":
            text = input("Enter Base64: ")
            try:
                output = base64.b64decode(text.encode()).decode()
                print(f"\n[bold cyan]Decoded:[/bold cyan] {output}")
                
                filename = save_report("Crypto_Base64_Decode", f"Decode: {text}", output)
                print_info(f"Report saved: {filename}")
            except Exception:
                print_error("Invalid Base64 string!")
            input("\nPress Enter...")
        elif choice == "4":
            text = input("Enter text: ")
            result = ""
            for char in text:
                if char.isalpha():
                    if char.islower():
                        result += chr((ord(char) - ord('a') + 13) % 26 + ord('a'))
                    else:
                        result += chr((ord(char) - ord('A') + 13) % 26 + ord('A'))
                else:
                    result += char
            print(f"\n[bold cyan]ROT13:[/bold cyan] {result}")
            
            filename = save_report("Crypto_ROT13", f"ROT13: {text}", result)
            print_info(f"Report saved: {filename}")
            input("\nPress Enter...")
        elif choice == "5":
            text = input("Enter text: ")
            key = input("Enter key (integer): ")
            try:
                result = "".join(chr(ord(c) ^ int(key)) for c in text)
                output = result.encode().hex()
                print(f"\n[bold cyan]XOR Hex:[/bold cyan] {output}")
                
                filename = save_report("Crypto_XOR", f"XOR: {text} with key {key}", output)
                print_info(f"Report saved: {filename}")
            except ValueError:
                print_error("Key must be an integer!")
            input("\nPress Enter...")
        elif choice == "0":
            break
        else:
            input("Wrong choice. Press Enter...")
