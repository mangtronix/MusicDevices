# SPDX-FileCopyrightText: 2026 Michael Ang with Claude Opus 5.5 for Music Devices
#
# SPDX-License-Identifier: MIT

print("fruitjam_synth_demo")

# CircuitPython code.py — Adafruit Fruit Jam (port of synth_demo.py)
# Audio comes out of the Fruit Jam's headphone jack (or set AUDIO_OUTPUT to
# "speaker" for the included mini speaker, or "line" to feed a mixer, audio
# interface or amp from the headphone jack). Set USE_DVI = True to show an
# instrument panel on a monitor connected to the DVI (HDMI-shaped) port.
# Play it from the computer over USB-C, or plug a USB MIDI keyboard into one
# of the USB-A ports (best before powering on; use a data-capable cable).
# Set USE_USB_HOST_MIDI = False to ignore the USB-A ports.
# Five knobs shape the synth sound: filter cutoff and resonance, and the
# waveform's Wave, Timbre and Shape (set up for an Arturia MiniFreak, see
# the CC_ settings below).
# Libraries: adafruit_fruitjam, adafruit_display_text, adafruit_usb_host_midi
# (the last one only when USE_USB_HOST_MIDI is on)

import math
import time
import synthio
import ulab.numpy as np
import audiocore
import audiomixer
import usb_midi
import displayio
import supervisor
import vectorio
import terminalio
from adafruit_display_text import label
from adafruit_fruitjam.peripherals import Peripherals, request_display_config

# Audio tuning: keep the I2S stream at a common sample rate and cap note level.
SAMPLE_RATE = 22050
MIDI_MAX_AMPLITUDE = 0.65
STARTUP_AMPLITUDE = 0.45
TABLE_SIZE = 256
# "headphone", "speaker", or "line" (line level from the headphone jack; don't
# plug headphones in with "line", it can be very loud)
AUDIO_OUTPUT = "headphone"
# Mixer buffer in bytes (2 bytes per sample): 1536 is about 35 ms of sound.
# Reading the USB keyboard (and redrawing the screen, if USE_DVI is on) can
# pause our code; a smaller buffer runs dry then and the sound clicks (1024
# clicked now and then). A bigger buffer makes notes start later (2048 felt
# laggy). With USE_DVI = True you may need a bit more.
BUFFER_SIZE = 1536
VOLUME = 0.6  # headphone and speaker level, 0.0 - 0.75
# Line output level, 0.0 - 1.0 on the same scale as VOLUME (used only when
# AUDIO_OUTPUT = "line"). 0.73 is about 0 dB; lower it if the mixer or
# interface input clips. There's no 0.75 limit here because it isn't meant
# for ears or speakers.
LINE_VOLUME = 0.73
# Show the instrument panel on a DVI monitor. False turns the DVI output off,
# which frees memory and processor time for audio.
USE_DVI = False
# Read a MIDI keyboard plugged into the USB-A ports. Reading it can pause our
# code (see BUFFER_SIZE), so turn this off if you only play from the computer.
USE_USB_HOST_MIDI = True
# MIDI CC numbers of the knobs that shape the synth. These are the Arturia
# MiniFreak's Filter Cutoff, Resonance and Osc 1 Wave/Timbre/Shape knobs;
# change them to match your controller. PRINT_CC = True prints every CC that
# arrives, a quick way to find your controller's numbers.
CC_CUTOFF = 74
CC_RESONANCE = 71
CC_WAVE = 14
CC_TIMBRE = 15
CC_SHAPE = 16
PRINT_CC = False

# Draw a compact 240x135 instrument panel, centered on a 320x240 DVI screen.
# The bar graph is pitch-mapped and its level decays after every note-on.
# 8-bit color keeps the screen's memory small; the panel's flat colors don't
# need more. With DVI off, the panel is still built (so the code below works
# the same) but nothing draws it.
if USE_DVI:
    request_display_config(320, 240, color_depth=8)
    display = supervisor.runtime.display
    width, height = display.width, display.height
else:
    displayio.release_displays()  # turn the DVI output off
    width, height = 320, 240
root = displayio.Group()
if USE_DVI:
    display.root_group = root

