#!/usr/bin/env python3
import os
import mmap
import struct
import subprocess
import select
import fcntl

FB_PATH = "/dev/fb1"
TOUCH_PATH = "/dev/input/event0"

WIDTH, HEIGHT = 240, 320
ROW_STRIDE = 480 # 240 pixels * 2 bytes per pixel

# Open framebuffer
fb_file = open(FB_PATH, "r+b")
fb = mmap.mmap(fb_file.fileno(), HEIGHT * ROW_STRIDE)

# Minimal 5x8 Font Dictionary for basic alphanumeric characters & symbols
FONT_5X8 = {
    ' ': [0x00,0x00,0x00,0x00,0x00], '0': [0x3E,0x51,0x49,0x45,0x3E],
    '1': [0x00,0x42,0x7F,0x40,0x00], '2': [0x42,0x61,0x51,0x49,0x46],
    '3': [0x21,0x41,0x45,0x4B,0x31], '4': [0x18,0x14,0x12,0x7F,0x10],
    '5': [0x27,0x45,0x45,0x45,0x39], '6': [0x3C,0x4a,0x49,0x49,0x30],
    '7': [0x01,0x71,0x09,0x05,0x03], '8': [0x36,0x49,0x49,0x49,0x36],
    '9': [0x06,0x49,0x49,0x29,0x1E], 'A': [0x7E,0x11,0x11,0x11,0x7E],
    'B': [0x7F,0x49,0x49,0x49,0x36], 'C': [0x3E,0x41,0x41,0x41,0x22],
    'D': [0x7F,0x41,0x41,0x22,0x1C], 'E': [0x7F,0x49,0x49,0x49,0x41],
    'F': [0x7F,0x09,0x09,0x09,0x01], 'L': [0x7F,0x40,0x40,0x40,0x40],
    'R': [0x7F,0x09,0x19,0x29,0x46], 'X': [0x41,0x22,0x1C,0x22,0x41],
    '.': [0x00,0x60,0x60,0x00,0x00], '=': [0x14,0x14,0x14,0x14,0x14],
}

def draw_rect(x, y, w, h, color):
    for py in range(y, min(y + h, HEIGHT)):
        start = (py * ROW_STRIDE) + (x * 2)
        row_data = struct.pack('H' * w, *([color] * w))
        if start + (w * 2) <= len(fb):
            fb[start:start + (w * 2)] = row_data

def draw_char(x, y, char, color, bg_color):
    char_data = FONT_5X8.get(char.upper(), FONT_5X8[' '])
    for col_idx, col_val in enumerate(char_data):
        for row_idx in range(8):
            if (col_val >> row_idx) & 1:
                px, py = x + col_idx, y + row_idx
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    offset = (py * ROW_STRIDE) + (px * 2)
                    fb[offset:offset+2] = struct.pack('H', color)

def draw_string(x, y, text, color, bg_color):
    for i, char in enumerate(text):
        draw_char(x + (i * 6), y, char, color, bg_color)

def clear_screen(color=0x0000):
    for py in range(HEIGHT):
        start = py * ROW_STRIDE
        row_data = struct.pack('H' * WIDTH, *([color] * WIDTH))
        fb[start:start + ROW_STRIDE] = row_data

def draw_ui(current_text, last_output):
    clear_screen(0x1082) # Dark gray background

    # Terminal Output Box (Top)
    draw_rect(5, 5, 230, 85, 0x0000)
    draw_string(10, 10, "OUT:", 0x07E0, 0x0000)
    draw_string(10, 25, last_output[:36], 0xFFFF, 0x0000)

    # Input Box (Middle)
    draw_rect(5, 100, 230, 40, 0xFFFF)
    draw_string(10, 112, "> " + current_text[-28:], 0x0000, 0xFFFF)

    # Virtual Keypad Buttons (Bottom 4 rows x 3 cols)
    buttons = [
        ("1", 5, 150), ("2", 85, 150), ("3", 165, 150),
        ("4", 5, 190), ("5", 85, 190), ("6", 165, 190),
        ("7", 5, 230), ("8", 85, 230), ("9", 165, 230),
        ("CLR", 5, 270), ("0", 85, 270), ("EXE", 165, 270)
    ]

    for label, bx, by in buttons:
        draw_rect(bx, by, 70, 32, 0x7BEF) # Gray button box
        # Center text label inside 70x32 button box
        text_x = bx + (70 - (len(label) * 6)) // 2
        text_y = by + 12
        draw_string(text_x, text_y, label, 0x0000, 0x7BEF)

