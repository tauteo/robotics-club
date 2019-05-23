# An overview of Linux

## Kernel structure
![kernel architecture][kernel-arch]

Linux is known as a modular operating system. This means that different sections of the operating system are independent of each other and can theoretically be swapped out with a different component which does the same thing. For example, if you would like to use a different file system type, then you can include the new type and rebuild the kernel.

The components that support this type of modularity are the file system types, block devices (i.e. how bits are written to storage), character devices (i.e. how characters are read and displayed), and interface drivers (i.e. how the OS connects to other systems via a network).

All of these modules form the base of the operating system, but none of these systems are directly accessible from the user space. In order to allow access from higher levels, the base levels are abstracted into kernel subsystems (such as the virtual file system, virtual memory system and process management system). These subsystems have direct access to the base systems.

Direct access to the kernel subsystems is also not possible from the user space. Instead, there is another layer of abstraction between the user and the kernel subsystems called the "system call interface". The user can access subsystem functions by using this standardised abstraction.

## File system
### Structure
![linux file system structure][filesys-structure]

The linux file system is built on top of the virtual file system kernel subsystem. As such, it does not start with direct access to physical devices (like C:) like in Windows. Like most file systems, the linux file system is a tree structure.

Like any tree, the structure starts at the root. This level is indicated simply by "/" (note the forward slash instead of the backslash that is used in Windows). The root directory (also called a folder in Windows) contains all of the base directories that make up the file system. Each base directory is responsible for keeping files related to a specific task (such as configuration, temporary files, programs etc.).

The base directories and their functions are listed below:
1. **/bin**  
   Contains essential binaries (compiled programs) that are necessary for the system to work. This includes programs that for example list file contents, change file ownership, mount new file systems and so on
2. **/sbin**  
    This directory is similar to the `/bin` directory in the sense that it contains compiled programs (i.e. binaries). The difference is that all programs intended to be run by the "root" user for system administration are placed here.
2. **/boot**  
   This contains static files needed to boot up the system, such as the `initd` file which specifies in which order programs need to be started after booting and what resources need to be available before these programs can be started.
3. **/etc**  
   Contains all of the configuration files, including the boot configuration files, needed to run the system. The configurations specified here apply to all users. They are generally text files and can be edited if you should want to change some configuration.
4. **/dev**  
   Linux exposes devices as files, and this directory contains a number of special files that represent devices. These are not actual files as we know them, but they appear as files. A good example of this is the `/dev/sda` file which represents a physical storage drive connected to the system.
   This directory also contains pseudo devices like `/dev/random` (which produces a random number when read) and `/dev/null` which produces no output and discards all input.
5. **/home**  
   This directory contains a subdirectory for each user that is registered on the system. The `pi` user on the Raspberry Pi therefore has a subdirectory called `/home/pi`, which is located here.
   You will typically place all of the files that you work on here as files created here are only accessible by yourself.

   It is also important to note that a user generally does not have write access to files located elsewhere.
6. **/lib**  
   All of the libraries needed by the programs on the system (i.e. in `/bin` and `/sbin`) are stored here.
7. **/media**  
   Contains a subdirectory for every removable media device (i.e. flash drives, or CDs) that is connected to the system. These subdirectories are created automatically when the media is inserted.
8. **/mnt**  
   All temporary mount points go here. This is typically used when mounting a temporary file system such as a folder or drive shared via the network (typically from another OS like Windows).

   It must be noted that this is a convention only and that a mount point can be created anywhere on the system.
9. **/opt**  
    This contains subdirectories for optional software that is installed by the user and which doesn't follow the standard file system hierarchy.
10. **/root**  
    This is the home directory for a special user called "root" (different to the file system root `/`). The "root" user has special access to all system files (but not to necessarily to user files).
11. **/usr**  
    All applications and files used by users (as opposed to being used by the system) are placed here. In other words, programs located here are deemed to be non-essential.

    Programs are again separated into general programs (located in `/usr/bin`) and system administration programs (located in `/usr/sbin`). Libraries for programs in both these locations are located in `/usr/lib`. Programs that are compiled locally are installed to `/usr/local` to prevent them from interfering with system programs.
12. **/var**  
    This directory contains all variable data files. This is typically where log files are written to (under `/var/log`).
13. **/tmp**  
    All temporary files are stored here and are typically deleted when the system is restarted or by cleanup programs such as `tmpwatch`.
14. **/proc**  
    Contains information on running processes.

### Paths
File paths are a set of directions that specify where to find the file that you want. As with any set of directions, you can provide them from either a fixed point of reference (e.g. if you start at the mall and drive towards the highway) or from your current position (e.g. from here, take a left to the mall and then continue to the highway).

