<div align="center">

⚔️ Sword
Modular Security Toolkit for Termux




Sword is a modular, menu-driven security framework for Termux on Android, written in Python and powered by Rich for its terminal interface. It brings together network utilities, web assessment tools, OSINT helpers, wireless information, basic encoding and hashing utilities, forensics commands, custom Python plugins, and report management in one interface.

Features · Requirements · Installation · Usage · Security & Legal Notes

</div>

Features
Sword is organized into nine modules. Some external tools are installed by install.sh; others must be installed separately. See External tools before using a module.

Module	Capabilities	Tools / dependencies
Network	Host discovery, service and port scans, aggressive scans, OS detection, ping, traceroute, DNS lookup, Wi-Fi connection details, custom-packet option	nmap, ping, traceroute, dig, hping3, rustscan, Termux
Web	SQL injection testing, directory/content discovery, technology detection, NS record lookup, HTTP header inspection, TLS certificate dates	sqlmap, ffuf, whatweb, nslookup, curl, Python ssl
OSINT	WHOIS and DNS lookups, IP geolocation, opening an email breach-check page, username search	whois, nslookup, ip-api.com, Have I Been Pwned, maigret*
Wireless	Nearby Wi-Fi scan, current Wi-Fi connection details, local-network device discovery	Termux, nmap
Crypto	MD5, SHA-1 and SHA-256 hashes; Base64 encode/decode; ROT13 and XOR demonstrations	Python standard library
Forensics	File-type identification, printable-string extraction, metadata inspection, hexadecimal preview	file, strings, exiftool, xxd*
Custom	Discover and run user-provided Python scripts from custom_scripts/	Python 3
Reports	Save scan output as JSON, view saved reports, generate HTML reports for a browser, delete individual or all reports	Python; local loopback report server
Settings	Language and animation preferences, proxy environment settings, update check, reset, and preset workflows	Git; configured command-line tools
* These commands are not installed by the current installer and may need to be installed manually. See External tools.

Settings presets
The Settings module also provides preset workflows:

Full Website Audit — headers, technology identification, TLS information, DNS records, and common subdomain checks.

OSINT Profile — IP geolocation or a small set of public social-profile checks.

Quick Network Scan — live-host discovery and a fast port scan for a supplied subnet.

Specific Wi-Fi Scan — lists nearby Wi-Fi networks and records the selected network details.

Scan Nearby Devices — attempts to determine the connected Wi-Fi subnet and runs an Nmap scan.

Wireless feature status: Nearby Wi-Fi scanning, connection information, and the Nmap local-network scan are implemented. The menu entries for Monitor Mode and Deauth Attack currently display prerequisite warnings only; those capabilities are not implemented in this Beta release.

Requirements
Android: 8.0 or later (as specified for this project).

Terminal: Termux. Use the F-Droid build; do not use the outdated Google Play build.

Python: 3.14 or later. The installer installs Python through Termux packages; verify the installed version with python --version.

Internet connection: Required to install dependencies and to use network-based tools and OSINT services.

Termux:API: Install the separate Termux Android app from the same source/signing channel as Termux, and grant it the required permissions. The termux-api command package is also installed by install.sh.

For Wi-Fi scanning, Android may require Location permission for Termux and Location Services to be enabled. Android version, device vendor, and permission settings can affect the information returned by the API.

Installation
Open Termux and run the following commands:

# Update Termux packages and install Git
pkg update -y && pkg upgrade -y
pkg install -y git

# Clone Sword
git clone https://github.com/termix-bit/sword.git
cd sword

# Install Python and command-line dependencies
bash install.sh

# Launch Sword
python main.py
The installer updates Termux packages, installs the base packages listed in install.sh, installs the Python dependencies from requirements.txt, and attempts to set up SQLMap, FFUF, and WhatWeb.

Python dependencies currently listed in requirements.txt:

rich — terminal interface and formatting.

aiohttp — asynchronous HTTP client used by the username-scanning helper.

Review install.sh before running it. It updates packages and downloads third-party tools from their upstream repositories. Installation time and success depend on your device architecture, Termux repositories, network access, and upstream availability.

External tools
The installer does not install every command referenced by every module. Depending on which features you plan to use, install and verify these tools separately:

Tool / command	Used by	Installation status
Nmap, WHOIS, DNS utilities, cURL, Wget	Network, Web, OSINT	Installed by install.sh through pkg
SQLMap	Web	Cloned by install.sh into $HOME/sqlmap
FFUF	Web	Installed by install.sh using Go
WhatWeb	Web	Cloned and set up by install.sh (Ruby/Bundler required)
RustScan	Network	Manual installation required
Maigret	OSINT	Manual installation required
hping3	Network	Manual installation required; raw-packet features may require root
ExifTool	Forensics	Manual installation required
file, xxd, traceroute	Forensics / Network	Check availability and install separately if missing
strings	Forensics	Usually provided by the installed binutils package
After installing an optional tool, make sure its executable is available in Termux's PATH. Sword invokes several tools by command name, so a binary installed outside PATH may not be found.

Usage
Start Sword with python main.py.

Select a module from the main menu.

Enter the target or file information requested by that module.

Review the command output in the terminal.

Open Reports to view saved JSON reports or generate an HTML view in your browser.

Use only targets you own or are explicitly authorized to assess. See Security Notes & Legal Use.

Custom Python scripts
Sword can discover Python scripts placed in the project-level custom_scripts/ folder.

