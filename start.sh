#!/bin/sh
#
# For hosting on Glitch.com

set -eu

cd .glitch

readonly INSTALL_DIR="$(mktemp -d)"

install_package() {
    local package="$1"

    local filename="$(apt-get download --print-uris "$package" | awk '{ print $2 }')"

    apt-get download "$package"
    dpkg-deb -x "$filename" "$INSTALL_DIR"
}

# Install dependencies
pip3 install -U --user -r ../requirements.txt
pip2 install -U --user supervisor

export PYTHONPATH="$INSTALL_DIR/usr/lib/python3/dist-packages"
install_package python3-gi
install_package python3-gi-cairo

# Import font
mkdir -p ~/.local/share/fonts
cp SourceSansPro-Bold.otf SourceHanSans-Bold.ttc ~/.local/share/fonts
fc-cache -f

exec supervisord -n
