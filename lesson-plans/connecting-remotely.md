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

FTP (File Transfer Protocol) is a method that is used to transfer files from one system to another system. It can provide access to files with or without authentication (usually by password) and used to be the de-facto standard for transfering files between sysytems. Due to the fact that it is not as secure as some other protocols, people have started using other methods to transfer files.  
FTP also uses a client-server architecture. As such, an FTP server needs to be installed on the remote machine in order to allow clients on other machines to access files there.

Unlike SSH, FTP is not installed on the Pi by default. You can install an FTP server as follows:

```bash
pi@raspberry:~ $ sudo apt install pure-ftpd
```

There are some additional configuration steps after the serve is installed. The configuration steps are as follows:

1. Create a new user that will be used for FTP access **only**
2. Create a new group to which to add this user
3. Set an FTP base directory
4. Set a user alias for uploading files
5. Define an authentication method
6. Complete additional configuration

The commands to achieve this are as follows:

```bash
# create the ftp group and user. the user must not be able to login and must have no home directory
pi@raspberry:~ $ sudo groupadd ftpgroup
pi@raspberry:~ $ sudo useradd ftpuser -g ftpgroup -s /sbin/nologin -d /dev/null
# make a base ftp directory and make it accessible to ftpuser
pi@raspberry:~ $ sudo mkdir /home/pi/FTP
pi@raspberry:~ $ sudo chown -R ftpuser:ftpgroup /home/pi/FTP
# create an alias (virtual user) for uploading files. enter a password when prompted
pi@raspberry:~ $ sudo pure-pw useradd upload -u ftpuser - ftpgroup -d /home/pi/FTP -m
password:
confirm:
# set up a virtual user database
pi@raspberry:~ $ sudo pure-pw mkdb
# define an authentication method by linking to the ftp authentication DB
pi@raspberry:~ $ sudo ln -s /etc/pure-ftpd/conf/PureDB /etc/pure-ftpd/auth 1puredb
# restart the ftp server
pi@raspberry:~ $ sudo service pure-ftpd restart
```

Additional configurations can be applied by creating a file with the name of the configuration option in the `/etc/pure-ftpd/conf/` directory.

1. ChrootEveryone
   1. Make a file called `ChrootEveryone` in the `/etc/pure-ftpd/conf/` directory
   2. Edit the file and type `yes`
   3. Save the file and exit `Ctrl + X` and then `Y` and `Enter`
2. NoAnonymous
   1. Make a file called `NoAnonymous` in the `/etc/pure-ftpd/conf/` directory
   2. Edit the file and type `yes`
   3. Save the file and exit `Ctrl + X` and then `Y` and `Enter`
3. AnonymousCanCreateDirs
   1. Make a file called `AnonymousCanCreateDirs` in the `/etc/pure-ftpd/conf/` directory
   2. Edit the file and type `no`
   3. Save the file and exit `Ctrl + X` and then `Y` and `Enter`
4. DisplayDotFiles
   1. Make a file called `DisplayDotFiles` in the `/etc/pure-ftpd/conf/` directory
   2. Edit the file and type `no`
   3. Save the file and exit `Ctrl + X` and then `Y` and `Enter`
5. DontResolve
   1. Make a file called `DontResolve` in the `/etc/pure-ftpd/conf/` directory
   2. Edit the file and type `yes`
   3. Save the file and exit `Ctrl + X` and then `Y` and `Enter`
6. ProhibitDotFilesRead
   1. Make a file called `ProhibitDotFilesRead` in the `/etc/pure-ftpd/conf/` directory
   2. Edit the file and type `yes`
   3. Save the file and exit `Ctrl + X` and then `Y` and `Enter`
7. ProhibitDotFilesWrite
   1. Make a file called `ProhibitDotFilesWrite` in the `/etc/pure-ftpd/conf/` directory
   2. Edit the file and type `yes`
   3. Save the file and exit `Ctrl + X` and then `Y` and `Enter`
