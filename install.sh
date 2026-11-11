#!/bin/bash
set -Eeuo pipefail

PROJECT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo "================================"
echo "   Sword Installation Script"
echo "================================"

echo "[1/7] Updating packages..."
pkg update -y && pkg upgrade -y

echo "[2/7] Installing base tools..."
pkg install -y python git nmap whois dnsutils curl wget golang rust binutils clang libxml2 libxslt pkg-config termux-api

echo "[3/7] Installing Python requirements..."
pip install -r requirements.txt

echo "[4/7] Installing SQLMap..."
if [ ! -d "$HOME/sqlmap" ]; then
    git clone --depth=1 https://github.com/sqlmapproject/sqlmap.git $HOME/sqlmap
fi

echo "[5/7] Installing FFUF..."
if [ ! -f "$PREFIX/bin/ffuf" ]; then
    go install github.com/ffuf/ffuf/v2@latest
    cp $HOME/go/bin/ffuf $PREFIX/bin/
fi

echo "[6/7] Installing WhatWeb..."
if [ ! -f "$PREFIX/bin/whatweb" ]; then
    pkg install ruby -y
    if [ ! -d "$HOME/WhatWeb" ]; then
        git clone https://github.com/urbanadventurer/WhatWeb.git $HOME/WhatWeb
    fi
    cd $HOME/WhatWeb
    gem install bundler
    bundle install
    cat > $PREFIX/bin/whatweb << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
cd $HOME/WhatWeb && ruby whatweb "$@"
EOF
    chmod +x $PREFIX/bin/whatweb
    cd "$PROJECT_DIR"
fi

echo "[7/7] Installation Complete!"
echo "================================"
echo "Run: python main.py"
