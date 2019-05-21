# An overview of Linux

## Kernel structure
![kernel architecture][kernel-arch]

Linux is known as a modular operating system. This means that different sections of the operating system are independent of each other and can theoretically be swapped out with a different component which does the same thing. For example, if you would like to use a different file system type, then you can include the new type and rebuild the kernel.

The components that support this type of modularity are the file system types, block devices (i.e. how bits are written to storage), character devices (i.e. how characters are read and displayed), and interface drivers (i.e. how the OS connects to other systems via a network).

All of these modules form the base of the operating system, but none of these systems are directly accessible from the user space. In order to allow access from higher levels, the base levels are abstracted into kernel subsystems (such as the virtual file system, virtual memory system and process management system). These subsystems have direct access to the base systems.

Direct access to the kernel subsystems is also not possible from the user space. Instead, there is another layer of abstraction between the user and the kernel subsystems called the "system call interface". The user can access subsystem functions by using this standardised abstraction.

## File system
### Structure
### Paths
### File types
### File descriptors

## Terminal commands
### Moving around
### Working with files
### The shell
### Partitions
### Users and access restrictions
### Reading the manual
### Combining instructions
### Process management

[kernel-arch]: ../static/images/linux-kernel-architecture.png "linux kernel architecture"
