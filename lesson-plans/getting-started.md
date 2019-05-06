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

### Installing and updating packages
From time to time it will be necessary to upgrade either the operating system or the software packages installed. You may also want to install new software packages (e.g. vnc-server, samba etc.). In order to do this, you will have to use the `apt-get` utility as follows:
```bash
sudo apt-get update
sudo apt-get upgrade
```

`sudo apt-get update` will update the local package manifest by downloading the latest manifest from a distribution repository. This will not actually update any applications.  
`sudo apt-get upgrade` will compare the installed version of all software packages with the latest version in the local manifest. It will then download and install any newer versions that are available from the distribution repository.

## Configuration
### Using the built in utility
The Raspberry Pi has a built-in configuration utility. This utility is used to make certain configuration tasks, such as configuring vnc, i2c, camera etc. easier.
The configuration utility is accessed by either running the graphical interface from the desktop or running the command-line utility.
The graphical interface can be accessed from `Start->Preferences->Raspberry Pi Configuration`.  
![config utility][raspi-config]

The command-line utility can be accessed by typing `sudo raspi-config` into the terminal.

Some of the basic settings that you may need to change are the following:
1. **Password**  
   If you want your password to be different to the default "raspberry". This is a good idea if are going to be connecting your Pi to a network.
2. **Locale**  
   This changes things such as your keyboard layout, time zone, interface language, wifi country code and so on. It is not required to change anything here, although it will default to British English and the GB time zone if you don't (this will mean that your time will always be two hours behind)
3. **Expand filesystem**  
   This changes the amount of memory that is used for file storage on your SD card. Installing Raspbian using the NOOBS installer will do this automatically, but you will need to do it yourself if you followed a different installation method. Importantly **do not** do this after you have started using the Pi, i.e. creating files and installing programs.
4. **VNC**  
   You will not be able to connect to the Pi via VNC until it has been enabled using the config utility. *It is disabled by default*.
5. **Communication protocols**  
   Some communications protocols, such as Camera (CSI), SSH, Remote GPIO, SPI, I2C, Serial, and 1-Wire are disabled by default. You can activate them using the config utility. *You will not be able to use any of these protocols from your code until they have been activated here*.

### Offline config
In some cases, you may wish to enable some settings before booting up the Raspberry Pi. This is generally required if you want to run your Pi without connecting a screen (also called a headless setup).
1. **SSH**  
   If you would like SSH to be enabled without needing to run the `raspi-config` utility, simply copy an empty file called `ssh` onto the boot partition of your SD card. This will enable SSH the next time the Raspberry Pi boots.
2. **WiFi**  
   It is generally recommended that you boot the Pi for the first time while it is connected to an ethernet network. When this is not possible, you can pre-configure a wifi connection by doing the following:
   1. Create a file called `wpa_supplicant.conf` in the boot partition of your SD card
   2. Edit the file to contain the following:
   ```
   network={
     ssid="your-wifi-network-name"
     psk="your-wifi-network-password"
     country=ZA
     #if wifi network has no password, use the following:
     key_mgmt=NONE
     #if using a hidden network, add the following after ssid:
     scan_ssid=1
   }
   ```

## Software overview
The Raspbian operating system comes pre-installed with several programs. Here is a list of programs that are installed and a short description of what they are:
1. **Scratch**  
   This is a visual programming tool which allows the creation of animations and games using drag and drop. It was developed by MIT and the newest version can be found [here][scratch-mit] (note that the new version only runs in the browser and is slightly different from the version on the Pi).
2. **Python**  
   [Python][python] is a general purpose programming langauge that is easy to learn and runs on any platform (Windows, Linux, MacOS). It is a popular language for developing web applications and is also used extensively in machine learning and data science. Python can also be used to program desktop applications and games, although it is usually not the first choice of language to do so.

   It is generally used on the Pi to write programs that interface with the GPIO and even provides an interactive mode that makes understanding and learning what commands do much easier.
3. **Sonic Pi**  
   [Sonic Pi][sonic-pi] is an open-source programming environment, designed for creating new sounds with code in a live coding environment. You can use it to make sounds and music using programming.
