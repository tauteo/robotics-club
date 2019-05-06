# Getting started with Raspberry Pi

## OS installation
Before you can use your Raspberry Pi, you must load an operating system (OS) onto the SD card.

### OS options
There are several options of operating systems available to run on the Raspberry Pi. The basic options are:
1. Raspbian (official OS)
2. Ubuntu MATE
3. Windows 10 IoT Core (not a full version of windows)
4. OSMC (Open Source Media Centre)
5. LibreELEC (just enough Linux for Kodi...)
...and many more

We will be using Raspbian, which is based on the Debian distrubution of Linux. The current version of Raspbian is named "Strectch".

### OS download options
There are three main "versions" (or rather version configurations) available for Raspbian:
1. Raspbian with desktop and recommended software (i.e. Python, Scratch, Sonic Pi, Java, etc.)
2. Raspbian with desktop
3. Raspbian Lite (without desktop, i.e. command line only)

I recommend that you download option 1 [here][raspi-downloads]

### Installing an OS
In order to load the OS image onto the SD card, you can follow one of two methods.

**Method 1:**
1. Download a program to flash an .iso or .zip image onto an SD card. It is recommended to use the [balenaEtcher][etcher] program.
2. Insert the SD card that you want to load the OS onto into your computer's memory card reader.
3. Run the balenaEtcher program and specify the OS image that you have downloaded, as well as the drive letter of the SD card.
4. Click "Flash" and wait for the image to be written to the SD card
5. Remove the SD card by clicking on "remove safely" in the taskbar, then remove the SD card from your computer
6. Insert the SD card into the Raspberry Pi, connect your screen, keyboard, and mouse and then power up the Pi
7. You should see some text on the screen and four raspberries in the top left hand corner:  
![four-raspberries][raspberries]
8. After some time, you should see the Raspbian desktop appear
![raspbian desktop][pi-desktop]

**Method 2:**
1. Download the NOOBS (New Out Of Box Software) image [here][noobs-downloads]
   1. There are two options: NOOBS and NOOBS Lite
   2. I recommend that you download NOOBS as this will allow for an offline (i.e. not connected to the internet) install
2. Format your SD card using [this formatter][sd-formatter]
3. Unzip the NOOBS image
4. Copy the unzipped files (not the parent folder) onto the SD card
5. Safely remove the SD card and insert it into the Pi
6. Connect your screen, keyboard, and mouse
7. Power up the Pi
8. Select Raspbian Full on the NOOBS screen and click on Install
![noobs installation screen][noobs-install]
9.  Accept the warning and wait for the OS installation to complete
![noobs installing raspbian][noobs-installing]
10. Click OK  
![noobs install complete][noobs-installed]
11. The Raspbian desktop will appear after some time
![raspbian desktop][pi-desktop]

### Updates

## Configuration
### Using the built in utility
1. Locale
2. Memory
3. VNC
4. Communication protocols


### Offline config
1. SSH
2. WiFi

## Software overview

## Hardware overview

[raspi-downloads]: https://www.raspberrypi.org/downloads/raspbian/
[noobs-downloads]: https://www.raspberrypi.org/downloads/noobs/
[etcher]: https://www.balena.io/etcher/
[sd-formatter]:  https://www.sdcard.org/downloads/formatter/index.html

[raspberries]: ../static/images/raspberries.png "four raspberries"
[noobs-install]: ../static/images/install.png "noobs install screen"
[noobs-installing]: ../static/images/installing.png "noobs installing screen"
[noobs-installed]: ../static/images/installed.png "noobs install complete screen"
[pi-desktop]: ../static/images/pi-desktop.png "pi desktop"
[pi-labelled]: ../static/images/pi-labelled.png "labelled raspberry pi layout"
[pi-pinout]: ../static/images/raspberry-pi-pinout.png "raspberry pi pinout"
[pinout-command]: ../static/images/gpiozero-pinout.png "pinout command screen"