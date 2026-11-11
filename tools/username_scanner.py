import asyncio
import aiohttp
import json
import os
import secrets
from urllib.parse import quote, urlsplit

DATASET_PATH = os.path.join(os.path.dirname(__file__), "wmn-data.json")
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.5",
}
MAX_RESPONSE_SIZE = 256 * 1024

def load_sites():
    if not os.path.exists(DATASET_PATH):
        print("[-] Dataset not found.")
        return []
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("sites", [])

def build_site_url(template, username):
    if not isinstance(template, str) or "{account}" not in template:
        raise ValueError("Invalid URL template")
    safe_username = quote(username, safe="._-")
    url = template.format(account=safe_username)
    parsed = urlsplit(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Invalid URL scheme")
    if not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("Invalid URL authority")
    return url

async def read_response(response):
    raw = await response.content.read(MAX_RESPONSE_SIZE + 1)
    raw = raw[:MAX_RESPONSE_SIZE]
    encoding = response.charset or "utf-8"
    try:
        return raw.decode(encoding, errors="replace")
    except Exception:
        return ""

async def is_reachable(session, url, timeout=5):
    try:
        async with session.head(url, timeout=timeout, allow_redirects=False) as resp:
            return True
    except Exception:
        return False

async def check_site(session, site, username):
    template = site.get("uri_check", "")
    if not template:
        return None
    
    try:
        url = build_site_url(template, username)
    except (ValueError, aiohttp.ClientError, asyncio.TimeoutError):
        return None

    e_code = site.get("e_code", 200)
    m_code = site.get("m_code", 404)
    e_str = site.get("e_string")
    m_str = site.get("m_string")

    try:
        async with session.get(url, headers=HEADERS, timeout=8, allow_redirects=False) as response:
            status = response.status
            text = await read_response(response)

            if m_code is not None and status == m_code:
                return None
            if m_str and m_str in text:
                return None
            if e_code is not None and status != e_code:
                return None
            if e_str and e_str not in text:
                return None

            fake = "zz" + secrets.token_hex(4)
            try:
                fake_url = build_site_url(template, fake)
                async with session.get(fake_url, headers=HEADERS, timeout=5, allow_redirects=False) as fresp:
                    ftext = await read_response(fresp)
                    if fresp.status == e_code and (not e_str or e_str in ftext):
                        return None 
            except (aiohttp.ClientError, asyncio.TimeoutError, ValueError):
                return None

            return (site.get("name", "Unknown"), url)
    except (aiohttp.ClientError, asyncio.TimeoutError, ValueError):
        return None

async def scan_username(username):
    all_sites = load_sites()
    if not all_sites:
        return
    
    print(f"\n[*] Step 1: Checking which sites are reachable from your network...")
    reachable_sites = []
    
    connector = aiohttp.TCPConnector(limit=20)
    async with aiohttp.ClientSession(connector=connector, trust_env=True) as session:
        check_tasks = []
        for site in all_sites:
            if "uri_check" in site:
                try:
                    probe_url = site["uri_check"].format(account="sword-probe")
                    check_tasks.append(is_reachable(session, probe_url))
                except (KeyError, ValueError):
                    check_tasks.append(asyncio.sleep(0, result=False))
            else:
                check_tasks.append(asyncio.sleep(0, result=False))
        
        results = await asyncio.gather(*check_tasks)
        
        for site, is_up in zip(all_sites, results):
            if is_up:
                reachable_sites.append(site)
        
        print(f"[*] {len(reachable_sites)} out of {len(all_sites)} sites are reachable.\n")
        
        if not reachable_sites:
            print("[-] No sites reachable. Your network is heavily filtered.")
            print("[!] This tool works best with a proxy/VPN.")
            return
        
        print(f"[*] Step 2: Scanning username '{username}' on reachable sites...\n")
        found = []
        
        scan_tasks = []
        for site in reachable_sites:
            scan_tasks.append(check_site(session, site, username))
        
        scan_results = await asyncio.gather(*scan_tasks)
        
        for result in scan_results:
            if result:
                found.append(result)
                print(f"[+] Found: {result[0]} -> {result[1]}")
        
        if not found:
            print("[-] No accounts found on reachable sites.")
        else:
            print(f"\n[✓] Finished! Found {len(found)} accounts on reachable sites.")
        
        return found

def run_scanner():
    username = input("Enter username to search: ").strip()
    if username:
        asyncio.run(scan_username(username))
    input("\nPress Enter to return...")
