# How to write programs that access the GPIO on the Raspberry Pi

## Introduction
There are many programming languages with which you can program on the Raspberry Pi and access the GPIO. Not all of these languages are equally well supported on the Pi (especially for GPIO access) and not all of them have good examples available. Some of the most common languages and libraries for accessing the GPIO are as follows:
- `C` [wiringPi, pigpio, bcm2835, direct register access]
- `C#` [RaspberryGPIOManager]
- `Ruby` [wiringPi, Pi Piper]
- `Perl`
- `Python` [gpiozero, RPi.GPIO, pigpio]
- `Scratch` [ScratchGPIO, RpiScratchIO]
- `Java` [Pi4J]
- `Shell` [sysfs, wiringPi gpio utility, pigpio pigs utility, pigpio /dev/pigpio interface, libgpiod]
- `BASIC`

Of these, the two most common languages used are `C` ang `Python`, so we will discuss both of them. For those of you coming from Arduino, the `C` language may be the most familiar.

## GPIO overview

The GPIO pins are rated at 3.3V and a maximum of 16mA (although you will not be able to run all of the pins at this current simultaneously). All of the pins have internal pull-up/pull-down resistors. All of the pins, when configured as a general purpose input, can also be configured as an interrupt source (level, rising/falling edge, asynchronous rising/falling edge).

In practice, some pins are reserved for special uses (and are not available for general purpose use) and some functions (such as the hardware implementations of UART, I2C, and SPI) are fixed to certain pins. In general, the [pinout][interactive-pinout] of the Raspberry Pi is as follows:  
![raspi pinout][pi-pinout]
The green pins are not reserved for any special use (except the ones labelled PWM - Hardware Pulse Width Modulation and GCLK - Hardware General Purpose Clock) and can be used as general purpose I/O. The black pins are reserved for ground. The other coloured pins are fixed to the indicated communications protocol, but can also be configured for general purpose I/O (although this means that you can no longer use them for communications).

If you ever forget the pin layout, there is a handy utility built into the Pi, which is called "pinout". You can always access this utility from the terminal / command line by just typing `pinout`. This will then give you the following printout:  
![pinout command][pinout-command]

The numbers on these pinouts use the BCM order and can be used directly to address a specific pin. An alternative numbering layout called "WiringPi" can also be used, although we will generally not be using this layout during this course.

## Programming in C
### A crash course in C
#### Overview
`C` is a statically typed, compiled, imperative language which excels in low level programming. Most of the Unix kernel is written in `C` and even other languages (like Python) are written in `C`.

"Statically typed" means that each variable is assigned a type (e.g. `int`, `char`, `float` etc.) when the program is written. This type cannot be changed while the program is running and any attempt at assigning a value of the wrong type to that variable will result in the program failing to compile.

"Compiled" means that the code you type must first be converted into what is called "machine language". This is a sequence of instructions that the processor understands how to execute, but which would be very hard for a human programmer to write (as it is represented in binary). There are many compilers for `C`, but one of the most common is called `gcc` (Gnu C Compiler). This compiler is included by default in the Raspbian distribution we are using on the Raspberry Pi.

"Imperative" means that the program is a list of instructions that is executed from top to bottom in sequence. Every statement that you write is a direct instruction to do something. If the statement is evaluated successfully, the statement that follows is evaluated and so on, and so on.

#### Structure
`C` is a block structured language where blocks of code that execute in the same context (also called scope) are grouped together using a matching pair of `{ }` brackets. In addition to this, every statement in `C` must be terminated by a semicolon `;`.

*Main function*  
All `C` programs that will be executed, in other words not a code library, **must** contain a `main` function. This is the first function that will be executed when the program is run. The main function can have many different forms, but like all functions in `C`, it must have a return type (which cannot be `void`) and a list of parameters. Like so:
```c
//return type = int (meaning it will return an integer value)
int main(void)
{

}

//return type = int
//parameters = int argc (representing a count of the number of argument given to the program when it is run), and char argv[] (representing an array of strings passed as arguments to the program when it is run)
int main(int argc, char *argv[])
{

}
```
Of these forms, the most common is `int main(int argc, char *argv[])`.

