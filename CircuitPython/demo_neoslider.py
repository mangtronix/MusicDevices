# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT

# Adapted by Michael Ang
# 2024-04-09
#
# Read from NeoSlider
"""
NeoSlider NeoPixel Rainbow Demo
"""

import board
# Flip display so buttons are on right
display = board.DISPLAY
display.rotation = 180

print("demo_neoslider")

# Give I2C devices a chance to turn on
import time
time.sleep(0.5)

import board
from rainbowio import colorwheel
from adafruit_seesaw.seesaw import Seesaw
from adafruit_seesaw.analoginput import AnalogInput
from adafruit_seesaw import neopixel

# NeoSlider Setup
i2c = board.I2C()  # uses board.SCL and board.SDA

# The default address for the NeoSlider is 0x30
# The default address for the NeoKey 1x4 is ALSO 0x30
# If two devices on the bus have the same address it will cause
# problems. For Music Devices we cut jumper A3 on the back of the
# NeoSlider board to set it to address 0x38.
# neoslider_address = 0x30 # Default address
neoslider_address = 0x38 # Address with A3 jumper cut

# Create a SeeSaw object that connects to the NeoSlider board over the
# I2C / QT bus using the NeoSlider address
neoslider = Seesaw(i2c, neoslider_address)

# Create an analog input for reading the position of the fader
fader = AnalogInput(neoslider, 18)

# Create an object that we can use to controls the LEDs on
# the NeoSlider
pixels = neopixel.NeoPixel(neoslider, 14, 4, pixel_order=neopixel.GRB)

# Convert a fader linear position to a color to display on the NeoPixels
# Returns the color
def fader_to_color(value):
    """Scale the fader values (0-1023) to the colorwheel values (0-255)."""
    return value / 1023 * 255

# Keep track of the old position of the fader. We'll only print the
# fader position when it changes
old_value = None

while True:
    # Get the current fader position
    current_value = int(fader.value)

    # If the value has changed, print the new value and change the slider
    # color
    if (current_value != old_value):
        print(fader.value)
        # Fill the pixels a color based on the position of the slider.
        pixels.fill(colorwheel(fader_to_color(fader.value)))
        old_value = current_value
