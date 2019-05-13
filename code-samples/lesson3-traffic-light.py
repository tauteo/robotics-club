from gpiozero import TrafficLights
from time import sleep
from signal import pause

lights = TrafficLights(2, 3, 4)

def traffic_light_sequence():
  while True:
    yield(0, 0, 1)
    sleep(10)
    yield(0, 1, 0)
    sleep(1)
    yield(1, 0, 0)
    sleep(10)
    yield(1, 1, 0)
    sleep(1)

lights.source = traffic_light_sequence()

pause()