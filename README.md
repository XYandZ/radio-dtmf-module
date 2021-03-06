# Radio Basestation

## About

This project turns a typical handset (Baofeng UV-5R or similar) into a base station that receives
[DTMF](https://en.wikipedia.org/wiki/Dual-tone_multi-frequency_signaling) commands and responses with information
sent over the radio via text-to-speech.

## Prerequistes for Ubuntu
```
$ sudo apt update && sudo apt install espeak ffmpeg libespeak1 portaudio19-dev
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

## Run Program 
```
$ python main.py
```

## DTMF Commands

| Command | Result                                            |
|---------|---------------------------------------------------|
| 38 (DT) | Get the current date and day of the week          |
| 86 (TM) | Get the current time in 12 hour format            |
| 99 (WX) | Get the current weather (temperature, wind speed) |
| #       | List commands                                     |