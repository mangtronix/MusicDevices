# SPDX-FileCopyrightText: 2019 Carter Nelson for Adafruit Industries
#
# SPDX-License-Identifier: MIT
#
# Original code at https://learn.adafruit.com/circuitpython-display-support-using-displayio/sprite-sheet
# - You need to install the adafruit_imageload library from the project bundle
# - You need to copy over the cp_sprite_sheet.bmp file from that page to CIRCUITPY/
#
# Modifications by Michael Anl g for NYUADIM Music Devices
# - sprite_scale for controlling size of sprite
# - center sprite on display

import adafruit_simplemath

input_value = 0
output_value = int(adafruit_simplemath.map_range(input_value, 0, 1023, 127, 0))
print(output_value)

import board
import digitalio
# Flip display so buttons are on right
display = board.DISPLAY
display.rotation = 180

print("spritekeys")

# Whether to print serial debug messages (slows down loop)
serial_debug = True
if serial_debug:
    print("Serial debug ON")

import time
time.sleep(0.5) # Might help I2C devices to power on

# Display / graphics
import displayio
import adafruit_imageload

# NeoKey / NeoSlider
from rainbowio import colorwheel
from adafruit_seesaw.seesaw import Seesaw
from adafruit_seesaw.analoginput import AnalogInput
from adafruit_seesaw import neopixel
from adafruit_neokey.neokey1x4 import NeoKey1x4

# MIDI
import adafruit_midi
import usb_midi
from adafruit_midi.control_change import ControlChange
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn



# Start i2c connection
i2c_success = False
i2c_chances = 5
i2c_power = digitalio.DigitalInOut(board.TFT_I2C_POWER)
i2c_power.direction = digitalio.Direction.OUTPUT

print("Initializing I2C")
while (not i2c_success) and i2c_chances > 0:
    try:
        i2c = board.I2C()
        i2c_success = True
    except Exception as e:
        print(e)
        print("  I2C init failed, %d chances left" % i2c_chances)
        print("  Resetting I2C power")
        i2c_power.value = False
        time.sleep(0.1)
        i2c_power.value = True
        time.sleep(0.1)
        i2c_chances -= 1

if not i2c_success:
    raise RuntimeError("Failed to initialize i2c")

#i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller


## NeoSlider Setup
#neoslider = Seesaw(i2c, 0x30) # Default address
neoslider_address = 0x38 # Address with A3 cut, to avoid conflicts with Neokey at 0x30
print("Connecting to Neoslider at %x" % neoslider_address)

# Try connecting with NeoSlider - for some reason the initial connection often
# doesn't work, so we retry several times
neoslider_success = False
neoslider_chances = 10
while (not neoslider_success) and neoslider_chances > 0:
    try:
        neoslider = Seesaw(i2c, neoslider_address)
        neoslider_success = True
    except Exception as e:
        print(e)
        print("  Retrying NeoSlider connect, %d chances left" % neoslider_chances)
        time.sleep(0.2)
        neoslider_chances -= 1

if not neoslider_success:
    raise RuntimeError("  Could not connect to NeoSlider")

slider = AnalogInput(neoslider, 18)
old_cc_value = slider.value # So we can act only on changes
pixels = neopixel.NeoPixel(neoslider, 14, 4, pixel_order=neopixel.GRB)

## Set up Neokey
print("Setting up NeoKey")
# Create a NeoKey object using existing i2c bus
neokey = NeoKey1x4(i2c, addr=0x30) # Default address
neokey_was_pressed = [False, False, False, False] # Keep track of previous state so we can act at transitions
neokey_on_colors = [0xCCFF00, # Chartreuse
    0xFFFF00,
    0x00FF00,
    0x00FFFF] # Color when pressed

neokey_off_colors = [0xFF0000, 0x00FF00, 0, 0]
# Start with off colors
for i in range(0,4):
    neokey.pixels[i] = neokey_off_colors[i]

def slider_to_color(value):
    """Scale the potentiometer values (0-1023) to the colorwheel values (0-255)."""
    return value / 1023 * 255

"""Return 0-127 value for CC message from slider value"""
def slider_to_cc_value(value):
    # Map 0-1023 to 127-0
    return int(adafruit_simplemath.map_range(value, 0, 1023, 127, 0))
#    return 127 - int((value / 1023) * 127)

