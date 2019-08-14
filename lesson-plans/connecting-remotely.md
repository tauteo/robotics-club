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

Git is neither a remote command execution protocol nor a remote file transfer protocol. Instead, it is a distributed version control platform. You should get into the habit of using a version control system for all of your projects, as this will help you to keep track of how your project has evolved over time and what changes have been made to which files. This is immensely important when you start working on larger projects with other people, especially if some of you are working on the same source files at the same time.
I will not write an in depth tutorial on using git here, as there are many better tutorials on the internet. Here are links to some of them:

* [Try Git][try-github]
* [Git Internals PDF][git-internals-pdf]
* [A visual guide to Git][visual-git]
* [Thinking in Git][think-git]
* [5 Git tutorials for beginners][git-tutorials-medium]
* [Git tutorials repo][git-tutorials-repo]

We have already been using Git in the sense that these documents are stored on GitHub, which is a Git repository management system in the cloud (i.e. on the internet). Git is also installed on the Raspberry Pi by default, so you shouldn't need much to get started.

The basic workflow that you can follow if you use Git to manage your source code is as follows:

1. Make a change to your source code
2. Commit this change to your local git repository
3. Push the change to your GitHub repository
4. Pull the code from your GitHub repository to your Raspberry Pi
5. The code is now on your Pi and you can compile/run it as if you had created it directly on the Pi.

### SMB/CIFS

This is a networking protocol which is used by Windows to provide share access to things like files, printers, serial ports and so on. An implementation of this protocol which can be installed on Linux is Samba. The Samba implementation can be used to mount a shared Windows folder on the Raspberry Pi, thus giving you access to files which were created in Windows. It can also be used to share a directory on the Pi, so that it can be accessed by a Windows client.

Samba is not installed on the Pi by default, so in order to use it, we first need to install it:

```bash
pi@raspberry:~ $ sudo apt update
pi@raspberry:~ $ sudo apt install samba samba-common-bin smbclient cifs-utils
```

In order to access a folder on a Windows machine, we first need to share a folder on Windows. Once we have shared a folder, we can mount it on the Raspberry Pi:

```bash
# first create a directory that will be used as a mount point
pi@raspberry:~ $ mkdir windowshare
# then mount the shared Windows folder to the new directory
# the <hostname> is the ip address of your Windows machine
# you must also provide the name of the Windows user that will be used to access the shared folder
pi@raspberry:~ $ sudo mount.cifs //<hostname>/<sharedfoldername> /home/pi/windowshare -o user=<windowsusername>
# the shared folder is now mounted and you can access is like you would any other directory on the Pi
pi@raspberry:~ $ cd windowshare
pi@raspberry:~ $ ls
```

In order to share a directory from the Pi that you will access on Windows, you need to do the following:

```bash
# first create a folder to be shared
pi@raspberry:~ $ mkdir shared
# then edit the samba config to share the new folder
pi@raspberry:~ $ sudo nano /etc/samba/smb.conf
```

The following should be appended (i.e. added to the end) of the `smb.conf` file:

```text
[share]
    path = /home/pi/shared
    read only = no
    public = yes
    writable = yes
```

You should also edit the `workgroup` entry in the `smb.conf` file:

```text
workgroup = <your workgroup name>
```

The shared folder should now appear on your Windows machine under "*Network*". You can also map this as a network drive.

### VNC

VNC (Virtual Network Computing) is a protocol designed to provide remote access to a graphical user interface (desktop) on another system. VNC is also a client-server protocol, which means that a VNC client can connect to an instance of a VNC server which is installed on a remote system.
RealVNC is an implementation of the VNC protocol and is installed on the Pi by default. It includes both a server and a client component, which means that you can VNC to your Pi's desktop from another machine, and also VNC to another machine from your Pi.  
It is important to note that if the Raspberry Pi is started in "headless" mode (i.e. without a screen connected to it), it will not actually have a desktop running to which you can VNC. You can overcome this problem by starting a "*virtual desktop*" and then connecting to this.

Although VNC is installed by default, it is also disabled by default. You can enable it as follows:

```bash
# first make sure that the latest version is installed
pi@raspberry:~ $ sudo apt update
pi@raspberry:~ $ sudo apt install realvnc-vnc-server realvnc-vnc-viewer
# then run the config utility
pi@raspberry:~ $ sudo raspi-config
```

Navigate to `Interfacing Options` in the config utility, then select `Yes` next to the `VNC` entry. Exiting the config utility should restart your Pi.

In order to connect from Windows, you will need to download [VNC Viewer][vnc-viewer]. You can then connect to the Pi directly by simply entering the Pi's IP address into the viewer and connecting. This will prompt you for a username and password, where you can simply enter the values that you use to normally log into the Pi.

To run a virtual desktop (for when you started in "headless" mode), do the following:

1. SSH into your Pi
2. Run the command `vncserver`, and take note of the IP address:display nr which is printed. This will be in the format `192.168.0.1:1`.
3. Enter the IP address:display nr into VNC Viewer on your local machine and connect

You can destroy a virtual desktop by running:

