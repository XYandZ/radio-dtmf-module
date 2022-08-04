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

### Local Installation

Copy `system/provisioning/install.sh` to the device that will be connected to the radio and run it.
Note this install, enable, and start a systemd service immediately. Ensure that all system configuration is handled
before running this script.

### ALSA Configuration

List ALSA devices and identify a device capable of audio input and output.
```shell
aplay -l
```

Identify the **card** number of the audio device you plan to use. Create a file in `/etc/asound.conf` that sets this
card to the default for ALSA pcm and ctl.
```shell
# /etc/asound.conf

defaults.pcm.!card 1
defaults.ctl.!card 1
```

### Environment Variables

Note these variables are usually set with an `/etc/default` file by the install script but they can be set
manually for testing or alternate methods of installation.

| Variable           | Service | Description                             | Default |
|--------------------|---------|-----------------------------------------|---------|
| OWM_API_KEY        | OWM     | Open Weather Maps API Key.              | None    |
| OWM_CITY           | OWM     | Open Weather Maps City.                 | None    |
| ALSA_DEVICE        | Audio   | ALSA Device for audio input and output. | 0       |
| BME280_IC2_PORT    | BME280  | BME280 IC2 Port.                        | 1       |
| BME280_IC2_ADDRESS | BME280  | BME280 IC2 Address.                     | 0x76    |