import os
import threading
import time
from rpi_ws281x import *
from light_strip_fncns import *
from http.server import HTTPServer, BaseHTTPRequestHandler

#HOST = "192.168.29.160"
HOST = "0.0.0.0"
PORT = 1111
# LED strip configuration:
LED_COUNT      = 20     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating a signal (try 10)
LED_BRIGHTNESS = 65      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_AMBER      = Color(252,69,6)
LED_RED        = Color(255,0,0)
LED_CLEAR      = Color(0,0,0)

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()

running_effect = None
stop_event = threading.Event()

def effect_runner(effect_func, *args):
    while not stop_event.is_set():
        print("looping..")
        effect_func(*args)

def run_right():
    colorWipe1(strip, LED_AMBER)
    colorWipe1(strip, Color(0,0,0))

def run_left():
    colorWipe2(strip, LED_AMBER)
    colorWipe2(strip, LED_CLEAR)

def run_brake():
    blink(strip, LED_RED)
    blink(strip, LED_CLEAR)

class LightHTTP(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        global running_effect, stop_event

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("utf-8")
        print(f"received POST data : {post_data}")

        self.send_response(200)
        self.end_headers()

        stop_event.set()
        time.sleep(0.1)
        stop_event.clear()

        if post_data=='1':
            print('turn right')
            threading.Thread(target=effect_runner, args=(run_right,), daemon=True).start()
        elif post_data=='2':
            print('left turn')
            threading.Thread(target=effect_runner, args=(run_left,), daemon=True).start()

        elif post_data=='0':
            print('braking')
            threading.Thread(target=effect_runner, args=(run_brake,), daemon=True).start()
        else:
            print("Unassigned data trigger")

    def do_DELETE(self):
        global stop_event
        stop_event.set()
        blink(strip, Color(0,0,0))
        self.send_response(200)
        self.end_headers()


server = HTTPServer((HOST, PORT), LightHTTP)

try:
   print("Light speed....")
   server.serve_forever()
except KeyboardInterrupt:
   server.server_close()
finally:
   print("....end")
