FROM python:3.8-bullseye
SHELL ["/bin/bash", "-ec"]

RUN DEBIAN_FRONTEND=noninteractive apt-get update -y && \
    apt-get install -y \
    build-essential \
    espeak \
    ffmpeg \
    libespeak1 \
    portaudio19-dev

COPY ./ /tmp/radiodtmf/

WORKDIR /tmp/radiodtmf/

RUN pip install --no-cache-dir ./

RUN /usr/local/bin/python -m radiodtmf --version

RUN install -o root -g root -m 600 \
    /tmp/radiodtmf/system/default/radiodtmf \
    /etc/default/radiodtmf


RUN install -o root -g root -m 644 \
    /tmp/radiodtmf/system/systemd/radiodtmf.service \
    /etc/systemd/system/radiodtmf.service

RUN systemd-analyze verify radiodtmf.service

RUN systemctl reset-failed
RUN systemctl enable radiodtmf
RUN systemctl start radiodtmf