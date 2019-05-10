# robotics-club

## Introduction
This repository contains all of the lesson plans for the Raspberry Pi training sessions

In order to follow along, you will need the following as a minimum:
* A Raspberry Pi (I recommend either the 3B or the 3B+)
* A 5V/2.5A micro-USB power supply
* An >=8GB  micro-SD card (I recommend a class 10 SD card as the speed difference will be notable with slower cards)

If you will mainly interface with your Pi via a computer on the same network (wired or wireless), then this is all you need.

If you would like to connect directly to your Pi (this is easier for beginners), then you will also need the following:<sup>1</sup>
* A USB keyboard (wired or wireless)<sup>2</sup>
* A USB mouse (wired or wireless)<sup>2</sup>
* A screen with an HDMI input (RCA works, but with limited resolution. You can also use a HDMI-VGA converter)

Completely optional extras:
* A case

> <sup>1</sup>Please check the [verified peripherals][verified-peripherals] before buying any keyboards, mice, or VGA adapters. Some peripherals are not compatible with Raspberry Pi.

> <sup>2</sup>Some bluetooth keyboards and mice do work, but check the [verified peripherals][verified-peripherals] list to confirm that it is compatible with the Pi.

## Lessons overview
The lessons are divided into the following sections:

1. Getting started
   1. OS installation
   2. Boot
   3. Configuration
   4. Overview (desktop and terminal)
   5. Hardware overview
2. Basic linux commands and usage (ongoing, commands are introduced as needed)
3. Basic projects
   1. Flashing an LED (Python, C, etc.)
   2. The arduino intro projects
4. File transfer between Windows and Raspberry Pi
   1. SCP
   2. FTP
   3. Git
5. Running scheduled scripts
6. Python overview
7. Advanced projects
   1. Python games with graphics
   2. Python and minecraft
   3. Raspberry Pi camera interface
   4. Google AIY
   5. Accessing APIs
   6. Sonic pi
   7. Making and hosting a website (Flask, Django, .Net Core)
   8. Robot car in python
   9. Digital art
   10. Robot arm
   11. Smart mirror
   12. Sound effect box
   13. Internet monitor
   14. Smart alarm clock (perhaps with google calendar integration)
   15. Retro arcade
   16. Media centre
   17. Communicating between programs
   18. IoT (ThingsBoard, NodeRed, Azure IoT)
   19. Web interface for the kWh meter project

Each topic has it's own plan under [lesson-plans][lessons] . The plans are added and updated as needed.

[verified-peripherals]: https://elinux.org/RPi_VerifiedPeripherals
[lessons]: ./lesson-plans/getting-started.md