In linux, the fixed point of reference is always the root `/` of the filesystem. An example of a path specified in this way is `/home/pi/programs/blink.py`. As you can see it starts with the `/`, then adds on a step `/home`. This process is repeated (i.e. `/home/pi`, then `/home/pi/programs`, and finally `/home/pi/programs/blink.py`) until the destination file `blink.py` is reached. This form of specifying a path (providing directions to a file) is called "absolute addressing", as it starts from an absolute point of reference.

The second method of providing directions to a file is called relative addressing (as it is in relation to your current position in the filesystem). In order to use this method effectively, you need two short cuts.

The first short cut is called `.`, it specifies the current directory. An example of this would be if you are already in the `/home/pi` directory and want to navigate to the `blink.py` file in the previous example. Using relative addressing, this can be written as `./programs/blink.py` (you can also use an even shorter route and just write `programs/blink.py`)

The second shortcut is called `..` and it means the parent directory or the directory that contains the current directory. Let's assume that we are in the directory `/home/pi/notes` and that we want to move from there to the `/home/pi/programs` directory. We can write that, in the relative form, as `../programs/blink.py`. Which simply means "go one directory up from where I am currently" (i.e. move from `/home/pi/notes` to `/home/pi`) and then go into the subdirectory called `programs`.

If you get lost on the path, then simply return to the root `/` or return to your home directory, which can be accessed with the short cut `~`.

### File types
As mentioned previously, everything in linux is represented with a file. A file simply means anything that stores information, whether that be information on other files and directories (which is what a directory is), bytes and information (a "regular" file) or access to a stream of data (like a network connection).

Most files actually contain information that is stored as bytes that have no special meaning to humans, but which have a very specific meaning to the computer. These files are called binary files (e.g. compiled programs, a music file and so on). Some files do contain information that is meaningful to humans, usually in the form of text (e.g. config files, reports etc.).

You can see that files in linux are slightly different to how you used to think of a file in Windows. Another difference is that files in linux do not require an extension (e.g. the `.py` part in `blink.py`). Extensions are only used as conventions and maintain some sanity, but do not restrict the use of the file at all. Some conventions are to label Python files with the `.py` extension, C files with the `.c` extension, configuration files with the `.conf` extension and so on.

## Terminal commands
Up to now, the discussion has been rather abstract and you have not really seen anything which you can use to control a linux system. That changes shortly.

We will begin by learning commands that allow us to move around the file system. We will then move on to working with files (i.e. create, read, edit, delete). Later on we will discuss how to create and manage users and access to files, as well as how to get help if you are stuck with a command. Finally, we will learn how to identify and manage processes.

But first, a short introduction to the shell is needed.
### The shell
The shell is the outermost layer of any linux system. It is a program that can read commands typed in plain (well, somewhat plain) language and translate it into commands that the system understands.

All shell commands are typed into the terminal, which is itself a program that allows interaction with the shell using a keyboard and a screen.

The input to a terminal is usually identified by your username, the directory you are currently in and the prompt (which is normally the symbol `$`, but can be any of the symbols `>`, `%`, `#`). A prompt in a terminal usually looks like the following:
![raspberry pi terminal][raspi-terminal]

The commands that you type into the terminal are usually the names of programs to run. The shell then runs the program and then displays the output of the program on the terminal. After the output is displayed, the terminal then displays the prompt again.

In addition to running commands that you type into the terminal, the shell does some other things as well. Some of the most useful are:
1. **Keeping history**  
   The shell keeps a history of all of the commands that you enter into the terminal. You can view the history by typing `history` into the terminal (i.e. running the `history` command). You can also view previous commands by cycling through them with the up and down arrow keys.
2. **Command completion**  
   It is not always necessary to type a command in full as the shell knows which commands are available. It will automatically fill in the command if you start typing the first few characters of the command and then press the `Tab` key. If the letters that you typed so far are too generic (in other words, more than one command starts with that combination), the shell will not know which specific command you want to enter. In this case, you can then press the `Tab` key twice, which will give you a list of available commands starting with the combination you entered (this is useful if you forgot the full command but remember how it started). Command completion also works for file and directory names.
3. **Environment variables**
   The shell keeps a list of variables in the background that are used to set up the execution environment for the terminal session. These variables are identified by the `$` sign and an all caps name, e.g. `$SHELL` (which contains the path to the shell executable, this should be `/bin/bash` on the pi). Another important variable is `$PATH`, which contains a list of directories where the shell will look for binaries (compiled programs that can be run from the shell).

### Moving around
### Working with files
### The shell
### Partitions
### Users and access restrictions
### Reading the manual
### Combining instructions
### Process management

[kernel-arch]: ../static/images/linux-kernel-architecture.png "linux kernel architecture"
[filesys-structure]: ../static/images/linux-file-system.jpg "linux file system structure"
