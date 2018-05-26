#!/bin/sh
#
# For hosting on Glitch.com

set -eu

cd .glitch

# Install dependencies
pip3 install -U --user -r ../requirements.txt

# Import font
mkdir -p ~/.local/share/fonts
cp SourceSansPro-Bold.otf ~/.local/share/fonts
fc-cache -f

exec supervisord -n
