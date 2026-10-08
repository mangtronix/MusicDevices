# SPDX-FileCopyrightText: 2026 Michael Ang with Claude Opus 5.5 for Music Devices
#
# SPDX-License-Identifier: MIT

print("fruitjam_synth")

# Polyphonic synthesizer for the Adafruit Fruit Jam. Plug a USB MIDI keyboard
# into one of the Fruit Jam's USB-A ports and listen on the headphone jack.
# You can also play it from your computer (Ableton, etc.) over the USB-C
# cable: the Fruit Jam shows up as a MIDI device called "CircuitPython".
#
# Controls:
#   Keys             play notes (louder when you hit harder)
#   Mod wheel (CC1)  opens/closes a low-pass filter (brighter / darker sound)
#   Pitch bend       bends held notes up/down by 2 semitones
#   Button 1         change waveform: sine -> triangle -> saw -> square
#   Button 2 / 3     octave down / up
#   NeoPixels        color shows the waveform; one pixel lights per held note
#
# Libraries: install into CIRCUITPY/lib with
#   circup install adafruit_fruitjam adafruit_midi adafruit_usb_host_midi
# Needs CircuitPython 10.x for the "Adafruit Fruit Jam":
#   https://circuitpython.org/board/adafruit_fruit_jam/
#
# Setup:
#   1. Copy this file to CIRCUITPY.
#   2. Run it from code.py with "import fruitjam_synth", or save it as code.py.
#   3. Plug in the MIDI keyboard (best before powering on the Fruit Jam) and
#      headphones. Use a USB cable that carries data, not a charge-only one.

import time

import audiomixer
import synthio
import ulab.numpy as np
import usb.core
import usb_midi

import adafruit_midi
import adafruit_usb_host_midi
from adafruit_fruitjam.peripherals import Peripherals
from adafruit_midi.control_change import ControlChange
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_midi.pitch_bend import PitchBend

# --- Settings you might want to change ---
SAMPLE_RATE = 44100
VOLUME = 0.5  # 0.0 - 0.75 (the library blocks louder values to protect ears/speakers)
BEND_RANGE = 2  # pitch bend range in semitones

# --- Hardware setup ---
# The Fruit Jam's audio chip (a "DAC") turns numbers into sound for the
# headphone jack. Peripherals() sets it up along with the buttons and
# NeoPixels. synthio is CircuitPython's built-in synthesizer: we start it
# playing once and it keeps running in the background, so pressing a note
# later makes sound right away.
# The synth plays through a mixer only to get a bigger audio buffer. Reading
# the USB keyboard sometimes pauses our code for longer than synthio's own
# small buffer lasts, which causes clicks. 2048 bytes is about
# 23 ms of sound: enough to ride out the pauses without making notes
# noticeably late. Bigger = safer but laggier.
fruit_jam = Peripherals(audio_output="headphone", sample_rate=SAMPLE_RATE)
fruit_jam.volume = VOLUME
synth = synthio.Synthesizer(sample_rate=SAMPLE_RATE)
mixer = audiomixer.Mixer(sample_rate=SAMPLE_RATE, channel_count=1, buffer_size=2048)
fruit_jam.audio.play(mixer)
mixer.voice[0].play(synth)

# NeoPixels: dim, and only update when we call show() so all 5 change at once
fruit_jam.neopixels.brightness = 0.1
fruit_jam.neopixels.auto_write = False

