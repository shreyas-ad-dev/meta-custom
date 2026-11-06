#!/usr/bin/env python3
import os
import mmap
import struct
import subprocess
import select
import fcntl

FB_PATH = "/dev/fb1"
TOUCH_PATH = "/dev/input/touchscreen0"

WIDTH, HEIGHT = 240, 320

# Open framebuffer
fb_file = open(FB_PATH, "r+b")
fb = mmap.mmap(fb_file.fileno(), WIDTH * HEIGHT * 2) # 16-bit RGB565

# Simple 5x8 font simulation or block drawing helper for text
# For a lightweight standalone script without Pygame, we can draw a status bar and interactive buttons.
def draw_rect(x, y, w, h, color):
    for py in range(y, min(y + h, HEIGHT)):
        start = (py * WIDTH + x) * 2
        row_data = struct.pack('H' * w, *([color] * w))
        if start + (w * 2) <= len(fb):
            fb[start:start + (w * 2)] = row_data

def clear_screen(color=0x0000):
    draw_rect(0, 0, WIDTH, HEIGHT, color)

# Draw UI Layout: Top output area, middle input line, bottom virtual keypad
def draw_ui(current_text, last_output):
    # Clear screen to dark gray
    clear_screen(0x1082)
    
    # Terminal Output Box (Top)
    draw_rect(5, 5, 230, 85, 0x0000) # Black box
    
    # Input Box (Middle)
    draw_rect(5, 100, 230, 40, 0xFFFF) # White box for active command
    
    # Virtual Keypad Buttons (Bottom)
    # Let's draw a grid of 4 rows x 3 cols for simplicity (Numbers & Actions)
    buttons = [
        ("1", 5, 150), ("2", 85, 150), ("3", 165, 150),
        ("4", 5, 190), ("5", 85, 190), ("6", 165, 190),
        ("7", 5, 230), ("8", 85, 230), ("9", 165, 230),
        ("CLR", 5, 270), ("0", 85, 270), ("EXE", 165, 270)
    ]
    
    for label, bx, by in buttons:
        draw_rect(bx, by, 70, 32, 0x7BEF) # Gray buttons

# Initialize UI state
current_cmd = ""
last_out = "Ready."
draw_ui(current_cmd, last_out)

print("Terminal UI framework initialized. Listening for touch input...")

# Open touch input event node
try:
    touch_file = open(TOUCH_PATH, "rb")
    # Set non-blocking or use select for touch reading
    fd = touch_file.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
except Exception as e:
    print(f"Could not open touch device: {e}")
    touch_file = None

# Event struct format for Linux input_event (time_sec, time_usec, type, code, value)
EVENT_FORMAT = 'llHhi'
EVENT_SIZE = struct.calcsize(EVENT_FORMAT)

touch_x, touch_y = 0, 0

while True:
    if touch_file:
        r, w, x = select.select([touch_file], [], [], 0.1)
        if r:
            data = touch_file.read(EVENT_SIZE)
            while data and len(data) == EVENT_SIZE:
                tv_sec, tv_usec, ev_type, code, value = struct.unpack(EVENT_FORMAT, data)
                # ABS_X = 0, ABS_Y = 1, SYN_REPORT = 0
                if ev_type == 3: # EV_ABS
                    if code == 0: touch_x = value
                    elif code == 1: touch_y = value
                elif ev_type == 1 and code == 330 and value == 0: # BTN_TOUCH release
                    print(f"Touch released at X={touch_x}, Y={touch_y}")
                    # Map touch coordinates (adjust ranges based on your XPT2046 calibration)
                    # For a 320x240 display, let's map button hitboxes:
                    if 120 <= touch_y <= 146:
                        if 10 <= touch_x <= 100: current_cmd += "1"
                        elif 115 <= touch_x <= 205: current_cmd += "2"
                        elif 220 <= touch_x <= 310: current_cmd += "3"
                    elif 210 <= touch_y <= 236:
                        if 10 <= touch_x <= 100: current_cmd = ""
                        elif 115 <= touch_x <= 205: current_cmd += "0"
                        elif 220 <= touch_x <= 310:
                            # Execute command via subprocess
                            print(f"Executing: {current_cmd}")
                            try:
                                res = subprocess.run(current_cmd, shell=True, capture_output=True, text=True, timeout=2)
                                last_out = res.stdout if res.stdout else res.stderr
                            except Exception as ex:
                                last_out = str(ex)
                            current_cmd = ""
                    draw_ui(current_cmd, last_out)
                data = touch_file.read(EVENT_SIZE)
