# SPDX-FileCopyrightText: 2026 Michael Ang for NYUADIM Music Devices
# SPDX-License-Identifier: MIT
#
# loopy_grid -- Loopy Pro 4x4 clip-launcher controller for the Adafruit
# ESP32-S3 Reverse TFT Feather + NeoKey 1x4 + NeoSlider.
#
# Layout in Loopy Pro:
#   - A template with 4 rows of 4 clips
#   - Each COLUMN is one instrument color (Loopy Pro default palette):
#       column 0 = drums   (orange)
#       column 1 = voice   (yellow)
#       column 2 = guitar  (lime)
#       column 3 = keys    (blue)
#
# Controls:
#   - The 4 NeoKey buttons trigger the clip in the SELECTED row for their column
#     (button 0 -> drums, 1 -> voice, 2 -> guitar, 3 -> keys), left-to-right.
#   - The slider chooses which row (0..3) is currently being controlled.
#
# MIDI convention (matches https://wiki.loopypro.com/Troubleshooting_MIDI):
#   - "ON event"  = CC value > 0  (we send 127, the preferred value)
#   - "OFF event" = CC value == 0
# Loopy Pro distinguishes ON from OFF on the same CC number.
#
# Outgoing (controller -> Loopy Pro):
#   - Press   -> ControlChange(cc, 127)   ON
#   - Release -> ControlChange(cc, 0)     OFF
#   Map the ON edge in Loopy Pro to "start clip" and OFF to "stop clip"
#   (or assign just the ON edge to "toggle").
#
# Incoming feedback (Loopy Pro -> controller):
#   - Clip started -> ControlChange(cc, 127)   ON
#   - Clip stopped -> ControlChange(cc, 0)     OFF
#   The NeoKey for each column lights bright in the column color when the clip
#   in the CURRENTLY SELECTED row is playing, dim otherwise. The 4 NeoSlider
#   pixels show which row is selected (and which other rows have any active
#   clip). LED state is driven only by feedback, so what you see is what
#   Loopy Pro actually did.
#
# Set up Loopy Pro to send the same CC back to the controller's input port
# whenever a clip starts/stops. Simplest: in each clip's MIDI settings add an
# outgoing CC matching the trigger CC, value 127 on play, 0 on stop.
#
# CC grid (default - using CCs 20..35 which are unassigned in the MIDI spec):
#   row 0 -> CC 20, 21, 22, 23
#   row 1 -> CC 24, 25, 26, 27
#   row 2 -> CC 28, 29, 30, 31
#   row 3 -> CC 32, 33, 34, 35

import adafruit_simplemath
import board
import digitalio
import time

display = board.DISPLAY
display.rotation = 180

print("loopy_grid")

serial_debug = True
if serial_debug:
    print("Serial debug ON - turn off for faster response")

time.sleep(0.5)

# Display / graphics
import displayio
import adafruit_imageload

# NeoKey / NeoSlider
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


### GRID CONFIG ---------------------------------------------------------------
NUM_ROWS = 4
NUM_COLS = 4

COLUMN_LABELS = ["drums", "voice", "guitar", "keys"]

# Column colors. Bright = currently-playing clip in selected row.
# Dim = idle. Match Loopy Pro's default clip palette.
COLUMN_BRIGHT = [
    0xFF6E00,  # drums  - orange
    0xFFE600,  # voice  - yellow
    0x9BFF1F,  # guitar - lime
    0x1E82FF,  # keys   - blue
]
COLUMN_DIM = [
    0x2A1200,
    0x2A2600,
    0x182A05,
    0x05162A,
]

# 4x4 grid of MIDI Control Change numbers. cc_grid[row][col] is the CC Loopy
# Pro listens for (and is expected to echo back when the clip is playing).
cc_grid = [
    [20, 21, 22, 23],  # row 0
    [24, 25, 26, 27],  # row 1
    [28, 29, 30, 31],  # row 2
    [32, 33, 34, 35],  # row 3
]

# ON / OFF event values per the Loopy Pro wiki convention.
# https://wiki.loopypro.com/Troubleshooting_MIDI
CC_ON  = 127  # preferred ON value
CC_OFF = 0    # OFF value

# Track which clips Loopy Pro reports as currently playing. Mirrors cc_grid.
playing = [[False] * NUM_COLS for _ in range(NUM_ROWS)]

# Current selected row from the slider
selected_row = 0


