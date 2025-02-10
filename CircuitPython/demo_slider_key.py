# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT
"""
Demo of NeoSlider and NeoKey combined

NOTE: These devices both have address 0x30 by default.
      You need to cut jumper A3 on the back of the NeoSlider to change
      its address to 0x38
"""
print("demo_slider_key")

import board
from rainbowio import colorwheel
from adafruit_seesaw.seesaw import Seesaw
from adafruit_seesaw.analoginput import AnalogInput
from adafruit_seesaw import neopixel
from adafruit_neokey.neokey1x4 import NeoKey1x4


# NeoSlider Setup
i2c = board.I2C()  # uses board.SCL and board.SDA
#i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
#neoslider = Seesaw(i2c, 0x30) # Default address
neoslider_address = 0x38 # Address with A3 cut, to avoid conflicts with Neokey at 0x30
print("Connecting to Neoslider at %x" % neoslider_address)
neoslider = Seesaw(i2c, neoslider_address)

potentiometer = AnalogInput(neoslider, 18)
pixels = neopixel.NeoPixel(neoslider, 14, 4, pixel_order=neopixel.GRB)

## Set up Neokey
print("Setting up NeoKey")
# Create a NeoKey object using existing i2c bus
neokey = NeoKey1x4(i2c, addr=0x30) # Default address

# Set false to skip printing debug messages - faster performance
serial_debug = False


def potentiometer_to_color(value):
    """Scale the potentiometer values (0-1023) to the colorwheel values (0-255)."""
    return value / 1023 * 255


while True:
    ### NeoSlider handling
    if serial_debug:
        print(potentiometer.value)
    # Fill the pixels a color based on the position of the potentiometer.
    pixels.fill(colorwheel(potentiometer_to_color(potentiometer.value)))

    ### NeoKey handling
    # Check each button, if pressed, light up the matching neopixel!
    if neokey[0]:
        if serial_debug:
            print("Button A")
        neokey.pixels[0] = 0xFF0000
    else:
        neokey.pixels[0] = 0x0

    if neokey[1]:
        if serial_debug:
            print("Button B")
        neokey.pixels[1] = 0xFFFF00
    else:
        neokey.pixels[1] = 0x0

    if neokey[2]:
        if serial_debug:
            print("Button C")
        neokey.pixels[2] = 0x00FF00
    else:
        neokey.pixels[2] = 0x0

    if neokey[3]:
        if serial_debug:
            print("Button D")
        neokey.pixels[3] = 0x00FFFF
    else:
        neokey.pixels[3] = 0x0