# --- Sound design ---
# The character of the sound comes from three things:
#   waveform  - the shape of one vibration (sine is pure, saw/square are buzzy)
#   envelope  - how the volume changes over time (fade in, hold, fade out)
#   filter    - removes high frequencies to make the sound darker
# Each waveform is one cycle of 256 samples. The color is shown on the
# NeoPixels so you can see which one is selected.
SIZE = 256
VOLUME_MAX = 32000
ramp = np.linspace(-VOLUME_MAX, VOLUME_MAX, num=SIZE, endpoint=False, dtype=np.int16)
WAVEFORMS = [
    ("sine", np.array(np.sin(np.linspace(0, 2 * np.pi, SIZE, endpoint=False)) * VOLUME_MAX,
                      dtype=np.int16), 0x0040FF),
    ("triangle", np.array(abs(np.linspace(-1, 1, SIZE, endpoint=False)) * 2 * VOLUME_MAX
                          - VOLUME_MAX, dtype=np.int16), 0x00FF40),
    ("saw", ramp, 0xFF8000),
    ("square", np.concatenate((np.ones(SIZE // 2, dtype=np.int16) * VOLUME_MAX,
                               np.ones(SIZE // 2, dtype=np.int16) * -VOLUME_MAX)), 0xFF0040),
]
waveform_index = 2  # start on saw, it shows off the filter

# Quick attack, short decay down to 70%, and a gentle 0.4 s fade after release
envelope = synthio.Envelope(
    attack_time=0.01, decay_time=0.2, release_time=0.4,
    attack_level=1.0, sustain_level=0.7,
)

# One filter shared by all notes, so the mod wheel changes every held note
lowpass = synthio.Biquad(synthio.FilterMode.LOW_PASS, frequency=4000, Q=1.0)
# Same idea for pitch bend: one shared value that every note follows
pitch_bend = synthio.LFO(rate=0, offset=0, scale=0)  # constant value we set by hand

# --- Playing notes ---
# synthio needs the same Note object to stop a note that it used to start it,
# so we remember each sounding note by its MIDI note number. This is what
# makes chords work: several notes can be held at once, and each key's
# release stops only its own note.
octave = 0
notes = {}  # MIDI note number -> synthio.Note currently sounding


def note_on(note_number, velocity):
    if note_number in notes:
        synth.release(notes[note_number])
    note = synthio.Note(
        frequency=synthio.midi_to_hz(note_number + 12 * octave),
        waveform=WAVEFORMS[waveform_index][1],
        envelope=envelope,
        amplitude=0.2 + 0.4 * velocity / 127,  # keep headroom for chords
        filter=lowpass,
        bend=pitch_bend,
    )
    notes[note_number] = note
    synth.press(note)


def note_off(note_number):
    note = notes.pop(note_number, None)
    if note is not None:
        synth.release(note)


# Light one pixel per held note, in the current waveform's color
def show_pixels():
    color = WAVEFORMS[waveform_index][2]
    fruit_jam.neopixels.fill(0)
    fruit_jam.neopixels[0] = color  # always show the waveform color
    for i in range(min(len(notes), 5)):
        fruit_jam.neopixels[i] = color
    fruit_jam.neopixels.show()


# --- MIDI inputs ---
# Two places MIDI can come from, and both feed the same synth:
#   - the computer, over the USB-C cable (always connected)
#   - a MIDI keyboard on the USB-A ports, where the Fruit Jam acts as the
#     "host", like a computer would. The keyboard might be plugged in late or
#     unplugged, so we keep looking for it instead of waiting at startup.
computer_midi = adafruit_midi.MIDI(midi_in=usb_midi.ports[0])
keyboard_midi = None
last_scan = 0


# Check each USB device and use the first one that sends MIDI.
# timeout: how long each read waits for the keyboard, in seconds. In
# CircuitPython 10.x a message that arrives just as a read times out can be
# lost (stuck or missing notes), so fewer timeouts = fewer lost notes. 20 ms
# keeps losses rare while the buttons still feel instant. (0 is not
# allowed: it would wait forever.)
# See https://github.com/adafruit/circuitpython/issues/10554
def find_keyboard():
    for device in usb.core.find(find_all=True):
        try:
            raw_midi = adafruit_usb_host_midi.MIDI(device, timeout=0.02)
        except (ValueError, usb.core.USBError):
            continue
        if raw_midi.in_ep == 0:
            continue  # not a MIDI device (e.g. a computer keyboard or mouse)
        print("Found MIDI keyboard:", hex(device.idVendor), hex(device.idProduct))
        return adafruit_midi.MIDI(midi_in=raw_midi)
    return None


# --- Responding to MIDI ---
# Turn each incoming MIDI message into a change in the sound. Messages we
# don't use (other CCs, aftertouch, clock...) are ignored.
def handle(msg):
    if isinstance(msg, NoteOn) and msg.velocity > 0:
        note_on(msg.note, msg.velocity)
    elif isinstance(msg, NoteOff) or isinstance(msg, NoteOn):  # NoteOn velocity 0 = off
        note_off(msg.note)
    elif isinstance(msg, ControlChange) and msg.control == 1:
        # mod wheel 0-127 -> filter cutoff 200 Hz - 8 kHz (exponential feels natural)
        lowpass.frequency = 200 * (40 ** (msg.value / 127))
    elif isinstance(msg, PitchBend):
        # 0-16383, center 8192 -> bend in octaves
        pitch_bend.offset = (msg.pitch_bend - 8192) / 8192 * BEND_RANGE / 12
    else:
        return
    show_pixels()


# --- Startup chime so you know the audio works ---
for n in (60, 64, 67, 72):
    note_on(n, 80)
    show_pixels()
    time.sleep(0.12)
    note_off(n)
time.sleep(0.3)
show_pixels()
print("Waveform:", WAVEFORMS[waveform_index][0])

# --- Main loop ---
# Runs over and over, very quickly. Each time through it checks every input
# once and never waits, so a note played on the keyboard is heard right away
# even while we're also watching the computer and the buttons.
buttons_were = (False, False, False)

while True:
    # Look for a USB keyboard every 2 seconds until one is found
    if keyboard_midi is None and time.monotonic() - last_scan > 2:
        last_scan = time.monotonic()
        keyboard_midi = find_keyboard()

    # receive() gives one message at a time, so keep going until there are
    # none left. Otherwise, releasing a chord would queue up note-offs that
    # fall behind (or seem to get lost, leaving notes stuck on).
    msg = computer_midi.receive()
    while msg is not None:
        handle(msg)
        msg = computer_midi.receive()

    # If the keyboard is unplugged, reading fails: forget it and look again
    if keyboard_midi is not None:
        try:
            msg = keyboard_midi.receive()
            while msg is not None:
                handle(msg)
                msg = keyboard_midi.receive()
        except usb.core.USBError:
            print("MIDI keyboard disconnected")
            keyboard_midi = None

    # Buttons: act on the moment of pressing, not while held, by comparing
    # with how the buttons were last time through the loop
    buttons = (fruit_jam.button1, fruit_jam.button2, fruit_jam.button3)
    if buttons[0] and not buttons_were[0]:
        waveform_index = (waveform_index + 1) % len(WAVEFORMS)
        print("Waveform:", WAVEFORMS[waveform_index][0])
        show_pixels()
    if buttons[1] and not buttons_were[1]:
        octave = max(octave - 1, -3)
        print("Octave:", octave)
    if buttons[2] and not buttons_were[2]:
        octave = min(octave + 1, 3)
        print("Octave:", octave)
    buttons_were = buttons
