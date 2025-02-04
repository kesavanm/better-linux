# Better Gnu/Linux - Build and Package Guide

## Prerequisites

### System Requirements
- Ubuntu 20.04 LTS or later
- Debian 10 or later
- Python 3.8+

### Required Packages
```bash
sudo apt-get update
sudo apt-get install -y \
    python3-pip \
    python3-venv \
    debhelper \
    dh-python \
    python3-tk \
    python3-psutil
```

## Development Setup

### Clone the Repository
```bash
git clone https://github.com/kesavan/better-linux.git
cd better-linux
```

### Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Packaging Process

### 1. Prepare Packaging Structure
```bash
mkdir -p debian/better-linux/usr/bin
mkdir -p debian/better-linux/usr/share/better-linux
mkdir -p debian/better-linux/usr/share/applications
mkdir -p debian/better-linux/DEBIAN
```

### 2. Create Control File
Create `debian/better-linux/DEBIAN/control`:
```
Package: better-linux
Version: 1.0.0
Section: utils
Priority: optional
Architecture: all
Depends: python3 (>= 3.8), python3-tk, python3-psutil, 
         python3-pil | python3-pillow
Recommends: ttkbootstrap
Maintainer: Kesavan Muthuvel <kesavan@example.com>
Description: System Information and Tool Management Application
 Better Gnu/Linux provides an intuitive interface 
 for system insights and tool management.
Homepage: https://github.com/kesavan/better-linux
```

### 3. Create Postinst Script
Create `debian/better-linux/DEBIAN/postinst`:
```bash
#!/bin/bash
set -e

# Ensure Pillow is available
if ! dpkg -s python3-pil python3-pillow >/dev/null 2>&1; then
    python3 -m pip install Pillow
fi

# Create virtual environment
python3 -m venv /usr/share/better-linux/venv
/usr/share/better-linux/venv/bin/pip install \
    psutil pillow ttkbootstrap

chmod +x /usr/bin/better-linux
```

### 4. Copy Application Files
```bash
cp better-linux.py debian/better-linux/usr/share/better-linux/
cp requirements.txt debian/better-linux/usr/share/better-linux/

# Create launcher script
cat > debian/better-linux/usr/bin/better-linux << 'EOL'
#!/bin/bash
/usr/share/better-linux/venv/bin/python /usr/share/better-linux/better-linux.py
EOL
chmod +x debian/better-linux/usr/bin/better-linux
```

### 5. Create Desktop Entry
Create `better-linux.desktop`:
```
[Desktop Entry]
Name=Better Gnu/Linux
Comment=System Information and Tool Management
Exec=better-linux
Icon=better-linux
Terminal=false
Type=Application
Categories=System;
```

### 6. Build Debian Package
```bash
# Set correct permissions
chmod +x debian/better-linux/DEBIAN/postinst
chmod +x debian/better-linux/DEBIAN/prerm

# Build package
dpkg-deb --build debian/better-linux better-linux_1.0.0_all.deb
```

## Installation

### Install Dependencies
```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-tk
```

### Install Package
```bash
# Install the package
sudo dpkg -i better-linux_1.0.0_all.deb

# Fix any dependency issues
sudo apt-get install -f
```

## Troubleshooting

### Common Issues
- **Missing Dependencies**: Ensure all required packages are installed
- **Permission Errors**: Run commands with `sudo`
- **Python Version**: Use Python 3.8 or later

### Uninstallation
```bash
sudo dpkg -r better-linux
sudo apt-get autoremove
```

## Development Tips
- Always test in a virtual environment
- Keep dependencies updated
- Run `pylint` and `black` for code quality

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
[Specify your license here]

---

**Maintained by Kesavan Muthuvel**
*Last Updated: February 2024*