BG = 0x101316
GRID = 0x293035
INK = 0xF1EBDD
LIME = 0xC6FF00
PINK = 0xFF5470
CYAN = 0x54E6D2

bg_bitmap = displayio.Bitmap(width, height, 1)
bg_palette = displayio.Palette(1)
bg_palette[0] = BG
root.append(displayio.TileGrid(bg_bitmap, pixel_shader=bg_palette))
# Everything below is laid out for 240x135 and placed in the middle.
screen = displayio.Group(x=(width - 240) // 2, y=(height - 135) // 2)
root.append(screen)

def add_text(text, x, y, color=INK):
    """Add a small fixed label to the display layout."""
    item = label.Label(terminalio.FONT, text=text, color=color, x=x, y=y)
    screen.append(item)
    return item

# Header and footer labels give the display a small hardware-instrument feel.
add_text("SYNTH / 01", 10, 12, LIME)
add_text("USB MIDI", 171, 12, CYAN)
add_text("NOTE", 10, 31, GRID)
shown_note = add_text("--", 10, 47, INK)
add_text("VEL", 82, 31, GRID)
shown_velocity = add_text("---", 82, 47, INK)
add_text("MONO / I2S", 158, 31, GRID)
add_text("TLV320DAC", 158, 47, INK)

# Draw a baseline, a few timing ticks, and eight muted meter wells.
grid_palette = displayio.Palette(1)
grid_palette[0] = GRID
screen.append(vectorio.Rectangle(pixel_shader=grid_palette, width=220, height=1, x=10, y=111))
for x in (10, 64, 118, 172, 229):
    screen.append(vectorio.Rectangle(pixel_shader=grid_palette, width=1, height=48, x=x, y=58))

bar_colors = (LIME, LIME, CYAN, CYAN, PINK, PINK, LIME, LIME)
bar_palettes = []
bar_shapes = []
bar_levels = [0.0] * 8
BAR_BASELINE = 106
BAR_MAX_HEIGHT = 42
BAR_X = (17, 44, 71, 98, 125, 152, 179, 206)
for x, color in zip(BAR_X, bar_colors):
    well = vectorio.Rectangle(pixel_shader=grid_palette, width=13, height=BAR_MAX_HEIGHT, x=x, y=BAR_BASELINE - BAR_MAX_HEIGHT)
    screen.append(well)
    palette = displayio.Palette(1)
    palette[0] = color
    bar_palettes.append(palette)  # Keep palettes alive for the display.
    bar = vectorio.Rectangle(pixel_shader=palette, width=13, height=1, x=x, y=BAR_BASELINE - 1)
    screen.append(bar)
    bar_shapes.append(bar)

add_text("LOW", 10, 126, GRID)
add_text("HIGH", 205, 126, GRID)

def note_name(note_number):
    """Format a MIDI note number as a compact pitch label."""
    names = ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B")
    return names[note_number % 12] + str((note_number // 12) - 1)

def flash_note(note_number, velocity):
    """Kick the pitch lane upward and update the note/velocity readouts."""
    lane = min(7, max(0, (note_number - 36) * 8 // 61))
    bar_levels[lane] = max(bar_levels[lane], velocity / 127.0)
    shown_note.text = note_name(note_number)
    shown_velocity.text = ("  " + str(velocity))[-3:]

last_animation_time = time.monotonic()
ANIMATION_INTERVAL = 1 / 30  # redraw at most 30 times a second

def animate_bars():
    """Ease every meter bar toward zero to create a trailing note animation."""
    global last_animation_time
    now = time.monotonic()
    elapsed = now - last_animation_time
    # Each redraw takes processor time away from the audio, so don't redraw
    # more often than the eye needs.
    if elapsed < ANIMATION_INTERVAL:
        return
    last_animation_time = now
    for index, level in enumerate(bar_levels):
        level = max(0.0, level - elapsed * 1.7)
        bar_levels[index] = level
        height = max(1, int(level * BAR_MAX_HEIGHT))
        # Only change bars that moved, so a still panel needs no redrawing.
        if bar_shapes[index].height != height:
            bar_shapes[index].height = height
            bar_shapes[index].y = BAR_BASELINE - height


# --- Synth sound, shaped by the knobs ---
# synthio repeats one cycle of a waveform (TABLE_SIZE samples) at each note's
# frequency. We build that cycle from three knob settings:
#   Wave   - the basic shape: sine, triangle, saw or square
#   Timbre - blends from a soft sine (0) to the full chosen wave (127)
#   Shape  - pushes the wave into a soft clipper: more = brighter and grittier
# ulab (CircuitPython's numpy) does the math on all samples at once, fast
# enough to rebuild the wave while a knob is turning.
WAVE_NAMES = ("sine", "triangle", "saw", "square")
phase = np.linspace(0, 1, TABLE_SIZE, endpoint=False)  # 0 to 1 across one cycle
BASE_WAVES = (
    np.sin(2 * math.pi * phase),  # sine
    1 - 4 * abs(phase - 0.5),  # triangle
    2 * phase - 1,  # saw
    np.array([1.0 if i < TABLE_SIZE // 2 else -1.0 for i in range(TABLE_SIZE)]),  # square
)
wave_index = 0  # start as a plain sine, like the original demo
timbre = 1.0
shape = 0.0


def build_waveform():
    """Make the synth's waveform from the Wave, Timbre and Shape settings."""
    wave = BASE_WAVES[0] * (1 - timbre) + BASE_WAVES[wave_index] * timbre
    if shape > 0:
        # Soft clipper: x / (1 + |x|) squashes peaks smoothly, and pushing the
        # wave in harder (more drive) squares it off and adds harmonics.
        # Dividing by the result at x = drive keeps the peaks at full height.
        drive = 1 + 9 * shape
        driven = drive * wave
        wave = driven / (1 + abs(driven)) / (drive / (1 + drive))
    # Centered and below full scale (16000 of 32767) to leave some headroom
    return np.array(wave * 16000, dtype=np.int16)


waveform = build_waveform()

# One low-pass filter shared by every note, so the Cutoff and Resonance knobs
# also change notes that are already playing.
CUTOFF_MIN = 100  # Hz
CUTOFF_MAX = 9000  # Hz, kept below half the sample rate (11025 Hz)
lowpass = synthio.Biquad(synthio.FilterMode.LOW_PASS, frequency=CUTOFF_MAX, Q=0.707)

# Route the mono synthesizer to the Fruit Jam's TLV320 DAC over I2S. The DAC's
# sample rate must match the mixer and the drum WAV files (22050 Hz).
# Line out uses the headphone jack, so start from the headphone setup.
fruit_jam = Peripherals(
    audio_output="speaker" if AUDIO_OUTPUT == "speaker" else "headphone",
    sample_rate=SAMPLE_RATE,
)
if AUDIO_OUTPUT == "line":
    # Peripherals sets the headphone path up quietly to protect your ears.
    # For a line input we want the jack's driver in line-out mode and its
    # analog stages neutral, with the level set by the DAC's digital volume.
    fruit_jam.dac.headphone_lineout = True
    fruit_jam.dac.headphone_left_gain = 0  # dB, no extra amp gain
    fruit_jam.dac.headphone_right_gain = 0
    fruit_jam.dac.headphone_volume = 0  # dB, analog volume fully open
    # Same mapping the Fruit Jam library uses for VOLUME: 0.0-1.0 -> -63 to +23 dB
    fruit_jam.dac.dac_volume = -63 + 86 * LINE_VOLUME
else:
    fruit_jam.volume = VOLUME

# Mix one continuous synth voice with six overlapping one-shot drum voices.
DRUM_VOICE_COUNT = 6
mixer = audiomixer.Mixer(
    voice_count=1 + DRUM_VOICE_COUNT,
    sample_rate=SAMPLE_RATE,
    channel_count=1,
    bits_per_sample=16,
    samples_signed=True,
    buffer_size=BUFFER_SIZE,
)
fruit_jam.audio.play(mixer)
synth = synthio.Synthesizer(sample_rate=SAMPLE_RATE, channel_count=1)
mixer.voice[0].play(synth, loop=True)

# The CC0 TR-808 one-shots are stored as small mono PCM WAVs beside this file.
# MIDI C3 through B3 selects a different drum; other notes stay on the synth.
# BD_CRUNCH.WAV is BD0000.WAV made louder with soft-clip saturation for more
# punch on headphones and the small speaker.
DRUM_NOTES = {
    48: "BD_CRUNCH.WAV",  # C3  kick
    49: "SD5050.WAV",  # C#3 snare
    50: "CP.WAV",      # D3  hand clap
    51: "CH.WAV",      # D#3 closed hi-hat
    52: "OH50.WAV",    # E3  open hi-hat
    53: "CY5000.WAV",  # F3  cymbal
    54: "BD_CRUNCH.WAV",  # F#3 kick
    55: "SD5050.WAV",  # G3  snare
    56: "CP.WAV",      # G#3 hand clap
    57: "CH.WAV",      # A3  closed hi-hat
    58: "OH50.WAV",    # A#3 open hi-hat
    59: "CY5000.WAV",  # B3  cymbal
}
_drums_dir = "samples/808/"
_drum_sources = [None] * DRUM_VOICE_COUNT
_next_drum_voice = 0

def trigger_drum(midi_note, velocity):
    """Start a one-shot on a rotating mixer voice so hits can overlap."""
    global _next_drum_voice
    filename = DRUM_NOTES.get(midi_note)
    if filename is None:
        return False

    slot = _next_drum_voice
    _next_drum_voice = (_next_drum_voice + 1) % DRUM_VOICE_COUNT
    source_file = open(_drums_dir + filename, "rb")
    sample = audiocore.WaveFile(source_file)
    voice = mixer.voice[slot + 1]
    voice.level = 0.85 * (velocity / 127.0)
    voice.play(sample)
    # Keep the WaveFile (and its open file) alive while the mixer reads it.
    _drum_sources[slot] = sample
    return True

# Shape note starts and stops to prevent clicks; the short attack keeps response
# snappy, while the release lets each note fade naturally after note-off.
envelope = synthio.Envelope(
    attack_time=0.003,
    decay_time=0.08,
    sustain_level=0.55,
    release_time=0.12,
)

# Startup sound check: play a short ascending/descending phrase once, before
# accepting live MIDI. Each step is 200 ms sounding plus a 50 ms gap.
for midi_note in (72, 76, 79, 76, 74, 77, 81, 84):
    frequency = 440.0 * (2 ** ((midi_note - 69) / 12.0))
    voice = synthio.Note(
        frequency=frequency,
        waveform=waveform,
        envelope=envelope,
        amplitude=STARTUP_AMPLITUDE,
    )
    synth.press(voice)
    flash_note(midi_note, 88)
    animate_bars()
    time.sleep(0.20)
    synth.release(voice)
    time.sleep(0.05)

# Live input comes from a computer acting as USB host and sending MIDI to the
# Fruit Jam over USB-C, and from a MIDI keyboard on the USB-A ports, where the
# Fruit Jam is the USB host.
midi_in = usb_midi.ports[0]
keyboard = None  # found later; the keyboard can be plugged in or unplugged
last_keyboard_scan = 0


if USE_USB_HOST_MIDI:
    import usb.core
    import adafruit_usb_host_midi


def find_keyboard():
    """Return the first USB device on the USB-A ports that sends MIDI."""
    for device in usb.core.find(find_all=True):
        try:
            # timeout: how long each read waits, in seconds. In CircuitPython
            # 10.x a message arriving just as a read times out can be lost, so
            # fewer timeouts = fewer lost notes; 20 ms keeps that rare.
            # See https://github.com/adafruit/circuitpython/issues/10554
            raw_midi = adafruit_usb_host_midi.MIDI(device, timeout=0.02)
        except (ValueError, usb.core.USBError):
            continue
        if raw_midi.in_ep == 0:
            continue  # not a MIDI device (e.g. a computer keyboard or mouse)
        print("Found MIDI keyboard:", hex(device.idVendor), hex(device.idProduct))
        return raw_midi
    return None


# Remember each held key and its synth voice so note-off can release that exact
# voice. Channel is part of the key, allowing the same pitch on different channels.
active_notes = {}
status = None
needed_data = 0
pending_data = []


def handle_note(status_byte, note_number, velocity):
    """Translate MIDI note-on/off events into synthio voices."""
    command = status_byte & 0xF0
    channel = status_byte & 0x0F
    key = (channel, note_number)

    if command == 0x90 and velocity > 0:  # Note On
        if trigger_drum(note_number, velocity):
            flash_note(note_number, velocity)
            return

        old_voice = active_notes.pop(key, None)
        if old_voice is not None:
            synth.release(old_voice)
        frequency = 440.0 * (2 ** ((note_number - 69) / 12.0))
        voice = synthio.Note(
            frequency=frequency,
            waveform=waveform,
            envelope=envelope,
            amplitude=MIDI_MAX_AMPLITUDE * (velocity / 127.0),
            filter=lowpass,
        )
        active_notes[key] = voice
        synth.press(voice)
        flash_note(note_number, velocity)
    elif command == 0x80 or (command == 0x90 and velocity == 0):
        # Drums are one-shots: note-off does not cut their sample short.
        voice = active_notes.pop(key, None)
        if voice is not None:
            synth.release(voice)
        if not active_notes:
            shown_note.text = "--"
            shown_velocity.text = "---"


def handle_cc(control, value):
    """Turn knob movements (MIDI CC messages) into changes in the synth sound."""
    global wave_index, timbre, shape, waveform
    if PRINT_CC:
        print("CC", control, value)

    if control == CC_CUTOFF:
        # 0-127 -> 100 Hz to 9 kHz. Exponential, so each part of the knob's
        # turn changes the sound by a similar amount.
        lowpass.frequency = CUTOFF_MIN * (CUTOFF_MAX / CUTOFF_MIN) ** (value / 127)
    elif control == CC_RESONANCE:
        # 0-127 -> Q 0.7 (no peak) to 6 (a strong, whistling peak at the cutoff)
        lowpass.Q = 0.707 + value / 127 * 5.3
    elif control in (CC_WAVE, CC_TIMBRE, CC_SHAPE):
        if control == CC_WAVE:
            new_index = value * len(BASE_WAVES) // 128  # four zones on the knob
            if new_index != wave_index:
                print("Wave:", WAVE_NAMES[new_index])
            wave_index = new_index
        elif control == CC_TIMBRE:
            timbre = value / 127
        else:
            shape = value / 127
        waveform = build_waveform()
        # Swap the new waveform into notes that are already sounding.
        for voice in active_notes.values():
            voice.waveform = waveform


def parse_midi_byte(value):
    """Assemble raw MIDI bytes into messages, including running status."""
    global status, needed_data, pending_data

    # MIDI real-time bytes can occur between any other bytes.
    if value >= 0xF8:
        return

    if value & 0x80:
        if 0x80 <= value <= 0xEF:  # Channel voice message
            status = value
            command = value & 0xF0
            needed_data = 1 if command in (0xC0, 0xD0) else 2
            pending_data = []
        else:  # Ignore system common and SysEx messages in this demo.
            status = None
            pending_data = []
        return

    if status is None:
        return

    pending_data.append(value)
    if len(pending_data) == needed_data:
        if (status & 0xF0) in (0x80, 0x90):
            handle_note(status, pending_data[0], pending_data[1])
        elif (status & 0xF0) == 0xB0:  # Control Change (a knob or slider)
            handle_cc(pending_data[0], pending_data[1])
        # Keep channel status for standard MIDI running-status messages.
        pending_data = []


# Stay responsive by checking both MIDI inputs continuously and feeding each
# arriving byte straight to the MIDI parser.
while True:
    # Read everything waiting from the computer, one byte at a time, so its
    # messages are finished before any keyboard bytes reach the parser.
    data = midi_in.read(1)
    while data:
        for byte in data:
            parse_midi_byte(byte)
        data = midi_in.read(1)

    if USE_USB_HOST_MIDI:
        # Look for a USB keyboard every 2 seconds until one is found.
        if keyboard is None and time.monotonic() - last_keyboard_scan > 2:
            last_keyboard_scan = time.monotonic()
            keyboard = find_keyboard()

        # The keyboard sends whole messages. If it is unplugged, reading fails:
        # forget it and look again.
        if keyboard is not None:
            try:
                data = keyboard.read(64)
                if data:
                    for byte in data:
                        parse_midi_byte(byte)
            except usb.core.USBError:
                print("MIDI keyboard disconnected")
                keyboard = None

    animate_bars()
