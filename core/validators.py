import ipaddress
from pathlib import Path
from urllib.parse import urlsplit

def validate_ip(value):
    try:
        return str(ipaddress.ip_address(value.strip()))
    except ValueError:
        raise ValueError("Invalid IP address")

def validate_subnet(value):
    try:
        return str(ipaddress.ip_network(value.strip(), strict=False))
    except ValueError:
        raise ValueError("Invalid subnet")

def validate_port(value):
    try:
        port = int(value)
        if not 1 <= port <= 65535:
            raise ValueError("Port out of range")
        return str(port)
    except ValueError:
        raise ValueError("Invalid port")

def validate_url(value):
    value = value.strip()
    if "://" not in value:
        value = "https://" + value
    parsed = urlsplit(value)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Invalid URL scheme")
    if not parsed.hostname:
        raise ValueError("Invalid hostname")
    if parsed.username or parsed.password:
        raise ValueError("URL credentials not allowed")
    try:
        parsed.port
    except ValueError:
        raise ValueError("Invalid URL port")
    return value

def validate_file_path(value):
    path = Path(value).expanduser().resolve(strict=True)
    if not path.is_file():
        raise ValueError("Not a regular file")
    return str(path)

def validate_domain(value):
    value = value.strip().lower()
    if not value or len(value) > 253:
        raise ValueError("Invalid domain")
    if not all(part.isalnum() or part == "-" for part in value.replace(".", "")):
        raise ValueError("Invalid domain characters")
    return value

def validate_username(value):
    value = value.strip()
    if not value or len(value) > 50:
        raise ValueError("Invalid username length")
    if not all(c.isalnum() or c in "._-" for c in value):
        raise ValueError("Invalid username characters")
    return value
