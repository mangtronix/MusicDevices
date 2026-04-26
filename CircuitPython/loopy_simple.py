# SPDX-FileCopyrightText: 2026 Michael Ang for NYUADIM Music Devices
# SPDX-License-Identifier: MIT
#
# loopy_simple -- 4-clip Loopy Pro controller for the Adafruit ESP32-S3
# Reverse TFT Feather + NeoKey 1x4 + NeoSlider.
#
# Layout in Loopy Pro:
#   - One row of 4 clips, left to right:
#       button 0 = drums   (red)
#       button 1 = voice   (yellow)
#       button 2 = guitar  (green)
#       button 3 = keys    (cyan)
#
# Trigger protocol (controller -> Loopy Pro):
#   - Each clip is mapped to a unique MIDI Control Change number.
#   - Pressing a button sends that CC with value 127 (trigger).
#   - Releasing sends value 0. Loopy Pro can map either edge to a clip action
#     (toggle, start, stop, etc.) in its MIDI Learn dialog.
#
# Feedback (Loopy Pro -> controller):
#   - When a clip starts, Loopy Pro sends the same CC back with value 127.
#   - When a clip stops, Loopy Pro sends the same CC back with value 0.
#   - The NeoKey for that clip lights bright in its column color when the clip
#     is playing, dim otherwise.
#
# Slider:
#   - Sends a single CC (default CC 7 = Volume). Map it to whatever you like
#     in Loopy Pro (master volume, send level, an effect, etc.).
#
# CCs (default - using CCs 20..23, unassigned in the MIDI spec):
#   button 0 -> CC 20 (drums)
#   button 1 -> CC 21 (voice)
#   button 2 -> CC 22 (guitar)
#   button 3 -> CC 23 (keys)
#   slider   -> CC  7 (volume)

import adafruit_simplemath
import board
import digitalio
import time

display = board.DISPLAY
display.rotation = 180

print("loopy_simple")

serial_debug = True
if serial_debug:
    print("Serial debug ON - turn off for faster response")

time.sleep(0.5)

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


### I2C SETUP -----------------------------------------------------------------
i2c_power = digitalio.DigitalInOut(board.TFT_I2C_POWER)
i2c_power.direction = digitalio.Direction.OUTPUT
i2c_power.value = True
i2c_success = False
i2c_chances = 5

print("Initializing I2C")
while (not i2c_success) and i2c_chances > 0:
    try:
        i2c = board.I2C()
        i2c_success = True
    except Exception as e:
        print(e)
        print("  I2C init failed, %d chances left" % i2c_chances)
        i2c_power.value = False
        time.sleep(0.1)
        i2c_power.value = True
        time.sleep(0.1)
        i2c_chances -= 1

if not i2c_success:
    raise RuntimeError("Failed to initialize i2c")


## NeoSlider
neoslider_address = 0x38
print("Connecting to NeoSlider at %x" % neoslider_address)

neoslider_success = False
neoslider_chances = 10
while (not neoslider_success) and neoslider_chances > 0:
    try:
        neoslider = Seesaw(i2c, neoslider_address)
        neoslider_success = True
    except Exception as e:
        print(e)
        print("  Retrying NeoSlider, %d chances left" % neoslider_chances)
        time.sleep(0.2)
        neoslider_chances -= 1

if not neoslider_success:
    raise RuntimeError("Could not connect to NeoSlider")

slider = AnalogInput(neoslider, 18)
slider_pixels = neopixel.NeoPixel(neoslider, 14, 4, pixel_order=neopixel.GRB)

## NeoKey
print("Setting up NeoKey")
neokey = NeoKey1x4(i2c, addr=0x30)
neokey_was_pressed = [False, False, False, False]


### CLIP CONFIG ---------------------------------------------------------------
NUM_CLIPS = 4

CLIP_LABELS = ["drums", "voice", "guitar", "keys"]

# CC per clip - 20..23 are unassigned in the MIDI spec
CLIP_CCS = [20, 21, 22, 23]

# Bright = clip playing; dim = idle
CLIP_BRIGHT = [
    0xFF0000,  # drums  - red
    0xFFAA00,  # voice  - amber/yellow
    0x00FF00,  # guitar - green
    0x00AAFF,  # keys   - cyan/blue
]
CLIP_DIM = [
    0x220000,
    0x221100,
    0x002200,
    0x001122,
]

# Values to send for press / release
CC_TRIGGER = 127
CC_RELEASE = 0

# Track which clips Loopy Pro reports as currently playing
playing = [False] * NUM_CLIPS

# Reverse lookup: CC -> clip index
cc_to_clip = {cc: i for i, cc in enumerate(CLIP_CCS)}


