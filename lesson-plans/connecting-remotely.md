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
   1. SFTP
   2. SSHFS
   3. SCP
   4. FTP
   5. Git
   6. Samba
3. Remote graphical interface
   1. VNC

You can also get some basic info about these methods at the [official Raspberry Pi documentation][raspi-remote-access] on remote access.

### SSH

#### What is SSH

SSH is short for *Secure SHell*. It is a protocol designed to securely connect to a remote computer over an insecure network (such as the internet). It follows the client-server architecture, which means that one computer must run an ssh server (a program that listens for, and authenticates incoming ssh connections), and the other must run an ssh client (this used to be PuTTY on Windows, but Windows 10 now includes OpenSSH by default).
The client initiates a connection request to the server, which then responds with a request for a username and password. If a correct username and password is then supplied by the client, the server creates a secure connection. The client can then use this secure connection to send commands to the remote computer, **which will execute on the remote computer as if you were logged in directly**.

SSH was created to replace insecure remote shell applications, such as Telnet, rlogin, rsh, etc. It was later extended to also allow for file transfer using SFTP (SSH File Transfer Protocol). In addition to remote command execution, it also allows tunneling, TCP port forwarding, and X11 (remote desktop for linux).

The SSH protocol communicates over TCP port 22 by default, although it can be configured to use any other port.

#### How to use SSH

SSH is installed by default on the Raspberry Pi, although it is also disabled by default for security reasons (due to the commonly known default username and password for the Pi). As discussed in the "Getting Started" lesson, SSH can be enabled by creating an empty file called `ssh` in the root directory of the SD card before booting for the first time. It can also be enabled by using the `raspi-config` command, then selecting the `Interfacing Options` entry and finally selecting `YES` next to `SSH`. Exiting the utility (select `OK` and then `Finish`) will cause the Pi to reboot, upon which SSH will be enabled.
It is important that the default password **must be changed** when enabling SSH, especially if you are planning on connecting your Pi to the internet. The default password for the `pi` user is commonly known and if it is not changed, it will allow *anyone* to access you Pi via SSH (as long as they also know your Pi's IP address).

You can find more information on enabling SSH in the official Raspberry Pi [SSH documentation][official-ssh]

##### Setting up a connection

In order to connect to a remote computer using SSH, you need three things. These are the IP address of the remote system, the username of a valid user on the remote system, and the password of the remote user. You also need to be connected to the same network as the remote system (i.e. the remote system must be "reachable" from your local system)
The IP address of a Raspberry can be found using the `hostname` command, which will print the IP address on the next line, like so:

```bash
pi@raspberry:~ $ hostname -I
192.168.0.1
pi@raspberry:~ $
```

Once the IP address is known, you can initiate an SSH connection using the command `ssh <user>@<host>`. This will attempt to connect to the remote system specified by `<host>` as the user `<user>`. You will then be prompted for the password that belongs to `<user>` and, if you enter the correct password, you will be connected to the remote system as if you had logged into a terminal directly.

```bash
me@localsystem:~ $ ssh pi@192.168.0.1
password:
pi@192.168.0.1:~ $
```

Any commands that you execute in the terminal will now be executed on the remote system and not on your local system.

As mentioned previously, the OpenSSH client is now installed by default in Windows 10. This means that the `ssh` command can be executed directly via the Windows command line, and that you can execute Linux commands (on the remote system) after connecting.

##### Connecting without a password

SSH uses public-private key encryption in order to secure the connection between the local and the remote system. This means that the client side of the connection has a private and a public key pair, and an identity associated with this key pair. Each message is encrypted using the public key, but can only be decrypted by the private key.
When authenticating an SSH connection with a password, such a public-private key pair (with an associated identity) is automatically generated and used for the duration of the connection. It is discarded after the connection is closed and a new key pair will be generated when a new connection is established.

It is also possible to manually generate a public-private key pair on the local system and then store this key on the remote system in some way. When the local system (client) attempts to connect to a remote system (server) where the client's public key had been previously stored, the SSH server compares the identity associated with the stored key to the identity associated with the connection key. If the identities match, then the connection is allowed, otherwise it is rejected.

The authorised SSH keys on a Linux system are usually stored in the `authorized_keys` file in the `~/.ssh/` folder (i.e. `~/.ssh/authorized_keys`). In order to allow key based authentication, it is thus necessary to generate a key pair on your local system and then place a copy of the public key in the `authorized_keys` file on the remote system.

In order to generate a public-private key pair, you can do the following:

###### Windows

The public key is usually stored at `%USERPROFILE%\.ssh\id_rsa.pub`. If you do not have such a key, you can generate it by doing the following:

1. In a command prompt, enter the following

   ```bash
   ssh-keygen -t rsa -b 4096
   ```

   this will generate the `id_rsa.pub` file with a new key inside.
2. Copy the generated public key to the `authorized_keys` file on the remote system

   ```bash
   #replace <user> and <host> with the appropriate remote hostname (IP) and required user
   scp %USERPROFILE%\.ssh\id_rsa.pub <user>@<host>:~/tmp.pub
   ssh <user>@<host> "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat ~/tmp.pub >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys && rm -f ~/tmp.pub"
   ```

###### Linux

1. Enter the following on a terminal

   ```bash
   ssh-keygen -t rsa -b 4096
   ```

   this will generate the `~/.ssh/id_rsa.pub` file with the new key inside
2. Then copy the public key to the remote system

   ```bash
   ssh-copy-id <user>@<host>
   ```

Any new SSH connection will now use the public key stored in `~/.ssh/authorized_keys` to authenticate the connection request and no password will be requested.

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

[official-ssh]:https://www.raspberrypi.org/documentation/remote-access/ssh/README.md
