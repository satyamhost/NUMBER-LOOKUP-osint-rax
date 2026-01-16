#!/bin/bash

echo "================================================"
echo "⚡ TEAM RAX OSINT Tool - Installation"
echo "================================================"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ASCII Art Banner
echo -e "${CYAN}"
cat << "EOF"
    ███████╗ █████╗ ██╗  ██╗     ██████╗  █████╗ ██╗  ██╗
    ██╔════╝██╔══██╗╚██╗██╔╝     ██╔══██╗██╔══██╗╚██╗██╔╝
    ███████╗███████║ ╚███╔╝█████╗██████╔╝███████║ ╚███╔╝ 
    ╚════██║██╔══██║ ██╔██╗╚════╝██╔══██╗██╔══██║ ██╔██╗ 
    ███████║██║  ██║██╔╝ ██╗     ██║  ██║██║  ██║██╔╝ ██╗
    ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
EOF
echo -e "${NC}"

echo -e "${YELLOW}[*] Starting Installation...${NC}"

# Check system
if [ -d "/data/data/com.termux" ]; then
    echo -e "${GREEN}[+] Termux Environment Detected${NC}"
    IS_TERMUX=true
else
    echo -e "${GREEN}[+] Linux Environment Detected${NC}"
    IS_TERMUX=false
fi

# Update packages
echo -e "${YELLOW}[*] Updating package list...${NC}"
if [ "$IS_TERMUX" = true ]; then
    pkg update -y && pkg upgrade -y
else
    sudo apt-get update -y || sudo pacman -Syu || sudo dnf update -y
fi

# Install Python
echo -e "${YELLOW}[*] Installing Python...${NC}"
if [ "$IS_TERMUX" = true ]; then
    pkg install -y python python-tkinter git
else
    if command -v apt-get &> /dev/null; then
        sudo apt-get install -y python3 python3-tk python3-pip python3-pil.imagetk
    elif command -v pacman &> /dev/null; then
        sudo pacman -S python tk python-pip python-pillow
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y python3 python3-tkinter python3-pip python3-pillow
    fi
fi

# Install Python packages
echo -e "${YELLOW}[*] Installing Python dependencies...${NC}"
pip3 install --upgrade pip

REQUIRED_PACKAGES=(
    "requests"
    "Pillow"
    "qrcode[pil]"
    "pyTelegramBotAPI"
    "numpy"
)

for package in "${REQUIRED_PACKAGES[@]}"; do
    echo -e "${CYAN}[*] Installing $package...${NC}"
    pip3 install "$package"
done

# Create application directory
echo -e "${YELLOW}[*] Setting up application...${NC}"
mkdir -p ~/rax-osint-tool
cp osint_tool_enhanced.py ~/rax-osint-tool/
cp install_enhanced.sh ~/rax-osint-tool/

# Create desktop launcher for Linux
if [ "$IS_TERMUX" = false ]; then
    echo -e "${YELLOW}[*] Creating desktop launcher...${NC}"
    
    cat > ~/.local/share/applications/rax-osint.desktop << EOF
[Desktop Entry]
Name=RAX OSINT Tool
Comment=Advanced Phone Number Lookup Tool by Team RAX
Exec=python3 $HOME/rax-osint-tool/osint_tool_enhanced.py
Icon=$HOME/rax-osint-tool/icon.png
Terminal=false
Type=Application
Categories=Utility;Security;
Keywords=OSINT;Security;Phone;Lookup;
StartupNotify=true
EOF
    
    # Make executable
    chmod +x ~/.local/share/applications/rax-osint.desktop
fi

# Create launch script
echo -e "${YELLOW}[*] Creating launch scripts...${NC}"

# Main launch script
cat > ~/rax-osint-tool/launch_rax.sh << 'EOF'
#!/bin/bash

echo "========================================"
echo "🚀 LAUNCHING RAX OSINT TOOL"
echo "========================================"

cd "$(dirname "$0")"

# Check dependencies
python3 -c "
import sys
import importlib

required = ['tkinter', 'PIL', 'qrcode', 'telebot', 'requests']

for package in required:
    try:
        importlib.import_module(package if package != 'PIL' else 'PIL.Image')
        print(f'✅ {package}')
    except ImportError as e:
        print(f'❌ {package}: {e}')
        sys.exit(1)
"

# Run the tool
echo -e "\n🎮 Starting RAX OSINT Tool..."
echo -e "⚠️  Make sure you have proper authorization!\n"

python3 osint_tool_enhanced.py
EOF

chmod +x ~/rax-osint-tool/launch_rax.sh

# Create Termux shortcut
if [ "$IS_TERMUX" = true ]; then
    echo -e "${YELLOW}[*] Creating Termux shortcut...${NC}"
    
    cat > ~/.shortcuts/RAX-OSINT << EOF
#!/data/data/com.termux/files/usr/bin/bash
cd ~/rax-osint-tool
python3 osint_tool_enhanced.py
EOF
    
    chmod +x ~/.shortcuts/RAX-OSINT
fi

# Create README
cat > ~/rax-osint-tool/README.md << 'EOF'
# 🔍 RAX OSINT TOOL v2.0

Advanced Phone Number Lookup Tool with Cyberpunk Interface

## 🚀 Features
- 📱 Phone Number Intelligence
- 🚨 Data Breach Checking
- 📜 Search History with Analytics
- 🤖 Telegram Bot Integration
- 🎮 Cyberpunk GUI with Animations
- 🔒 Secure & Private

## 📋 Requirements
- Python 3.8+
- Tkinter
- Internet Connection

## 🎯 Quick Start
```bash
cd ~/rax-osint-tool
python3 osint_tool_enhanced.py