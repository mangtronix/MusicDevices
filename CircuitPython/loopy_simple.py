# SPDX-FileCopyrightText: 2026 Michael Ang for NYUADIM Music Devices
# SPDX-License-Identifier: MIT
#
# loopy_simple -- 4-clip Loopy Pro controller for the Adafruit ESP32-S3
# Reverse TFT Feather + NeoKey 1x4 + NeoSlider.
#
# Layout in Loopy Pro:
#   - One row of 4 clips, left to right (colors match Loopy Pro defaults):
#       button 0 = drums   (orange)
#       button 1 = voice   (yellow)
#       button 2 = guitar  (lime)
#       button 3 = keys    (blue)
#
# MIDI convention (matches https://wiki.loopypro.com/Troubleshooting_MIDI):
#   - "ON event"  = CC value > 0  (we send 127, the preferred value)
#   - "OFF event" = CC value == 0
# Loopy Pro distinguishes ON from OFF on the same CC number, so the same CC
# carries press / release on the way out and play / stop on the way back.
#
# Outgoing (controller -> Loopy Pro):
#   - Press   -> ControlChange(cc, 127)   ON
#   - Release -> ControlChange(cc, 0)     OFF
#   In Loopy Pro's MIDI Learn dialog you can assign the ON edge to "start clip"
#   and the OFF edge to "stop clip", or assign just the ON edge to "toggle".
#
# Incoming feedback (Loopy Pro -> controller):
#   - Clip started -> ControlChange(cc, 127)   ON  -> NeoKey bright
#   - Clip stopped -> ControlChange(cc, 0)     OFF -> NeoKey dim
#   The LED state is driven only by feedback, so what you see on the keys is
#   what Loopy Pro is actually doing -- not what you tried to do.
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
#
# === Setting up the mapping in Loopy Pro 2.0 =================================
# 1. Plug the controller in. Loopy Pro picks it up automatically.
#
# 2. Enter MIDI Learn mode:
#      Tap the hamburger icon (upper right) -> "MIDI Learn".
#    The screen now shows a "MIDI Learn" panel along the bottom.
#
# 3. Map each clip to its button:
#      a. Tap the clip you want to control.
#      b. Press the matching NeoKey button on the controller -- the panel
#         shows the CC it just learned.
#      c. Tap the bottom panel to open the binding's options. Set the action
#         to "Toggle" (one press starts the clip, next press stops it).
#      Repeat for the other 3 clips.
#
#    Feedback (the CC that lights up the NeoKey when the clip is playing) is
#    sent automatically -- there is no extra option to enable.
#
# 4. Map the slider (still in MIDI Learn mode):
#      a. Tap the master volume fader (or any knob you want).
#      b. Move the slider on the controller -- it learns CC 7.
#
# 5. Tap "Done" / exit MIDI Learn mode (hamburger -> MIDI Learn again).
#
# That's it. Press a button -> the clip toggles -> the NeoKey lights up.
# Press again -> the clip stops -> the NeoKey dims.
# =============================================================================

import adafruit_simplemath
import board
import digitalio
import time

display = board.DISPLAY
display.rotation = 180

print("loopy_simple")

serial_debug = False
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


### CLIP CONFIG ---------------------------------------------------------------
NUM_CLIPS = 4

CLIP_LABELS = ["drums", "voice", "guitar", "keys"]

# CC per clip - 20..23 are unassigned in the MIDI spec
CLIP_CCS = [20, 21, 22, 23]

# Bright = clip playing; dim = idle. Colors match Loopy Pro's default
# clip palette: orange, yellow, lime, blue.
CLIP_BRIGHT = [
    0xFF6E00,  # drums  - orange
    0xFFE600,  # voice  - yellow
    0x9BFF1F,  # guitar - lime
    0x1E82FF,  # keys   - blue
]
CLIP_DIM = [
    0x2A1200,
    0x2A2600,
    0x182A05,
    0x05162A,
]

# ON / OFF event values per the Loopy Pro wiki convention.
# https://wiki.loopypro.com/Troubleshooting_MIDI
CC_ON  = 127  # preferred ON value
CC_OFF = 0    # OFF value

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


### LED HELPERS ---------------------------------------------------------------
def update_neokey_lights():
    for i in range(NUM_CLIPS):
        neokey.pixels[i] = CLIP_BRIGHT[i] if playing[i] else CLIP_DIM[i]

