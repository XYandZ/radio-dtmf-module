FROM python:3.8-bullseye

RUN cat > /etc/default/radiodtmf <<EOF
ALSA_DEVICE=0
OWM_API_KEY=12345
OWM_CITY=London,UK
EOF

RUN install -o root -g root -m 644 \
    /tmp/radiodtmf/system/systemd/radiodtmf.service/radiodtmf.service \
    /etc/systemd/system/radiodtmf.service

RUN systemd-analyze verify radiodtmf.service

RUN systemctl enable radiodtmf