### SLIDER -> ROW MAPPING -----------------------------------------------------
# Use hysteresis so jitter at zone boundaries doesn't flip the selected row.
ROW_THRESHOLDS_UP   = [256, 512, 768]   # crossing upward to enter rows 1, 2, 3
ROW_THRESHOLDS_DOWN = [192, 448, 704]   # crossing downward to leave rows 1, 2, 3

def row_from_slider(value, current_row):
    """Convert raw slider value (0..1023) to a row index (0..3) with hysteresis."""
    r = current_row
    # Move up
    while r < NUM_ROWS - 1 and value > ROW_THRESHOLDS_UP[r]:
        r += 1
    # Move down
    while r > 0 and value < ROW_THRESHOLDS_DOWN[r - 1]:
        r -= 1
    return r


### LED HELPERS ---------------------------------------------------------------
def update_neokey_lights():
    """Light each key in its column color, brightly if that clip in the selected
    row is playing, dimly otherwise."""
    for col in range(NUM_COLS):
        if playing[selected_row][col]:
            neokey.pixels[col] = COLUMN_BRIGHT[col]
        else:
            neokey.pixels[col] = COLUMN_DIM[col]

def update_slider_lights():
    """Show selected row on the slider's 4 pixels.
    The selected row pixel is white; other rows show a dim hint if any clip in
    that row is currently playing, otherwise off."""
    for r in range(NUM_ROWS):
        if r == selected_row:
            slider_pixels[r] = 0x444444  # white = selected
        elif any(playing[r]):
            slider_pixels[r] = 0x080808  # very dim = something playing here
        else:
            slider_pixels[r] = 0x000000


### SPRITE / DISPLAY ----------------------------------------------------------
tile_width = 32
tile_height = 32
sprite_scale = 4
sprite_width = tile_width * sprite_scale
sprite_height = tile_height * sprite_scale

spritesheet_filename = "spritesheet.gif"
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

# Tile 0 = idle, tiles 1..4 = rows 1..4 selected
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
print("MIDI out channel: %d, in channel: %d" % (midi.out_channel + 1, midi.in_channel + 1))

# Quick lookup: CC number -> (row, col)
cc_to_cell = {}
for r in range(NUM_ROWS):
    for c in range(NUM_COLS):
        cc_to_cell[cc_grid[r][c]] = (r, c)


### INIT VISUALS --------------------------------------------------------------
selected_row = row_from_slider(slider.value, 0)
update_neokey_lights()
update_slider_lights()

time.sleep(0.5)  # let MIDI reconnect on board reset


### MAIN LOOP -----------------------------------------------------------------
while True:

    # --- Slider -> row selection -------------------------------------------
    new_row = row_from_slider(slider.value, selected_row)
    if new_row != selected_row:
        selected_row = new_row
        if serial_debug:
            print("Row -> %d (%s)" % (selected_row, COLUMN_LABELS))
        update_neokey_lights()
        update_slider_lights()

    # --- Buttons -> send ON on press, OFF on release ----------------------
    for col in range(NUM_COLS):
        cc = cc_grid[selected_row][col]
        if neokey[col] and not neokey_was_pressed[col]:
            midi.send(ControlChange(cc, CC_ON))
            if serial_debug:
                print("send ON  %s row %d cc%d=%d" %
                      (COLUMN_LABELS[col], selected_row, cc, CC_ON))
            neokey_was_pressed[col] = True

        elif neokey_was_pressed[col] and not neokey[col]:
            midi.send(ControlChange(cc, CC_OFF))
            if serial_debug:
                print("send OFF %s row %d cc%d=%d" %
                      (COLUMN_LABELS[col], selected_row, cc, CC_OFF))
            neokey_was_pressed[col] = False

    # --- Incoming feedback from Loopy Pro ---------------------------------
    # Per the wiki: ON  = CC value > 0  -> clip is playing
    #               OFF = CC value == 0 -> clip is stopped
    msg = midi.receive()
    while msg is not None:
        if isinstance(msg, ControlChange):
            cell = cc_to_cell.get(msg.control)
            if cell is not None:
                r, c = cell
                is_on = msg.value > 0
                if playing[r][c] != is_on:
                    playing[r][c] = is_on
                    if serial_debug:
                        print("recv %s r%d c%d (%s) cc%d=%d" %
                              ("ON " if is_on else "OFF",
                               r, c, COLUMN_LABELS[c], msg.control, msg.value))
                    update_neokey_lights()
                    update_slider_lights()
        msg = midi.receive()

    # --- Sprite shows the selected row -------------------------------------
    new_tile = selected_row + 1
    if new_tile != old_tile:
        sprite[0] = new_tile
        old_tile = new_tile
