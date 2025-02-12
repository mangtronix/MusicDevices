# SPDX-FileCopyrightText: 2019 Carter Nelson for Adafruit Industries
#
# SPDX-License-Identifier: MIT
#
# Original code at https://learn.adafruit.com/circuitpython-display-support-using-displayio/sprite-sheet
#
# Modifications by Michael Ang for NYUADIM Music Devices
# - sprite_scale for controlling size of sprite
# - center sprite on display

print("spritekeys")

import time
import board
import displayio
import adafruit_imageload

from rainbowio import colorwheel
from adafruit_seesaw.seesaw import Seesaw
from adafruit_seesaw.analoginput import AnalogInput
from adafruit_seesaw import neopixel
from adafruit_neokey.neokey1x4 import NeoKey1x4

# Whether to print serial debug messages (slows down loop)
serial_debug = False

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


def potentiometer_to_color(value):
    """Scale the potentiometer values (0-1023) to the colorwheel values (0-255)."""
    return value / 1023 * 255

display = board.DISPLAY
display.rotation = 180 # Flip display so buttons are on right

# Dimensions in .bmp file
tile_width = 16
tile_height = 16

# Dimensions on screen
sprite_scale = 6
sprite_width = tile_width * sprite_scale
sprite_height = tile_height * sprite_scale

# Load the sprite sheet (bitmap)
spritesheet_filename = "cp_sprite_sheet.bmp"
try:
    sprite_sheet, palette = adafruit_imageload.load(spritesheet_filename,
                                                    bitmap=displayio.Bitmap,
                                                    palette=displayio.Palette)
# Catch any exception (problem)                                                    
except Exception as e:
    # Give the user a hint
    print("Missing %s - copy it to your CIRCUITPY drive" % spritesheet_filename)

    # Raise the exception so it will print the full error message
    raise e

# Create a sprite (tilegrid)
sprite = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
                            width = 1,
                            height = 1,
                            tile_width = tile_width,
                            tile_height = tile_height)

# Create a Group to hold the sprite
group = displayio.Group(scale=sprite_scale)

# Add the sprite to the Group
group.append(sprite)

# Add the Group to the Display
display.root_group = group

# Set sprite location
# Need to put inside int() to ensure we get e.g. 40 instead of 40.0
group.x = int(board.DISPLAY.width / 2 - sprite_width / 2)
group.y = int(board.DISPLAY.height / 2 - sprite_height / 2)

# Start on first sprite
old_source_index = 0
source_index = old_source_index
sprite[0] = source_index

while True:

    # Set sprite to "off" state - this will get overwritten if a key is being pressed
    source_index = 0

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
        source_index = 1
    else:
        neokey.pixels[0] = 0x0

    if neokey[1]:
        if serial_debug:
            print("Button B")
        neokey.pixels[1] = 0xFFFF00
        source_index = 2
    else:
        neokey.pixels[1] = 0x0

    if neokey[2]:
        if serial_debug:
            print("Button C")
        neokey.pixels[2] = 0x00FF00
        source_index = 3
    else:
        neokey.pixels[2] = 0x0

    if neokey[3]:
        if serial_debug:
            print("Button D")
        neokey.pixels[3] = 0x00FFFF
        source_index = 4
    else:
        neokey.pixels[3] = 0x0

    # Update screen if necessary
    if source_index != old_source_index:        
        sprite[0] = source_index
        old_source_index = source_index