### SLIDER CONFIG -------------------------------------------------------------
SLIDER_CC = 7  # Volume
old_slider_cc_value = -1  # forces send on first read

def slider_to_cc_value(value):
    """Map slider 0..1023 to MIDI CC 0..127 (inverted to match physical fader)."""
    return int(adafruit_simplemath.map_range(value, 0, 1023, 127, 0))

def slider_to_color(value):
    return value / 1023 * 255


### LED HELPERS ---------------------------------------------------------------
def update_neokey_lights():
    for i in range(NUM_CLIPS):
        neokey.pixels[i] = CLIP_BRIGHT[i] if playing[i] else CLIP_DIM[i]


### SPRITE / DISPLAY ----------------------------------------------------------
tile_width = 32
tile_height = 32
sprite_scale = 4
sprite_width = tile_width * sprite_scale
sprite_height = tile_height * sprite_scale

spritesheet_filename = "loopy_sprites.bmp"
try:
    sprite_sheet, palette = adafruit_imageload.load(
        spritesheet_filename,
        bitmap=displayio.Bitmap,
        palette=displayio.Palette,
    )
except Exception as e:
    print("Missing %s - copy it to your CIRCUITPY drive" % spritesheet_filename)
    raise e

sprite = displayio.TileGrid(
    sprite_sheet, pixel_shader=palette,
    width=1, height=1,
    tile_width=tile_width, tile_height=tile_height,
)
group = displayio.Group(scale=sprite_scale)
group.append(sprite)
display.root_group = group
group.x = int(board.DISPLAY.width / 2 - sprite_width / 2)
group.y = int(board.DISPLAY.height / 2 - sprite_height / 2)

# Tile index = bitmask of which clips are playing. 16 tiles total.
#   bit 0 = drums, bit 1 = voice, bit 2 = guitar, bit 3 = keys
old_tile = -1


### USB MIDI ------------------------------------------------------------------
print("USB MIDI ports:")
print(usb_midi.ports)
if len(usb_midi.ports) == 0:
    print("No MIDI ports found, check that MIDI is enabled in boot.py")
    raise Exception("No MIDI port found")

midi_in_channel = 1
midi_out_channel = 1
midi = adafruit_midi.MIDI(
    midi_in=usb_midi.ports[0],
    midi_out=usb_midi.ports[1],
    in_channel=(midi_in_channel - 1),
    out_channel=(midi_out_channel - 1),
    debug=False,
)
print("MIDI out ch %d, in ch %d" % (midi.out_channel + 1, midi.in_channel + 1))
print("Clip CCs: %s   Slider CC: %d" % (CLIP_CCS, SLIDER_CC))

update_neokey_lights()
time.sleep(0.5)  # let MIDI reconnect on board reset


### MAIN LOOP -----------------------------------------------------------------
while True:

    # --- Slider -> CC ------------------------------------------------------
    new_slider_cc_value = slider_to_cc_value(slider.value)
    if new_slider_cc_value != old_slider_cc_value:
        midi.send(ControlChange(SLIDER_CC, new_slider_cc_value))
        if serial_debug:
            print("slider CC %d = %d" % (SLIDER_CC, new_slider_cc_value))
        slider_pixels.fill(colorwheel(slider_to_color(slider.value)))
        old_slider_cc_value = new_slider_cc_value

    # --- Buttons -> trigger clip ------------------------------------------
    for i in range(NUM_CLIPS):
        cc = CLIP_CCS[i]
        if neokey[i] and not neokey_was_pressed[i]:
            midi.send(ControlChange(cc, CC_TRIGGER))
            if serial_debug:
                print("trigger %s -> CC %d = %d" %
                      (CLIP_LABELS[i], cc, CC_TRIGGER))
            neokey_was_pressed[i] = True
        elif neokey_was_pressed[i] and not neokey[i]:
            midi.send(ControlChange(cc, CC_RELEASE))
            neokey_was_pressed[i] = False

    # --- Incoming MIDI from Loopy Pro --------------------------------------
    msg = midi.receive()
    while msg is not None:
        if isinstance(msg, ControlChange) and msg.control in cc_to_clip:
            i = cc_to_clip[msg.control]
            is_playing = msg.value > 0
            if playing[i] != is_playing:
                playing[i] = is_playing
                if serial_debug:
                    print("%s %s cc%d=%d" %
                          ("PLAY" if is_playing else "STOP",
                           CLIP_LABELS[i], msg.control, msg.value))
                update_neokey_lights()
        msg = midi.receive()

    # --- Sprite reflects exactly which clips are playing -------------------
    new_tile = sum(1 << i for i, p in enumerate(playing) if p)
    if new_tile != old_tile:
        sprite[0] = new_tile
        old_tile = new_tile
