# midi_particles.py
# CircuitPython controller designed to work with Web Example 04 — Notes + CC
#
# Written with Claude inside Visual Studio Code based
# on handwritten code spritekeys.py by Michael Ang
#
# Hardware
#   Adafruit ESP32-S3 Reverse TFT Feather
#   Adafruit NeoKey 1x4 QT  (default I2C addr 0x30)
#   Adafruit NeoSlider       (I2C addr 0x38, A3 pad cut)
#
# What it sends over USB MIDI
#   NeoKey buttons → NoteOn / NoteOff  (E-minor pentatonic, ch 1)
#   NeoSlider      → CC 74             (controls gravity in the web visualiser)
#
# Display
#   Idle:           floating star pattern
#   Button pressed: explosion sprite matching that button's colour
#
# Setup
#   1. Make sure boot.py enables USB MIDI (it should already do this).
#   2. Copy this file to CIRCUITPY/code.py  (or import it from code.py).
#
# Custom keycaps
#   Available at https://www.tinkercad.com/things/gZI03QlbHj2-04-p5-controller

import time
import board
import digitalio
import adafruit_simplemath
import displayio
import adafruit_imageload
import adafruit_midi
import usb_midi
from adafruit_midi.control_change import ControlChange
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_seesaw.seesaw import Seesaw
from adafruit_seesaw.analoginput import AnalogInput
from adafruit_seesaw import neopixel
from adafruit_neokey.neokey1x4 import NeoKey1x4

# ─── Config ───────────────────────────────────────────────────────────────────
serial_debug = True          # set False for faster response in performance

# MIDI notes for the 4 NeoKey buttons — E-minor pentatonic (matches web ex. 04)
NOTES    = [64, 67, 69, 71]  # E4, G4, A4, B4
VELOCITY = 100

# CC number for the slider (CC 74 = Filter Cutoff; used as "gravity" in ex. 04)
CC_NUMBER = 74

# NeoKey colours matching the particle colours in the web visualiser
# off = dim version, on = bright version
KEY_OFF_COLORS = [
    0x33002A,   # dim pink     (note 64)
    0x332200,   # dim yellow   (note 67)
    0x003300,   # dim green    (note 69)
    0x003325,   # dim cyan     (note 71)
]
KEY_ON_COLORS = [
    0xFF33BD,   # bright pink
    0xFFDD33,   # bright yellow
    0x55FF33,   # bright green
    0x33FFDD,   # bright cyan
]

# Tile indices in particles_sprites.bmp
SPRITE_IDLE     = 0
SPRITE_KEYS     = [1, 2, 3, 4]   # one per button, matching note colours

# ─── Display ──────────────────────────────────────────────────────────────────
display = board.DISPLAY
display.rotation = 180           # flip so buttons are on the right

TILE_W       = 32
TILE_H       = 32
SPRITE_SCALE = 4                 # 32 × 4 = 128 px on screen

# ─── I2C ──────────────────────────────────────────────────────────────────────
i2c_power = digitalio.DigitalInOut(board.TFT_I2C_POWER)
i2c_power.direction = digitalio.Direction.OUTPUT
i2c_power.value = True

print("Initializing I2C")
i2c = None
for attempt in range(5):
    try:
        i2c = board.I2C()
        break
    except Exception as e:
        print(f"  I2C attempt {attempt + 1} failed: {e}")
        i2c_power.value = False
        time.sleep(0.1)
        i2c_power.value = True
        time.sleep(0.1)

if i2c is None:
    raise RuntimeError("Could not initialise I2C")

# ─── NeoSlider ────────────────────────────────────────────────────────────────
NEOSLIDER_ADDR = 0x38   # A3 pad cut to avoid conflict with NeoKey at 0x30
print(f"Connecting to NeoSlider at 0x{NEOSLIDER_ADDR:02x}")

neoslider = None
for attempt in range(10):
    try:
        neoslider = Seesaw(i2c, NEOSLIDER_ADDR)
        break
    except Exception as e:
        print(f"  NeoSlider attempt {attempt + 1} failed: {e}")
        time.sleep(0.2)

if neoslider is None:
    raise RuntimeError("Could not connect to NeoSlider")

slider        = AnalogInput(neoslider, 18)
slider_pixels = neopixel.NeoPixel(neoslider, 14, 4, pixel_order=neopixel.GRB)
old_cc_value  = None   # force a send on the first loop

def slider_to_cc(raw):
    """Map raw slider value (0–1023) to MIDI CC (0–127), inverted so
    sliding up increases the value."""
    return int(adafruit_simplemath.map_range(raw, 0, 1023, 127, 0))