8. FSCharset
   1. Make a file called `FSCharset` in the `/etc/pure-ftpd/conf/` directory
   2. Edit the file and type `UTF8`
   3. Save the file and exit `Ctrl + X` and then `Y` and `Enter`

Restart the server again:

```bash
pi@raspberry:~ $ sudo service pure-ftpd restart
```

You should now be able to transfer files to and from the Raspberry Pi using an FTP client like FileZilla (remember to use the `upload` user and password that you created previously)

### SCP

SCP (Secure Copy Protocol) is a protocol that is based on SSH, but which is designed for secure file transfer between two hosts (local<->remote, remote<->remote). As it uses SSH for the actual transfer, it is secured using the same method as SSH.

Copying files to another system is easy and follows the basic format `scp <sourcefile> <user>@<host>:[directory]<destinationfile>`. For example:

```bash
# copying blink.py from local computer to ~/projects/ directory on remote computer
# the projects/ directory must exist on the remote computer
scp blink.py pi@192.168.0.1:projects/
```

Copying files from another system is simply the reverse (`scp <user>@<host>:[directory]<sourcefile> <destiniationfile>`):

```bash
# copy ~/projects/blink.py from remote computer to current directory on the local computer
scp pi@192.168.0.1:projects/blink.py .
```

You can also copy multiple files at once:

```bash
# copy files file1.txt and file2.txt to pi user's home directory
scp file1.txt file2.txt pi@192.168.0.1:
# copy all files ending in .txt
scp *.txt pi@192.168.0.1:
# copy all files starting with 'm'
scp m* pi@192.168.0.1:
# copy all files starting with 'm' and with extension .txt
scp m*.txt pi@192.168.0.1:
```

Filenames with spaces need to be wrapped in quotation marks `"`:

```bash
scp "my file.txt" pi@192.168.0.1:
```

### SFTP

SFTP (SSH File Transfer Protocol) provides file access, file transfer and file management over SSH. It is easier to set up than FTP, especially if SSH is already enabled.  
The easiest way to use SFTP is with the [WinSCP][winscp-home] client. This client will allow you to browse and transfer files, to and from, the Raspberry Pi using a username and password or using the public key setup described in the SSH section.

### SSHFS

SSHFS (SSH File System) allows you to mount and interact with files and folders (directories) that are located on a remote system, using SSH as a protocol. The interaction between client and server happens via SFTP.

You can use SSHFS from either a Linux or a Windows client, although a Linux client is somewhat easier.

#### Linux SSHFS

First install SSHFS:

```bash
me:~ $ sudo apt install sshfs
```

Then create a mount directory and mount the sshfs remote directory:

```bash
# create a directory to hold all of the pi files
me:~ $ mkdir pi
# mount the pi's filesystem to this directory
me:~ $ sshfs pi@192.168.0.1: pi
```

You can now use the directory as if it were a local directory:

```bash
# move into the pi directory
me:~ $ cd pi
# you are now in the pi user's home directory on the remote
# any filesystem commands you execute will be done on the remote
# programs that you run will still be run on your local system
me:~/pi $ ls
```

This will also mount the pi's filesystem for use by your graphical file manager, and supports things like drag-and-drop to copy files between systems. You can also use your local graphical editors to edit files on the pi's filesystem.

#### Windows SSHFS

Using SSHFS is slightly more complicated to install, but just as easy to use.

First, install the *stable* release of [WinFSP][winfsp-install].  
Second, install the *stable* release of [SSHFS-Win][sshfswin-install].

Once these two programs are installed, you can map a remote drive using the normal "map network drive" method. Enter the string `\\sshfs\<user>@<host>` in the `Folder` text box in the `map network drive` dialog. This will map the home folder of the user you specified to the drive letter you specified.  
Remember to choose `connect using different credentials` in order to specify the username and password of the remote machine. This method does not currently support key-based authentication in Windows.

### Git

### File Sharing (Samba)

### VNC

## Remote Development

### VS Code Remote

#### Prerequisites

#### Installation

#### Use

[official-ssh]:https://www.raspberrypi.org/documentation/remote-access/ssh/README.md