*Source files*  
All `C` code is written in a file with a `.c` extension and a valid `C` program must have at least one `.c` file (which you can name as you wish, as long as it adheres to the operating system specifications for allowed file names). We could, for example, name a file `blink.c` to convey the message that the program it contains will "blink" something.

You can optionally put your code in more than one source (`.c`) file, but you must then reference all of these additional source files when compiling your program. Only one main function is allowed (so only one of the source files should contain the `main` function).

In addition to `.c` files, the `C` language also uses `.h` files (also called header files). These files may not contain any expressions, but are generally used for common definitions and references that are needed to compile the `.c` file(s). A header file is included in a source file by means of the `#include` directive, like so:
```c
//include a header file from the standard library
#include <stdio.h>
//include one of your own header files from the same directory as your source file
#include "my_header.h"
```

#### `C` language basics  
This code snippet illustrates some basic ways to write `C` code:
```c
#include <stdio.h>

// this is a single line comment
/* this
is
a
multi-line
comment */

// to define a variable, indicate the type, then the variable name and assign it an
// initial value, and terminate with a ';':
int count = 0;

// all functions must be declared before they are used. in other words, if you want to
// use the function 'count_to_ten' in 'main', it must be declared above it:
int count_to_ten()
{
  // loop by starting from the value '1', continue while the value is less than or equal
  // to '10', increment the value by one every time.
  for (int i = 1; i <= 10; i++)
  {
    //print the value to the screen (also called 'stdout') by specifying the %d format
    //specifier and passing the value to the function 'printf'
    //print every value on its own line by including the \n (or newline) character
    printf("%d\n", i);
  }

  //return a value to indicate success
  return 0;
}

// functions can be declared first without providing an implementation for them. This allows you to define (i.e. provide an implementation for) the function after the place in which it is used (which helps in structuring your source file):
int count_to_zero(int start);

int main()
{
  // to use a value, reference the name and optionally assign a new value:
  count = 1;
  // to increment a numeric value, use one of the following:
  count = count + 1;
  count += 1;
  count++;
  // to decrement, use:
  count = count - 1;
  count -= 1;
  count--;

  // call the 'count_to_ten' function. the function will return a value, but we don't have to use it.
  count_to_ten();

  // can call this function as it has a declaration before 'main', even if the definition
  // is after 'main'
  count_to_zero(20);

  // must always return a value when a function has specified a return type ('int' in this case)
  // linux attaches special meanings to return values from 'main' (which is why 'main' cannot return 'void').
  // returning '0' from 'main' means that the program completed without errors.
  return 0;
}

// provide a definition for the 'count_to_zero' function
// it is common practice to declare functions at the top of a source file and provide
// function definitions after the main function.
int count_to_zero(int start)
{
  // always check if valid information was passed
  if (start < 0)
  {
    printf("can't count any lower than zero...");
    // return a value that indicates an error (this will not continue with the rest of
    // the function)
    return -1;
  }
  // loop from the supplied starting value, continue while the value is greater than or
  // equal to zero, decrement the value by one each time
  for (int i = start, i >= 0; i--)
  {
    printf("%d\n", i);
  }

  return 0;
}
```

#### Compiling and executing  
In order to compile the `.c` file, use the `gcc` program, like so:
```bash
# compile the file blink.c and output (-o) the executable, compiled file to blink
$ gcc -o blink blink.c
# run the blink program
$ ./blink
```