4. **Minecraft**  
   Minecraft is a popular sandbox open world building game. A free version of Minecraft is available for the Raspberry Pi; it also comes with a programming interface. This means you can write commands and scripts in Python code to build things in the game automatically.
5. **Python Games**  
   These are examples of games written in Python. The source code for all of the games is available as part of the installation, so you can edit and enhance them or even integrate them with the GPIO.
6. **Mathematica**  
   Mathematica is a computational programming tool used in science, maths, computing and engineering first released in 1988. It is proprietary software that you can use for free on the Raspberry Pi and has been bundled with Raspbian and NOOBS since late 2013.
7. **Wolfram**  
   The Wolfram Language is a general multi-paradigm computational communication languagedeveloped by Wolfram Research and is the programming language of the mathematical symbolic computation program Mathematica and the Wolfram Programming Cloud. It emphasizes symbolic computation, functional programming, and rule-based programming and can employ arbitrary structures and data.

## Hardware overview
The Raspberry Pi consists of several hardware components working together. These are:
1. ARMv8 Cortex-A53 CPU (Broadcom BCM2837B0 SoC in the 3B+)
2. RAM (1GB in the 3B+)
3. Wireless communication (IEEE 802.11.b/g/n/ac wireless LAN, Bluetooth 4.2, BLE)
4. Wired communication (USB 2.0 and Gigabit Ethernet over USB 2.0)
5. SD card reader
6. Video interfaces (HDMI & RCA)
7. Sound interface (3.5mm audio jack)
8. Display interface (DSI)
9. Camera interface (CSI)
10. General Purpose I/O pins (GPIO)

![raspi layout][pi-labelled]

The GPIO pins are rated at 3.3V and a maximum of 16mA (although you will not be able to run all of the pins at this current simultaneously). All of the pins have internal pull-up/pull-down resistors. All of the pins, when configured as a general purpose input, can also be configured as an interrupt source (level, rising/falling edge, asynchronous rising/falling edge).

In practice, some pins are reserved for special uses (and are not available for general purpose use) and some functions (such as the hardware implementations of UART, I2C, and SPI) are fixed to certain pins. In general, the [pinout][interactive-pinout] of the Raspberry Pi is as follows:  
![raspi pinout][pi-pinout]
The green pins are not reserved for any special use (except the ones labelled PWM - Hardware Pulse Width Modulation and GCLK - Hardware General Purpose Clock) and can be used as general purpose I/O. The black pins are reserved for ground. The other coloured pins are fixed to the indicated communications protocol, but can also be configured for general purpose I/O (although this means that you can no longer use them for communications).

If you ever forget the pin layout, there is a handy utility built into the Pi, which is called "pinout". You can always access this utility from the terminal / command line by just typing `pinout`. This will then give you the following printout:
![pinout command][pinout-command]

The numbers on these pinouts use the BCM order and can be used directly to address a specific pin. An alternative numbering layout called "WiringPi" can also be used, although we will generally not be using this layout during this course.

[raspi-downloads]: https://www.raspberrypi.org/downloads/raspbian/
[noobs-downloads]: https://www.raspberrypi.org/downloads/noobs/
[etcher]: https://www.balena.io/etcher/
[sd-formatter]:  https://www.sdcard.org/downloads/formatter/index.html
[interactive-pinout]: https://pinout.xyz/
[scratch-mit]: https://scratch.mit.edu/
[python]: https://python.org
[sonic-pi]: https://projects.raspberrypi.org/en/projects/getting-started-with-sonic-pi

[raspberries]: ../static/images/raspberries.png "four raspberries"
[noobs-install]: ../static/images/install.png "noobs install screen"
[noobs-installing]: ../static/images/installing.png "noobs installing screen"
[noobs-installed]: ../static/images/installed.png "noobs install complete screen"
[pi-desktop]: ../static/images/pi-desktop.png "pi desktop"
[pi-labelled]: ../static/images/pi-labelled.png "labelled raspberry pi layout"
[pi-pinout]: ../static/images/raspberry-pi-pinout.png "raspberry pi pinout"
[pinout-command]: ../static/images/gpiozero-pinout.png "pinout command screen"
[raspi-config]: ../static/images/config.png "raspberry pi config utility"