"""Music Devices library for NYUAD IM Music Devices class."""

import board

def init():
    print("musicdevices init v1.0")
    init_display()

def init_display():
    # Flip display so buttons are on right
    display = board.DISPLAY
    display.rotation = 180
