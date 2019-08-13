# How to connect to your Raspberry Pi remotely

## Introduction

Up to now, we have been using the Pi while it is connected to a dedicated screen, keyboard, and mouse. In many cases, this is either not practical or it is simply unnecessary, as the most common use case for a Pi is as an application server. As such, the Pi will mostly be running either dedicated IO programs or it will be running higher level management programs that talk to other remote IO platforms (such as the Arduino).
Neihter of these use cases requires a graphical interface that runs directly on the Pi. It would even be preferable to run a graphical interface as a web site, in which case a direct connection is most definitely not needed.

Running the Pi without a dedicated screen, keyboard, and mouse is called running it in "headless" mode. But, if we are not able to interact directly with the Pi, how would we go about creating and running programs on the Pi? This is exactly the question that is answered in this lesson.

## Connection methods

### Overview

There are many ways of connecting to remote computers, none of them specific to the Rapsberry Pi. These methods were developed over time to solve two fundamental problems:

1. How can I execute commands on a remote system?
2. How can I create a copy of a local file on a remote system?

A third problem was added later, namely, "how can I see the GUI/desktop of a remote system?".

Most methods of connecting remotely solve one of the two problems, and in some cases they solve one problem well and the other partially (and in a limited way). We will therefore discuss both methods that solve the command execution problem, as well as other methods that solve the file transfer problem. We will also briefly discuss remote graphical interfaces, although most of you should be familiar with this already.

The methods we will be covering are as follows:

1. Remote command execution
   1. SSH
2. Remote file transfer
   1. SCP
   2. FTP
   3. Git
   4. Samba
3. Remote graphical interface
   1. VNC

### SSH

### FTP

### SCP

### Git

### File Sharing (Samba)

### VNC

## Remote Development

### VS Code Remote

#### Prerequisites

#### Installation

#### Use
