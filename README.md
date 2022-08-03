# Radio Basestation

## About

This project turns a typical handset (Baofeng UV-5R or similar) into a base station that receives
[DTMF](https://en.wikipedia.org/wiki/Dual-tone_multi-frequency_signaling) commands and responses with information
sent over the radio via text-to-speech.

## Prerequistes for Ubuntu
```shell
sudo apt update
sudo apt install espeak ffmpeg libespeak1 portaudio19-dev
```

## Hardware

* [UV-5R](https://www.amazon.com/dp/B007H4VT7A/) (any handset with Kenwood microphone jack should work)
* [APRS Cable](https://www.amazon.com/BTECH-APRS-K1-Interface-APRSDroid-Compatible/dp/B01LMIBAZW)

## Radio Setup

This program relies on the VOX (amplitude based automatic transmission) function of a handset to function
properly.

You can enable VOX On the UV-5R using the following steps.

* `MENU` -> `4` to select `VOX`
* `MENU` again to modify values 
* Use arrow keys to set `VOX` to `3`
* `MENU` again save the setting

## Start Program Manually

The DTMF module is primarily designed to be run as a systemd service on an embedded system.
However, it can be run as a standalone python project for testing and debug purposes.

From the project root directory run:
```shell
$ pip install .
```

And start the program
```shell
$ python -m radiodtmf
```

## DTMF Commands

| Command | Result                                            |
|---------|---------------------------------------------------|
| 38 (DT) | Get the current date and day of the week          |
| 86 (TM) | Get the current time in 12 hour format            |
| 99 (WX) | Get the current weather (temperature, wind speed) |
| #       | List commands                                     |

## System Configuration

### ALSA

```shell
# /etc/asound.conf

defaults.pcm.!card 1
defaults.ctl.!card 1
```

### Systemd Service

From the project root directory run:

```shell
sudo install -o root -g root -m 644 \
    ./system/systemd/radiodtmf.service/radiodtmf.service \
    /etc/systemd/system/radiodtmf.service

systemd-analyze verify radiodtmf.service

sudo systemctl enable radiodtmf
```

### Environment Variables