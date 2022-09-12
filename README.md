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

Default / Recommended DTMF Commands

| Command | Result                                                                        |
|---------|-------------------------------------------------------------------------------|
| 38 (DT) | Get the current date and day of the week                                      |
| 86 (TM) | Get the current time in 12 hour format                                        |
| 27 (AQ) | Get estimate of Air Quality Index (AQI) using EPA format                      |
| 99 (WX) | Get the current weather (temperature, barometric pressure, relative humidity) |
| #       | List commands                                                                 |

## System Configuration

### ALSA

This project uses ALSA for audio input and output. Most systems have multiple audio devices, and as such we need to
identify an appropriate device and configure ALSA to use this device by default.

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

### BME280

This project uses the ubiquitous BME280 multisensor chip in order to get hyper local weather information.
The following guide assumes you're attaching the BME280 to a Raspberry Pi but should be adaptable to other SoCs.

#### 4 Pin BME280 Hook Up

_Most_ 4 pin BME280 breakout boards are I2C only and as such are hooked up to the RPi like any other device.

| Board Pin          | Name | RPi Pin                   | RPi Description |
|--------------------|------|---------------------------|-----------------|
| +3.3V Power        | VCC  | P01-1                     | 3V3             |
| Ground             | GND  | P01-6                     | GND             |
| Clock (SCL/I2C)    | SCL  | P01-5                     | GPIO 3 (SCL)    |
| Data (SDA/I2C)     | SDA  | P01-3                     | GPIO 2 (SDA)    |

#### 6 Pin BME280 Hook Up (I2C)

_Most_ 6 pin BME280 breakout boards allow the use of either the I2C or SPI but do not include a built-in logic level
shifter. For this project we require the board to use I2C and will hard configure the board to use this protocol.

| Board Pin                       | Name | RPi Pin                   | RPi Description |
|---------------------------------|------|---------------------------|-----------------|
| +3.3V Power                     | VCC  | P01-1                     | 3V3             |
| Ground                          | GND  | P01-6                     | GND             |
| Clock (SCL/I2C) or (SCK/SPI)    | SCL  | P01-5                     | GPIO 3 (SCL)    |
| Data (SDA/I2C) or (SDI/SPI)     | SDA  | P01-3                     | GPIO 2 (SDA)    |
| Chip Select (High=I2C, Low=SPI) | CSB  | (Connect to Board Ground) | Not Connected   |
| Data (SDO/SPI)                  | SDO  | Not Connected             | Not Connected   |

#### IC2 Configuration

Ensure that the I2C kernel driver is enabled:

    $ dmesg | grep i2c
    [    4.925554] bcm2708_i2c 20804000.i2c: BSC1 Controller at 0x20804000 (irq 79) (baudrate 100000)
    [    4.929325] i2c /dev entries driver

or:

    $ lsmod | grep i2c
    i2c_dev                 5769  0
    i2c_bcm2708             4943  0
    regmap_i2c              1661  3 snd_soc_pcm512x,snd_soc_wm8804,snd_soc_core

If you have no kernel modules listed and nothing is showing using
`dmesg` then this implies the kernel I2C driver is not loaded. Enable
the I2C as follows:

1.  Run `sudo raspi-config`
2.  Use the down arrow to select `9 Advanced Options`
3.  Arrow down to `A7 I2C`
4.  Select **yes** when it asks you to enable I2C
5.  Also select **yes** when it asks about automatically loading the
    kernel module
6.  Use the right arrow to select the **\<Finish\>** button
7.  Select **yes** when it asks to reboot

After rebooting re-check that the `dmesg | grep i2c` command shows
whether I2C driver is loaded before proceeding.

Optionally, to improve permformance, increase the I2C baudrate from the
default of 100KHz to 400KHz by altering `/boot/config.txt` to include:

    dtparam=i2c_arm=on,i2c_baudrate=400000

Then reboot.

Then add your user to the i2c group:

    $ sudo adduser pi i2c

Install some packages:

    $ sudo apt-get install i2c-tools

Next check that the device is communicating properly (if using a rev.1
board, use 0 for the bus not 1):

    $ i2cdetect -y 1
           0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
      00:          -- -- -- -- -- -- -- -- -- -- -- -- --
      10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
      20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
      30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
      40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
      50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
      60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
      70: -- -- -- -- -- -- 76 --

### Local Installation

Copy `system/provisioning/install.sh` to the device that will be connected to the radio and run it.
Note this install, enable, and start a systemd service immediately. Ensure that all system configuration is handled
before running this script.

### Environment Variables

Note these variables are usually set with an `/etc/default` file by the install script but they can be set
manually for testing or alternate methods of installation.

| Variable           | Service | Description                             | Default      |
|--------------------|---------|-----------------------------------------|--------------|
| ALSA_DEVICE        | Audio   | ALSA Device for audio input and output. | 0            |
| BME280_IC2_PORT    | BME280  | BME280 IC2 Port.                        | 1            |
| BME280_IC2_ADDRESS | BME280  | BME280 IC2 Address.                     | 0x76         |
| SDS011_DEV         | SDS011  | SDS011 dev file                         | /dev/ttyUSB0 |