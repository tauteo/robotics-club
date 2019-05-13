from gpiozero import LEDBoard
from time import sleep
from signal import pause

leds = LEDBoard(5, 6, 13, 19, 26)

for led in leds:
  led.on()

sleep(1)

for led in leds:
  led.off()