def gravity_color(cc_val):
    """Return (R, G, B) for the slider NeoPixels.
    Blue = floating (low CC), white = neutral (mid), red = falling (high CC).
    This gives the slider a visual meaning that matches the web visualiser."""
    if cc_val < 64:
        t = cc_val / 63.0
        return (int(t * 255), int(t * 200), 255)
    else:
        t = (cc_val - 64) / 63.0
        return (255, int((1 - t) * 200), int((1 - t) * 255))

# ─── NeoKey ───────────────────────────────────────────────────────────────────
print("Setting up NeoKey")
neokey          = NeoKey1x4(i2c, addr=0x30)
key_was_pressed = [False, False, False, False]

for i in range(4):
    neokey.pixels[i] = KEY_OFF_COLORS[i]

# ─── Display / sprites ────────────────────────────────────────────────────────
SPRITESHEET = "particles_sprites.bmp"
print(f"Loading {SPRITESHEET}")

try:
    sprite_sheet, palette = adafruit_imageload.load(
        SPRITESHEET,
        bitmap=displayio.Bitmap,
        palette=displayio.Palette,
    )
except Exception as e:
    print(f"Missing {SPRITESHEET} — run generate_particles_sprites.py on your")
    print("computer first, then copy the .bmp to your CIRCUITPY drive.")
    raise e

sprite = displayio.TileGrid(
    sprite_sheet,
    pixel_shader=palette,
    width=1, height=1,
    tile_width=TILE_W, tile_height=TILE_H,
)

group = displayio.Group(scale=SPRITE_SCALE)
group.append(sprite)
display.root_group = group

# Centre the sprite on the screen
group.x = int(display.width  / 2 - TILE_W * SPRITE_SCALE / 2)
group.y = int(display.height / 2 - TILE_H * SPRITE_SCALE / 2)

sprite[0]        = SPRITE_IDLE
current_sprite   = SPRITE_IDLE

# ─── USB MIDI ─────────────────────────────────────────────────────────────────
print("USB MIDI ports:", usb_midi.ports)
if not usb_midi.ports:
    raise RuntimeError(
        "No MIDI ports found — check that boot.py enables USB MIDI.\n"
        "See https://learn.adafruit.com/customizing-usb-devices-in-circuitpython/"
        "circuitpy-midi-serial#midi-3096586"
    )

MIDI_CHANNEL = 1
midi = adafruit_midi.MIDI(
    midi_in=usb_midi.ports[0],
    midi_out=usb_midi.ports[1],
    in_channel=MIDI_CHANNEL - 1,
    out_channel=MIDI_CHANNEL - 1,
    debug=False,
)
print(f"MIDI output channel: {midi.out_channel + 1}")

def notes_off():
    for note in NOTES:
        midi.send(NoteOff(note, 0))

# Send NoteOff for all notes in case any were left hanging after a reset
time.sleep(0.5)
notes_off()
print("Ready — press buttons, move the slider")

# ─── Main loop ────────────────────────────────────────────────────────────────
while True:

    # ── NeoSlider → CC 74 (gravity) ──────────────────────────────────────────
    new_cc = slider_to_cc(slider.value)

    if new_cc != old_cc_value:
        midi.send(ControlChange(CC_NUMBER, new_cc))
        slider_pixels.fill(gravity_color(new_cc))

        if serial_debug:
            direction = "↑ float" if new_cc < 55 else ("↓ fall" if new_cc > 72 else "~ weightless")
            print(f"Slider CC {CC_NUMBER} = {new_cc:3d}  {direction}")

        old_cc_value = new_cc

    # ── NeoKey buttons → NoteOn / NoteOff ───────────────────────────────────
    new_sprite = SPRITE_IDLE   # will stay idle unless a button is held

    for i in range(4):
        pressed = neokey[i]

        if pressed and not key_was_pressed[i]:
            # ── just pressed ──
            midi.send(NoteOn(NOTES[i], VELOCITY))
            neokey.pixels[i] = KEY_ON_COLORS[i]
            if serial_debug:
                print(f"Key {i} pressed  → NoteOn  {NOTES[i]}")
            key_was_pressed[i] = True

        elif key_was_pressed[i] and not pressed:
            # ── just released ──
            midi.send(NoteOff(NOTES[i], 0))
            neokey.pixels[i] = KEY_OFF_COLORS[i]
            if serial_debug:
                print(f"Key {i} released → NoteOff {NOTES[i]}")
            key_was_pressed[i] = False

        # Show the highest-indexed pressed button's sprite
        # (if multiple held, last one wins — easy to change)
        if key_was_pressed[i]:
            new_sprite = SPRITE_KEYS[i]

    # ── Update display only when the sprite actually changes ─────────────────
    if new_sprite != current_sprite:
        sprite[0]      = new_sprite
        current_sprite = new_sprite
