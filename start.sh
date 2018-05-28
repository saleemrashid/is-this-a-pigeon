#!/bin/sh
#
# For hosting on Glitch.com

set -eu

cd .glitch

readonly INSTALL_DIR="$PWD/sysroot"

apt_install() {
    apt-get download "$@"

    for filename in *.deb; do
        dpkg-deb -x "$filename" "$INSTALL_DIR"
    done
}

# Install dependencies
pip3 install -U --user -r ../requirements.txt
pip2 install -U --user supervisor

export PYTHONPATH="$INSTALL_DIR/usr/lib/python3/dist-packages"
apt_install python3-gi python3-gi-cairo

# Import font
mkdir -p ~/.local/share/fonts
cp SourceSansPro-Bold.otf SourceHanSans-Bold.ttc ~/.local/share/fonts
fc-cache -f

exec supervisord -n
