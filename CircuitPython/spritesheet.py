# SPDX-FileCopyrightText: 2019 Carter Nelson for Adafruit Industries
#
# SPDX-License-Identifier: MIT
#
# Original code at https://learn.adafruit.com/circuitpython-display-support-using-displayio/sprite-sheet
#
# Modifications by Michael Ang for NYUADIM Music Devices
# - sprite_scale for controlling size of sprite
# - center sprite on display

print("spritesheet")

import time
import board
import displayio
import adafruit_imageload

display = board.DISPLAY

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

# Loop through each sprite in the sprite sheet
source_index = 0
while True:
    sprite[0] = source_index % 6
    source_index += 1
    time.sleep(2)
