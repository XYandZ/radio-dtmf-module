#!/bin/bash

sudo DEBIAN_FRONTEND=noninteractive apt-get update -y && \
    apt-get install -y \
    build-essential \
    espeak \
    ffmpeg \
    libespeak1 \
    portaudio19-dev

pip install --no-cache-dir ../../

# Sanity check to see if program sort of works
/usr/bin/python -m radiodtmf --version

sudo install -o root -g root -m 600 \
    ../default/radiodtmf \
    /etc/default/radiodtmf

sudo install -o root -g root -m 644 \
    ../systemd/radiodtmf.service \
    /etc/systemd/system/radiodtmf.service

systemd-analyze verify radiodtmf.service

sudo systemctl reset-failed
sudo systemctl enable radiodtmf
sudo systemctl start radiodtmf