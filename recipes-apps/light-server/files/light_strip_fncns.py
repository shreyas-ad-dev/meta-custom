import time
from rpi_ws281x import *

# Define functions which animate LEDs in various ways.
def colorWipe1(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)


def colorWipe2(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(strip.numPixels()-i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def blink(strip, color):
    for i in range(strip.numPixels()):
        if not (strip.getPixelColor(i) == '0'):
           strip.setPixelColor(i, color)
           strip.show()
        else:
           print(f"pixel {i} is {strip.getPixelColor(i)}")
#        time.sleep(0.001)