```bash
pi@raspberry:~ $ vncserver -kill :<display-number>
```

This will immediately stop any existing connections to the virtual desktop.

## Remote Development

### Dev Introduction

Up to now, we have been writing programs in one of two ways. Either we have written and compiled the source code directly on the Pi, or we have written the source code on another machine and then transferred it to the Pi for compiling.  
In the first case, writing code on the Pi is not very user friendly. There are graphical editors that run on the Pi, but this requires that the Pi be connected to a dedicated screen, keyboard, and mouse. The alternative is to use a terminal based editor like `nano`, but this is a very restricted way of writing source code. Ideally we would like to be able to write code in a modern editor that provides us with things like syntax highlighting, code completion and so on. The Pi simply does not have the resources to run an editor like this.
This brings us to the second case, where we write source code on another system which has the resources needed to run a modern code editor. The problem with this is that, although we get all of the benefits of a modern editor, we now need to transfer files to and from the Pi and it still does not allow us to do things like debugging our code.

What we need is some way to connect to the Pi from our machine running the modern editor. Specifically, we need to be able to write code in the modern editor, without having to first transfer the source files from the Pi, and then be able to compile and debug the code on the Pi while still interfacing with it from the editor on our local machine.  
This is exactly the problem which has now been solved in one of the preeminent code editors currently available, namely Visual Studio Code.

VS Code is available for download, completely for free, and can run on Windows, Linux, and MacOS. It provides all of the benefits of a modern code editor, and in addition it provides the ability for *anyone* to write an extension that supplements the default capabilities of the editor. One such extension is called is called "VS Code Remote Development", and we will use this extension to be able to run the code editor interface on our local machine, while actually working on the (remote) Raspberry Pi.

### VS Code Remote

![Architecture of the VS Code Remote extension][vscode-remote-arch]

The VS Code Remote extension uses SSH as a tunnel through which to communicate between the local editor and a remote server program that is installed on the Raspberry Pi (or any remote Linux machine, WSL instance, or Docker container). It also requires an OpenSSH compatible client to be installed on the local machine (which Windows 10 has by default and is installable on Linux and MacOS).  
At the moment, there is only experimental support for Linux on ARMv7 (Raspberry Pi 2) and ARMv8 (Raspberry Pi 3B+), but it is quite stable enough to use. The experimental support does require that we use the insiders build of VS Code (which is also stable enough for general use).

#### Installation

To install VS Code follow the instructions for downloading and installing the [insiders release][vscode-insiders].

If SSH is not enabled on your Windows 10 installation, then follow the instructions for [enabling OpenSSH in Windows 10][win10-ssh] and install OpenSSH client.

After installing VS Code Insiders and making sure that SSH is enabled, install the Remote Development extension pack.

The Remote extension requires SSH key based authentication to work. You can follow the instructions under the section [SSH -> How to use SSH -> Connecting without a password -> Windows](#windows) in order to set up key based authentication with your Pi, or you can visit the [VS Code website][vscode-ssh-config] for more detailed instructions.  
Once this is set up, run the command `Remote-SSH:Connect to Host` from the Command Palette (<kbd>F1</kbd>) and enter the `<user>@<host>` combination for your Pi. VS Code will then attempt to establish an SSH connection with the Pi and install the server component on the Pi.

When the SSH connection has been established and the server component installed, VS Code will present you with an empty window. You can then proceed to open any folder or workspace on the Pi from within VS Code. You can also open the integrated terminal in VS Code in order to automatically open a remote terminal on the Pi.

You will also be able to install extensions while in remote mode. Compatible extensions will be installed on the Raspberry Pi itself, while other extensions will be installed on the local machine.

For more information on VS Code Remote, see the [Remote Development using SSH][vscode-remote-ssh] webpage.

---

[official-ssh]:https://www.raspberrypi.org/documentation/remote-access/ssh/README.md
[winscp-home]:https://winscp.net/eng/index.php
[winfsp-install]:https://github.com/billziss-gh/winfsp/releases
[sshfswin-install]:https://github.com/billziss-gh/sshfs-win/releases
[try-github]:http://try.github.io/
[git-internals-pdf]:https://github.com/pluralsight/git-internals-pdf
[visual-git]:http://marklodato.github.io/visual-git-guide/index-en.html
[think-git]:http://think-like-a-git.net/
[git-tutorials-medium]:https://medium.com/quick-code/top-tutorials-to-learn-git-for-beginners-622289ffdfe5
[git-tutorials-repo]:https://gist.github.com/jaseemabid/1321592
[vnc-viewer]:https://www.realvnc.com/en/connect/download/viewer/
[raspi-remote-access]:https://www.raspberrypi.org/documentation/remote-access/
[vscode-insiders]:https://code.visualstudio.com/insiders/
[win10-ssh]:https://docs.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse
[vscode-ssh-config]:https://code.visualstudio.com/docs/remote/troubleshooting#_configuring-key-based-authentication
[vscode-remote-ssh]:https://code.visualstudio.com/docs/remote/ssh

[vscode-remote-arch]:../static/images/vscode-remote-architecture.png "vscode remote architecture"