# Initialize UI state
current_cmd = ""
last_out = "Ready."
draw_ui(current_cmd, last_out)
print("Terminal UI framework initialized. Listening for touch input...")

# Open touch input event node (using event0 directly)
try:
    touch_file = open(TOUCH_PATH, "rb")
    fd = touch_file.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
except Exception as e:
    print(f"Could not open touch device: {e}")
    touch_file = None

# 64-bit kernel Linux input event format
EVENT_FORMAT = 'QQhhi'
EVENT_SIZE = struct.calcsize(EVENT_FORMAT)

raw_x, raw_y = 0, 0

# Calibration ranges mapped from raw XPT2046 ADC values to 240x320 screen pixels
RAW_X_MIN, RAW_X_MAX = 300, 3800
RAW_Y_MIN, RAW_Y_MAX = 300, 3800

while True:
    if touch_file:
        r, w, x = select.select([touch_file], [], [], 0.1)
        if r:
            data = touch_file.read(EVENT_SIZE)
            while data and len(data) == EVENT_SIZE:
                tv_sec, tv_usec, ev_type, code, value = struct.unpack(EVENT_FORMAT, data)
                if ev_type == 3: # EV_ABS
                    if code == 0: raw_x = value
                    elif code == 1: raw_y = value
                elif ev_type == 1 and code == 330 and value == 0: # BTN_TOUCH release
                    # Map raw ADC values to portrait screen pixels (240x320)
                    screen_x = int((raw_x - RAW_X_MIN) / (RAW_X_MAX - RAW_X_MIN) * WIDTH)
                    screen_y = int((raw_y - RAW_Y_MIN) / (RAW_Y_MAX - RAW_Y_MIN) * HEIGHT)
                    
                    # Hitbox mapping for 4 rows of buttons
                    if 150 <= screen_y <= 182: # Row 1: [1], [2], [3]
                        if 5 <= screen_x <= 75: current_cmd += "1"
                        elif 85 <= screen_x <= 155: current_cmd += "2"
                        elif 165 <= screen_x <= 235: current_cmd += "3"
                    elif 190 <= screen_y <= 222: # Row 2: [4], [5], [6]
                        if 5 <= screen_x <= 75: current_cmd += "4"
                        elif 85 <= screen_x <= 155: current_cmd += "5"
                        elif 165 <= screen_x <= 235: current_cmd += "6"
                    elif 230 <= screen_y <= 262: # Row 3: [7], [8], [9]
                        if 5 <= screen_x <= 75: current_cmd += "7"
                        elif 85 <= screen_x <= 155: current_cmd += "8"
                        elif 165 <= screen_x <= 235: current_cmd += "9"
                    elif 270 <= screen_y <= 302: # Row 4: [CLR], [0], [EXE]
                        if 5 <= screen_x <= 75: current_cmd = "" # CLR
                        elif 85 <= screen_x <= 155: current_cmd += "0" # 0
                        elif 165 <= screen_x <= 235: # EXE
                            print(f"Executing: {current_cmd}")
                            try:
                                res = subprocess.run(current_cmd, shell=True, capture_output=True, text=True, timeout=2)
                                last_out = res.stdout if res.stdout else res.stderr
                                if not last_out.strip(): last_out = "OK."
                            except Exception as ex:
                                last_out = str(ex)
                            current_cmd = ""
                            
                    draw_ui(current_cmd, last_out)
                data = touch_file.read(EVENT_SIZE)