def update_slider_lights(cc_value):
    """Show the slider's value (0..127) as a vertical level meter on the
    NeoSlider's 4 LEDs, filling from bottom (LED 0) to top (LED 3) in pure
    blue. Each LED covers a quarter of the range; the partially-filled LED
    uses scaled brightness so the fill looks smooth between LED steps.

    Called both locally (when the controller sends a CC update) and on
    feedback from Loopy Pro, so the lights stay in sync regardless of which
    side moved the value."""
    step = 127.0 / 4  # 31.75 -- range each LED covers
    for i in range(4):
        led_min = i * step
        if cc_value >= led_min + step:
            blue = 255              # fully lit
        elif cc_value <= led_min:
            blue = 0                # off
        else:
            blue = int((cc_value - led_min) / step * 255)  # partial
        slider_pixels[3 -i] = blue     # 0x0000BB -- pure blue, scaled brightness


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

midi_out_channel = 1
midi = adafruit_midi.MIDI(
    midi_in=usb_midi.ports[0],
    midi_out=usb_midi.ports[1],
    # Listen on ALL channels for incoming feedback. Loopy Pro can send echoes
    # on a channel different from the one we send on, so a strict in_channel
    # filter silently drops feedback messages.
    in_channel=tuple(range(16)),
    out_channel=(midi_out_channel - 1),
    debug=False,
)
print("MIDI out ch %d, listening on all channels for feedback" % (midi.out_channel + 1))
print("Clip CCs: %s   Slider CC: %d" % (CLIP_CCS, SLIDER_CC))

update_neokey_lights()
update_slider_lights(0)  # start the slider LEDs off; Loopy Pro feedback will fill them in
time.sleep(0.5)  # let MIDI reconnect on board reset


### MAIN LOOP -----------------------------------------------------------------
while True:

    # --- Slider -> CC ------------------------------------------------------
    # Loopy Pro only sends fader feedback when the change originates inside
    # the app (e.g. the on-screen fader is touched), so we drive the LEDs
    # locally on physical slider movement and ALSO accept feedback below for
    # changes that come from Loopy Pro.
    new_slider_cc_value = slider_to_cc_value(slider.value)
    if new_slider_cc_value != old_slider_cc_value:
        midi.send(ControlChange(SLIDER_CC, new_slider_cc_value))
        if serial_debug:
            print("slider CC %d = %d" % (SLIDER_CC, new_slider_cc_value))
        update_slider_lights(new_slider_cc_value)
        old_slider_cc_value = new_slider_cc_value

    # --- Buttons -> send ON on press, OFF on release ----------------------
    for i in range(NUM_CLIPS):
        cc = CLIP_CCS[i]
        if neokey[i] and not neokey_was_pressed[i]:
            midi.send(ControlChange(cc, CC_ON))
            if serial_debug:
                print("send ON  %s cc%d=%d" % (CLIP_LABELS[i], cc, CC_ON))
            neokey_was_pressed[i] = True
        elif neokey_was_pressed[i] and not neokey[i]:
            midi.send(ControlChange(cc, CC_OFF))
            if serial_debug:
                print("send OFF %s cc%d=%d" % (CLIP_LABELS[i], cc, CC_OFF))
            neokey_was_pressed[i] = False

    # --- Incoming feedback from Loopy Pro ---------------------------------
    # Clip CCs:   ON  = value > 0  -> clip is playing  (NeoKey bright)
    #             OFF = value == 0 -> clip is stopped  (NeoKey dim)
    # Slider CC: value 0..127      -> slider LEDs fade off..full pure blue
    # Anything else is logged when serial_debug is on so you can see what
    # Loopy Pro is actually sending back -- useful for diagnosing missing
    # feedback (e.g. CC numbers or channels you didn't expect).
    msg = midi.receive()
    while msg is not None:
        if isinstance(msg, ControlChange):
            if msg.control in cc_to_clip:
                i = cc_to_clip[msg.control]
                is_on = msg.value > 0
                if playing[i] != is_on:
                    playing[i] = is_on
                    if serial_debug:
                        print("recv %s %s cc%d=%d" %
                              ("ON " if is_on else "OFF",
                               CLIP_LABELS[i], msg.control, msg.value))
                    update_neokey_lights()
            elif msg.control == SLIDER_CC:
                if serial_debug:
                    print("recv slider cc%d=%d" % (msg.control, msg.value))
                update_slider_lights(msg.value)
            else:
                if serial_debug:
                    print("recv unknown cc%d=%d (ch %s)" %
                          (msg.control, msg.value, getattr(msg, "channel", "?")))
        else:
            if serial_debug:
                print("recv non-CC:", msg)
        msg = midi.receive()

    # --- Sprite reflects exactly which clips are playing -------------------
    new_tile = sum(1 << i for i, p in enumerate(playing) if p)
    if new_tile != old_tile:
        sprite[0] = new_tile
        old_tile = new_tile