### WiringPi
WiringPi is a library that was written in `C` specifically for accessing GPIO on the Raspberry Pi. You can find more information at [Wiring Pi](http://wiringpi.com).

The following code snippet shows some basic ways to use the wiringPi library:
```c
#include <stdio.h>
#include <wiringPi.h>

// define a text replacement (i.e. before compiling, every occurrence of RED will be
// replaced by 17). This is also called a "pre-processor directive".
#define RED 17
#define BUTTON 21
#define PWM_LED 18

int main()
{
  int button_state = 0;

  // one of the setup functions MUST be called at the beginning of your program, or else
  // nothing will work
  // note that you cannot call more than one setup function per program

  // if you would like to use the wiringPi numbering scheme for GPIO, then do this first:
  wiringPiSetup();
  // if you would like to use the BCM numbering scheme for GPIO, then do this first:
  wiringPiSetupGpio();

  // must set the pin mode before using it. available options are:
  // OUTPUT, INPUT, PWM_OUTPUT (only on BCM pin 18), GPIO_CLOCK (only on BCM pin 4)
  pinMode(RED, OUTPUT);
  pinMode(BUTTON, INPUT);
  pinMode(PWM_LED, PWM_OUPUT);

  // "write" a value to the pin. writing '1' or 'HIGH' will set the value to VCC (3.3 v), whereas writing '0' or 'LOW' will set the value to GND (0 V).
  digitalWrite(RED, HIGH);

  // "read" the current value of a pin. a value of '1' will indicate that there is a voltage value (typically 3.3 V) on the pin, whereas a value of '0' will indicate that there is 0 V on the pin.
  button_state = digitalRead(BUTTON);

  // write a PWM (Pulse Width Modulation) value to a pin. The range is 0..1024 with zero being a duty cycle of 0% (i.e. full off) and 1024 being a duty cycle of 100% (i.e. full on)
  pwmWrite(PWM_LED, 1024);
}
```

### Compiling and running your program
In order to compile the program and build an executable, you have to reference the wiringPi library, like so:
```bash
# -Wall: enables all compiler warnings
# -l: links to a pre-compiled library
$ gcc -Wall -o blink blink.c -l wiringPi
# this will produce an executable file called "blink" in the current directory
# you must run this program with root privileges, so use "sudo"
$ sudo ./blink
```

### Things to watch out for
1. Don't forget that all statements in `C` **must** end with a `;`
2. All variables and functions **must** be declared before using them
3. Remember to call one of the setup functions before doing anything else
4. Take special note of which numbering scheme you are using (and maybe even state it specifically in the source file). Mixing up pin numbers between the BCM and wiringPi schemes can cause a lot of confusion
5. Always use descriptive variable names, as it will make it much easier to understand you program later on
6. Try to maintain a single point of control. For example, defining pin numbers as descriptive names in the beginning of the program allows you to easily change which pins are actually used, as you only need to change it in one place


## Programming in Python
### A crash course in Python
`Python` is a dynamically typed, interpreted, object-oriented language. It excels in high level programming, which basically means that much of the low level functionality has been wrapped in abstractions which take care of the setup (things like memory allocation etc.) and provide the programmer with an easy to use interface.

"Dynamically typed" means that variables are not assigned a fixed type at compile time, but rather that the type of a variable is determined during run-time. This also means that variables can change which type they are during run-time by reassignment. For example, the following is valid:
```python
redLed = 1
redLed = "RED"
```
**This does not mean that types are interchangeable**! Attempting to do something with a "string" variable that can only be done with an "integer" variable will result in a runtime error.

"Interpreted" means that there is no need to compile a program before running it. The statements in the program are read by an "interpreter" and then executed one after the other, from top to bottom. This is why `Python` has a utility called the `REPL` (Read, Evaluate, Print, Loop), which allows you to interactively enter statements, which are then immediately evaluated and have the result printed out. This allows you to interact with language in a short feedback loop and see exactly what each statement does.

"Object-oriented" means that code and memory is structured in objects, which are data structures that encapsulate data and behaviour (i.e. methods/functions).

#### Structure
`Python` is also a block structured language, but it does not use bracket pairs `{ }` to indicate a block. Instead it uses indentation (i.e. spaces) to indicate block membership. This makes it easier to read, but can result in some undesired behaviour and errors if you do not structure indentation correctly. Statements do not have to be terminated by a special character, but you can only have one statement per line.

A python source file does not need a main function, as any code in the file will be executed top to bottom when the file is called (invoked). It is usually recommended (for anything non-trivial) to have all code in functions or classes (object definitions) and have an entry point like the following:
```python
# write something regardless of how the file is accessed
print("I will always be there")

# define a function
def writeHello():
  print("Hello")

if __name__ == "__main__":
  writeHello()
```
When we run this source file directly, it will execute in the `__main__` context and will call the function `writeHello`. If we run this source file from another source file, it will not execute in the `__main__` context and this will not happen.
```bash
$ python3 say_hello.py
I will always be there
Hello
$
```

#### Python language basics
Here are some basic ways to write `Python` code:
```python
# this is a comment

# import everything from another module or file
import my_module
# import only some things from another module
from my_module import func1, func2, my_class

# write something to the terminal (stdout)
print("Hello there")

# declare a variable
greeting = "Hello"
numberOfGreetings = 10

# define a function
def greet(greeting, name, howManyTimes):
    # everything that should be part of this function must be indented
    for i in range(howManyTimes):
        # everything part of the for loop should again be indented
        print(f'{greeting} {name}')

    # this is not part of the for loop, as we are back to the previous level of indentation

# this is not part of the function, as we are back to no indentation

# count forwards in increments of 2
def countToTen():
    for i in range(0, 10, 2): #(start, end, step size)
        print(i)
    
    return 0

# count backwards to 0
def countToZero(start):
    for i in range(start, 0, -1):
        print(i)

# only execute if the file is invoked directly
if __name__ == "__main__":
    # call the function
    greet()
```

### gpiozero
`gpiozero` is a `Python` library that allows access to the Raspberry Pi's GPIO via a high level interface. You can find more information [here][gpiozero]

Here are some basic ways to use the `gpiozero` library:
```python
# the 'LED' class allows output to pins
from gpiozero import LED
# the 'Button' class allows input from the pins
from gpiozero import Button
# the 'sleep' function allows the process to be delayed (this is not part of gpiozero)
from time import sleep
# the 'pause' function will keep the process running, while still reacting to events
# this will only work in linux
from signal import pause

# create an object that will allow us to output values
red_led = LED(17) # using BCM pin 17
green_led = LED(18)
yellow_led = LED(20)

# define a function to blink an LED continuously
def blink_led(led_to_blink):
    while True:
        led_to_blink.on()   # turn it on
        sleep(1)            # wait for 1 second
        led_to_blink.off()  # turn it off
        sleep(1)            # wait for 1 second

# create a button object that will allow us to read values
button = Button(3)

# register event handlers (functions to be called) to button events
button.when_pressed = red_led.on # don't actually call the function, just provide it's name
button.when_released = red_led.off

green_led.blink()

if __name__ == "__main__":
    blink_led(yellow_led)
```

### Running your program
There is no need to compile your python program first. You can run it by simply passing it as an option to the `Python` interpreter, like so:
```bash
$ python3 blink.py
```


### Things to watch out for
1. The Raspbian distribution comes with python v2.7 and python v3.x installed by default. There are significant differences between v2.x and v3.x, so the programs are not compatible. Make sure to write all of your code in v3.x syntax.
2. Make sure to run all of your programs using the python v3.x interpreter. This is achieved by running the `python3` program from the shell. If you run the `python` program, it will attempt to run the python v2.x interpreter and your program will most likely not run
3. Take special note of the indentation in any code block. This includes functions, control statements (e.g. `if`, `for`, `while` etc.) and classes.

[interactive-pinout]: https://pinout.xyz/
[gpiozero]: https://gpiozero.readthedocs.io/en/stable/index.html

[pi-labelled]: ../static/images/pi-labelled.png "labelled raspberry pi layout"
[pi-pinout]: ../static/images/raspberry-pi-pinout.png "raspberry pi pinout"
[pinout-command]: ../static/images/gpiozero-pinout.png "pinout command screen"