Create the folder if it does not already exist:

mkdir -p custom_scripts
Copy your own .py script into that folder. For example:

cp ~/my_tool.py custom_scripts/
Launch Sword and open Custom Tools.

Select the script from the menu to run it.

Plugin security: Custom scripts run as separate Python processes with the same Android/Termux user permissions as Sword. A plugin can read or modify files accessible to that user and can launch other processes. Only run scripts you wrote yourself or have reviewed and trust. The current execution timeout is 120 seconds.

Reports and generated files
Scan output is saved locally under reports/ as JSON. The Reports module can generate an HTML version for viewing in a browser through a temporary local server bound to 127.0.0.1. Treat reports as potentially sensitive: they may contain target addresses, commands, and scan output. Do not commit real reports or private scan data to a public repository.

Security Notes & Legal Use
Authorized testing only
Sword is intended for education and authorized security testing. Only scan devices, applications, accounts, and networks that you own or have explicit permission to test. Unauthorized access or scanning may violate laws, contracts, or service terms. You are responsible for complying with all applicable laws and obtaining permission before testing.

Root access
Sword can run without root for many basic features. Some operations may require a rooted device or additional privileges, depending on the device and scan mode. Examples include hping3 raw-packet operations and Nmap OS detection (-O). Features marked as root-required in the menu may fail on non-rooted devices or restricted Android builds.

Proxy and VPN
Some OSINT endpoints and external services may be unreachable on restricted or filtered networks, including in countries such as Iran. You can configure a proxy from Settings → Set Proxy/VPN, or use a VPN at the device level.

Proxy behavior is tool-dependent: Sword can set proxy-related environment variables, but not every command-line utility honors them, and SOCKS support depends on the individual tool. Do not assume that all scans or requests automatically pass through the configured proxy.

Wireless permissions
For Wireless features:

Install the Termux Android app.

Install the Termux command package (termux-api), which the installer attempts to add.

Grant the required Location permission to Termux and enable Location Services when Android requests it.

Expect limitations imposed by Android and the device manufacturer.

External services and privacy
Some OSINT actions contact third-party services. The IP geolocation feature currently sends the queried IP address to ip-api.com (the implementation uses HTTP), and the email breach-check option opens the Have I Been Pwned account page in the device browser. Review the relevant providers’ terms and privacy policies before using these features; do not submit data you are not authorized to share.

The repository also contains a WhatsMyName dataset and an auxiliary username-scanner helper under tools/. That helper is not currently exposed as an option in the main menu.

Beta status
Sword is a Beta project and is still under development. Some features depend on external tools that must be installed manually, and behavior can vary across Android versions and devices. Not every menu entry implies that the underlying device or optional tool supports that operation.

Cryptography disclaimer
The Crypto module is intended for basic demonstrations and utility tasks. Base64 and ROT13 are encodings/obfuscation, not encryption. XOR with a simple key is not suitable for protecting sensitive data. MD5 and SHA-1 are cryptographically broken for collision-resistant security uses. Do not use these features as a substitute for modern, authenticated cryptography.

Project structure
sword/
├── core/                  # Executor, paths, settings, UI, report server, validators
├── modules/
│   ├── network/           # Network discovery and scanning
│   ├── web/               # Web assessment helpers
│   ├── osint/             # OSINT lookups
│   ├── wireless/          # Wi-Fi information via Termux:API
│   ├── crypto/            # Hashing and encoding demonstrations
│   ├── forensics/         # File and metadata utilities
│   ├── custom/            # Python plugin runner
│   ├── reports/           # JSON and HTML report management
│   └── settings/          # Preferences and preset workflows
├── tools/                 # Auxiliary tools and WhatsMyName dataset
├── custom_scripts/        # User-created Python plugins (created as needed)
├── reports/               # Generated reports (created at runtime)
├── screenshots/           # Project screenshots
├── main.py                # Main entry point
├── install.sh             # Termux setup script
├── requirements.txt       # Python dependencies
├── THIRD_PARTY_NOTICES.md # Third-party dataset notices
├── LICENSE                # MIT License
└── README.md
Screenshots
Screenshots will be added here.

<!-- Add screenshot links here when the final images are ready. -->

Credits & acknowledgements
Sword builds on the work of the open-source projects and services it uses. Thanks to their maintainers and contributors, including:

Rich — terminal UI and formatting.

aiohttp — asynchronous HTTP client.

Nmap — network discovery and security auditing.

SQLMap — SQL injection testing automation.

FFUF — web fuzzing.

WhatWeb — web technology identification.

Maigret and RustScan — optional external tools.

WhatsMyName — username lookup dataset included at tools/wmn-data.json.

Third-party dataset license
The WhatsMyName dataset is distributed under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0). Its license is separate from Sword's MIT license. See THIRD_PARTY_NOTICES.md and the CC BY-SA 4.0 license for details and attribution requirements.

License
Sword's original project code is released under the MIT License. See the LICENSE file. Third-party components and datasets remain subject to their respective licenses; see THIRD_PARTY_NOTICES.md.

Contributing
Bug reports, documentation improvements, and pull requests are welcome. Before submitting a feature or a larger change, consider opening an issue to discuss the proposal. Please include reproduction steps, device/Android details, Termux source, and relevant error output when reporting a bug. Remove private targets, tokens, and personal information from logs before sharing them.

<div align="center">

Made with ❤️ for Termux

</div>
