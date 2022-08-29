#!/bin/bash

sudo DEBIAN_FRONTEND=noninteractive apt-get update -y && \
    apt-get install -y \
    build-essential \
    espeak \
    ffmpeg \
    libespeak1 \
    portaudio19-dev

cp -r ./ /tmp/radiodtmf/

pushd /tmp/radiodtmf || exit
sudo python -m pip install .
popd || exit

# Sanity check to see if program sort of works
/usr/local/bin/python -m radiodtmf --version

sudo install -o root -g root -m 600 \
    /tmp/radiodtmf/system/default/radiodtmf \
    /etc/default/radiodtmf

sudo install -o root -g root -m 644 \
    /tmp/radiodtmf/system/systemd/radiodtmf.service \
    /etc/systemd/system/radiodtmf.service

systemd-analyze verify radiodtmf.service

sudo systemctl reset-failed
sudo systemctl enable radiodtmf
sudo systemctl start radiodtmf