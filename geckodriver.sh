# geckodriver installer for linux

INSTALL_DIR="/usr/local/bin"

curl -s -L "https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz" | tar -xz
chmod +x geckodriver
sudo mv geckodriver "$INSTALL_DIR"
echo "installed geckodriver binary in $INSTALL_DIR"