display = board.DISPLAY
display.rotation = 180 # Flip display so buttons are on right

# Dimensions in .bmp file
tile_width = 32
tile_height = 32

# Dimensions on screen
sprite_scale = 4
sprite_width = tile_width * sprite_scale
sprite_height = tile_height * sprite_scale

# Load the sprite sheet (bitmap)
spritesheet_filename = "spritesheet.gif"
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


# USB MIDI setup
print("USB MIDI ports:")
print(usb_midi.ports)
if len(usb_midi.ports) == 0:
    print("No MIDI ports found, check that MIDI is enabled in boot.py")
    print("https://learn.adafruit.com/customizing-usb-devices-in-circuitpython/circuitpy-midi-serial#midi-3096586")
    raise(Exception("No MIDI port found"))

midi_in_channel = 2
midi_out_channel = 1
midi = adafruit_midi.MIDI(
    # Hardware MIDI port
    # midi_in=uart,
    # midi_out=uart,

    # USB MIDI
    midi_in=usb_midi.ports[0],
    midi_out=usb_midi.ports[1],

    in_channel=(midi_in_channel - 1),
    out_channel=(midi_out_channel - 1),
    debug=False,
)
print("MIDI output channel:", midi.out_channel + 1)

# Which notes to play
# See examples at
# https://learn.adafruit.com/midi-melody-maker/circuitpython-code-walkthrough#create-the-midi-note-arrays-3073059
c_major_scale = [60, 62, 64, 65, 67, 69, 71, 72]
c_major_pentatonic_scale = [60, 62, 64, 67, 69] # C, D, E, G, A
e_minor_scale = [64, 66, 67, 69, 71, 72, 74]
e_minor_pentatonic_scale = [64, 67, 69, 71, 74] # E, G, A, B, D

# Notes of b flat minor from Perplexity.ai
bb_minor_midi_array = [58, 60, 61, 63, 65, 66, 68]

bb_minor_midi_array_octave_up = [
    70,  # Bb
    72,  # C
    73,  # Db
    75,  # Eb
    77,  # F
    78,  # Gb
    80   # Ab
]


notes = bb_minor_midi_array_octave_up
#notes = c_major_scale
velocity = 100

"""Turn all of our notes off"""
def notesOff():
    for note in notes:
        midi.send(NoteOff(note, 0))

# Which Control Change the slider will send
cc_number = 1 # Modulation CC
    

# Give MIDI a chance to reconnect
time.sleep(0.5)
# Turn all the notes off in case we left any hanging (e.g. unplugged or reset board)
notesOff()

while True:

    ### NeoSlider handling
    new_cc_value = slider_to_cc_value(slider.value)
    if new_cc_value != old_cc_value:
        if serial_debug:
            print("Slider %d" % slider.value)

        # Send the Control Change (CC) message
        midi.send(ControlChange(cc_number, new_cc_value))
        if serial_debug:
            print("CC %d - %d" % (cc_number, new_cc_value))

        # Fill the pixels a color based on the position of the potentiometer.
        pixels.fill(colorwheel(slider_to_color(slider.value)))

        # Store old value - we'll run again only when the slider has changed
        old_cc_value = new_cc_value

    ### NeoKey handling
    # Check each button, if pressed, light up the matching neopixel!
    for i in range(0, 4): # 4 buttons
        if neokey[i] and not neokey_was_pressed[i]:
            # Just pressed
            if serial_debug:
                print("Button %d pressed" % i)

            # Send note on
            midi.send(NoteOn(notes[i], velocity))
            if serial_debug:
                print("NoteOn %d" % notes[i])

            # Set on color
            neokey.pixels[i] = neokey_on_colors[i]

            # Update screen
            source_index = i + 1

            neokey_was_pressed[i] = True

        elif neokey_was_pressed[i] and not neokey[i]:
            # Just released
            if serial_debug:
                print ("Button %d released" % i)
            
            # Set off color
            neokey.pixels[i] = neokey_off_colors[i]

            # Send note off
            midi.send(NoteOff(notes[i], 0))
            if serial_debug:
                print("NoteOff %d" % notes[i])

            # Update sprite
            source_index = 0

            neokey_was_pressed[i] = False

    # Update screen pixels if necessary
    if source_index != old_source_index:        
        sprite[0] = source_index
        old_source_index = source_index
