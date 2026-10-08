# SPDX-FileCopyrightText: 2026 Michael Ang with Claude Opus 5.5 for Music Devices
#
# SPDX-License-Identifier: MIT

print("fruitjam_looper")

# CircuitPython code.py — Adafruit Fruit Jam two-track MIDI looper
# Same synth and 808 drums as fruitjam_synth_demo.py, plus a looper that
# records what you play and plays it back in a loop:
#   - Notes C3-B3 (the drums) go on the DRUMS track, all other notes go on the
#     SYNTH track, so you can play both while recording.
#   - Tap button 1 to arm; recording starts on the first note you play, so
#     that note is the start of the loop. Tap again to end the loop: it starts
#     playing right away from that first note. Overdub adds to the loop.
#   - The looper records notes, not sound, so the knobs (filter, Wave,
#     Timbre, Shape) still change looped synth notes as they play.
#   - Optional quantize (QUANTIZE): when you end the first recording, the
#     looper guesses the tempo from the loop length and gently pulls looped
#     notes toward a 1/32-note grid. Your original timing is kept, so
#     QUANTIZE = False plays the loop exactly as you played it.
#
# Button 1 (the looper):
#   empty:      press to arm; recording then starts on your first note
#   recording:  press to end the loop; it plays straight away from the top
#   playing:    tap to start/stop overdubbing; hold 1 second to stop
#   stopped:    press to start again from the top
#   The moments that set the loop's timing (ending the first recording,
#   starting) happen the instant you press, so you can press on the "1".
# Buttons 2 and 3:      tap                          hold (1 second)
#   Button 2   mute / unmute drums                  clear drums
#   Button 3   mute / unmute synth                  clear synth
#   Clearing both tracks empties the looper, ready to record again.
#   Buttons 2 + 3 together: save a "gruv" (see below)
#
# Serial commands: type these in the serial console (then Enter) to work the
# looper without touching the board: tap 1, tap 2, tap 3, hold 1, hold 2,
# hold 3, save (= buttons 2 + 3), state.
#
# Gruv capture: the board always remembers what you've been hearing (live
# playing and loop playback). Had a nice moment? Press buttons 2 and 3
# together to save it as a MIDI file, /saves/gruv_001.mid, gruv_002.mid ...
# It shows up on the CPSAVES drive, ready to drag into Ableton. The file
# starts at the first note after your last pause of 3+ seconds (at most the
# last 2 minutes), with drums and synth on separate tracks. All five
# NeoPixels flash white when it's saved. Notes keep the lengths you played
# (drums too, though their sounds are one-shots).
#
# NeoPixels (left to right):
#   0  looper: off = empty, blinking red = armed (waiting for the first note),
#      red = recording (first take or overdub), green = playing,
#      slowly blinking green = stopped (tap button 1 to start)
#   1  drums track: lit when it has notes (dim when muted), flashes on hits,
#      blinks white for half a second when cleared
#   2  synth track: same
#   3  first half of the loop, with a bright flash at the start of each pass
#   4  second half of the loop
#
# Audio comes out of the headphone jack (or set AUDIO_OUTPUT). Play from the
# computer over USB-C, or plug a USB MIDI keyboard into a USB-A port.
# Libraries: adafruit_fruitjam, adafruit_usb_host_midi (only when
# USE_USB_HOST_MIDI is on)

import array
import math
import os
import sys
import time
import supervisor
import synthio
import ulab.numpy as np
import audiocore
import audiomixer
import usb_midi
from adafruit_fruitjam.peripherals import Peripherals

# --- Settings ---
SAMPLE_RATE = 22050
MIDI_MAX_AMPLITUDE = 0.65
STARTUP_AMPLITUDE = 0.45
TABLE_SIZE = 256
# "headphone", "speaker", or "line" (line level from the headphone jack; don't
# plug headphones in with "line", it can be very loud)
AUDIO_OUTPUT = "headphone"
# Mixer buffer in bytes (2 bytes per sample): 1536 is about 35 ms of sound.
# Reading the USB keyboard can pause our code; a smaller buffer runs dry then
# and the sound clicks. A bigger buffer makes notes start later.
BUFFER_SIZE = 1536
VOLUME = 0.6  # headphone and speaker level, 0.0 - 0.75
# Line output level, 0.0 - 1.0 on the same scale as VOLUME (used only when
# AUDIO_OUTPUT = "line"). 0.73 is about 0 dB.
LINE_VOLUME = 0.73
# Read a MIDI keyboard plugged into the USB-A ports. Reading it can pause our
# code (see BUFFER_SIZE), which also makes loop playback timing less exact.
USE_USB_HOST_MIDI = True
# MIDI CC numbers of the knobs that shape the synth (Arturia MiniFreak's
# Filter Cutoff, Resonance and Osc 1 Wave/Timbre/Shape). PRINT_CC = True
# prints every CC that arrives, to find your controller's numbers.
CC_CUTOFF = 74
CC_RESONANCE = 71
CC_WAVE = 14
CC_TIMBRE = 15
CC_SHAPE = 16
PRINT_CC = False
HOLD_TIME = 1.0  # seconds to hold a button for its "hold" action
# Gruv capture: a pause at least this long marks the start of what gets saved,
# and a save never goes back further than CAPTURE_MAX_S.
CAPTURE_GAP_S = 3
CAPTURE_MAX_S = 120
# Quantize: pull looped notes toward a rhythmic grid. The grid comes from the
# loop length: the looper picks the number of beats (1, 2, 4, 8 ...) whose
# tempo lands closest to the middle of TEMPO_MIN-TEMPO_MAX. Live looping tends
# to sit a bit slower and more laid back than 120 BPM.
QUANTIZE = True
QUANTIZE_STEPS_PER_BEAT = 8  # 8 = 1/32 notes, 4 = 1/16 notes
QUANTIZE_STRENGTH = 0.8  # 0 = as played, 1 = exactly on the grid
TEMPO_MIN = 60  # BPM
TEMPO_MAX = 100
PIXEL_BRIGHTNESS = 0.15
SERIAL_COMMANDS = True  # accept "tap 1", "save" etc. from the serial console

# --- Synth sound, shaped by the knobs ---
# synthio repeats one cycle of a waveform (TABLE_SIZE samples) at each note's
# frequency. We build that cycle from three knob settings:
#   Wave   - the basic shape: sine, triangle, saw or square
#   Timbre - blends from a soft sine (0) to the full chosen wave (127)
#   Shape  - pushes the wave into a soft clipper: more = brighter and grittier
WAVE_NAMES = ("sine", "triangle", "saw", "square")
phase = np.linspace(0, 1, TABLE_SIZE, endpoint=False)  # 0 to 1 across one cycle
BASE_WAVES = (
    np.sin(2 * math.pi * phase),  # sine
    1 - 4 * abs(phase - 0.5),  # triangle
    2 * phase - 1,  # saw
    np.array([1.0 if i < TABLE_SIZE // 2 else -1.0 for i in range(TABLE_SIZE)]),  # square
)
wave_index = 0
timbre = 1.0
shape = 0.0


def build_waveform():
    """Make the synth's waveform from the Wave, Timbre and Shape settings."""
    wave = BASE_WAVES[0] * (1 - timbre) + BASE_WAVES[wave_index] * timbre
    if shape > 0:
        # Soft clipper: x / (1 + |x|) squashes peaks smoothly; more drive
        # squares the wave off and adds harmonics.
        drive = 1 + 9 * shape
        driven = drive * wave
        wave = driven / (1 + abs(driven)) / (drive / (1 + drive))
    return np.array(wave * 16000, dtype=np.int16)


waveform = build_waveform()

# One low-pass filter shared by every note, so the Cutoff and Resonance knobs
# also change notes that are already playing (live or looped).
CUTOFF_MIN = 100  # Hz
CUTOFF_MAX = 9000  # Hz, kept below half the sample rate (11025 Hz)
lowpass = synthio.Biquad(synthio.FilterMode.LOW_PASS, frequency=CUTOFF_MAX, Q=0.707)

# --- Audio output ---
fruit_jam = Peripherals(
    audio_output="speaker" if AUDIO_OUTPUT == "speaker" else "headphone",
    sample_rate=SAMPLE_RATE,
)
if AUDIO_OUTPUT == "line":
    # Line-out mode with neutral analog stages; LINE_VOLUME sets the level.
    fruit_jam.dac.headphone_lineout = True
    fruit_jam.dac.headphone_left_gain = 0
    fruit_jam.dac.headphone_right_gain = 0
    fruit_jam.dac.headphone_volume = 0
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

# --- Drums: 808 one-shots on C3-B3 ---
DRUM_NOTES = {
    48: "BD_CRUNCH.WAV",  # C3  kick
    49: "SD5050.WAV",  # C#3 snare
    50: "CP.WAV",  # D3  hand clap
    51: "CH.WAV",  # D#3 closed hi-hat
    52: "OH50.WAV",  # E3  open hi-hat
    53: "CY5000.WAV",  # F3  cymbal
    54: "BD_CRUNCH.WAV",  # F#3 kick
    55: "SD5050.WAV",  # G3  snare
    56: "CP.WAV",  # G#3 hand clap
    57: "CH.WAV",  # A3  closed hi-hat
    58: "OH50.WAV",  # A#3 open hi-hat
    59: "CY5000.WAV",  # B3  cymbal
}
DRUMS_DIR = "samples/808/"
next_drum_voice = 0


def load_sample(filename):
    """Read a 16-bit mono WAV file into memory as a playable sample."""
    with open(DRUMS_DIR + filename, "rb") as file:
        data = file.read()
    start = data.find(b"data")  # the sound itself follows the "data" marker
    size = int.from_bytes(data[start + 4 : start + 8], "little")
    sound = array.array("h", data[start + 8 : start + 8 + size])
    return audiocore.RawSample(sound, sample_rate=SAMPLE_RATE, channel_count=1)


# Load every drum sound into memory once (they're small: about 80 KB in all).
# Playing from memory means no file reading while music is playing, which
# could otherwise interrupt the audio and crackle.
drum_samples = {}
for filename in DRUM_NOTES.values():
    if filename not in drum_samples:
        drum_samples[filename] = load_sample(filename)


def trigger_drum(midi_note, velocity):
    """Start a one-shot on a rotating mixer voice so hits can overlap."""
    global next_drum_voice
    filename = DRUM_NOTES.get(midi_note)
    if filename is None:
        return False
    voice = mixer.voice[next_drum_voice + 1]
    next_drum_voice = (next_drum_voice + 1) % DRUM_VOICE_COUNT
    voice.level = 0.85 * (velocity / 127.0)
    voice.play(drum_samples[filename])
    return True


envelope = synthio.Envelope(
    attack_time=0.003,
    decay_time=0.08,
    sustain_level=0.55,
    release_time=0.12,
)

# --- Looper state ---
# Each track is a list of recorded events, oldest first:
#   [time_ms, status, note, velocity, pass_recorded, play_ms]
# time_ms is when you played it, measured from the start of the loop.
# play_ms is when it plays back: the same as time_ms, or moved toward the
# grid when QUANTIZE is on. pass_recorded stops a note recorded during
# overdub from playing again straight away in the same pass; -1 means
# "play on every pass".
EMPTY, ARMED, RECORDING = "empty", "armed", "recording"
PLAYING, OVERDUB, STOPPED = "playing", "overdub", "stopped"
looper_state = EMPTY
loop_start_ms = 0  # when the loop's first pass started
loop_length_ms = 0  # set when the first recording ends
loop_beats = 4  # guessed from the loop length, for quantize
tracks = {"drums": [], "synth": []}
muted = {"drums": False, "synth": False}
flash = {"drums": 0.0, "synth": 0.0}  # NeoPixel flash level, fades out
cleared_until = {"drums": 0, "synth": 0, "looper": 0}  # blink white until then
# Synth notes recorded as pressed, waiting for their note-off to be recorded.
open_notes = set()


def now_ms():
    return time.monotonic_ns() // 1_000_000


def track_for(note_number):
    return "drums" if note_number in DRUM_NOTES else "synth"


def record_event(status_byte, note_number, velocity, is_note_off):
    """Add a live note event to its track at the current loop position."""
    elapsed = now_ms() - loop_start_ms
    if looper_state == RECORDING:
        position, pass_number = elapsed, 0
    else:
        position, pass_number = elapsed % loop_length_ms, elapsed // loop_length_ms
    if is_note_off:
        pass_number = -1  # always play note-offs, so notes never get stuck
    event = [position, status_byte, note_number, velocity, pass_number, position]
    if looper_state != RECORDING:
        # The loop is already playing, so work out this one note's playback
        # time now. (The first take is all done at once when it ends.)
        event[5] = quantized_time(event, held_shifts)
    tracks[track_for(note_number)].append(event)
    if looper_state != RECORDING:
        rebuild_schedules()


# How far each held note's note-on was moved by quantize, so its note-off can
# be moved the same amount: {(channel, note): shift_ms}
held_shifts = {}


def quantized_time(event, shifts):
    """Return when this event should play back (moved toward the grid)."""
    time_ms, status_byte, note_number, velocity = event[0], event[1], event[2], event[3]
    key = (status_byte & 0x0F, note_number)
    if not QUANTIZE:
        shift = 0
    elif (status_byte & 0xF0) == 0x90 and velocity > 0:
        step = loop_length_ms / (loop_beats * QUANTIZE_STEPS_PER_BEAT)
        nearest = round(time_ms / step) * step  # closest grid step
        shift = QUANTIZE_STRENGTH * (nearest - time_ms)
        shifts[key] = shift
    else:
        # Move a note-off as far as its note-on moved, so the note keeps the
        # length you played.
        shift = shifts.pop(key, 0)
    return int(time_ms + shift) % loop_length_ms


def guess_beats(length_ms):
    """Pick the beat count (1, 2, 4, 8 ...) with the most likely tempo."""
    # The middle of the tempo range, on a musical (multiplying) scale
    target = math.sqrt(TEMPO_MIN * TEMPO_MAX)
    best_beats, best_error = 1, None
    beats = 1
    while beats <= 64:
        tempo = 60000 * beats / length_ms
        error = abs(math.log(tempo / target))  # how far off, up or down
        if best_error is None or error < best_error:
            best_beats, best_error = beats, error
        beats *= 2
    return best_beats


def update_play_times():
    """Work out when every recorded note plays back (when the loop is made)."""
    held_shifts.clear()
    for events in tracks.values():
        for event in events:  # oldest first, so each note-off follows its note-on
            event[5] = quantized_time(event, held_shifts)
    rebuild_schedules()


# For playback, each track's events are also kept sorted by when they play,
# with a pointer to the next one due. Each check then only looks at the next
# event, instead of every note in the loop.
schedules = {"drums": [], "synth": []}
next_event = {"drums": 0, "synth": 0}


def play_time(event):
    return event[5]


def rebuild_schedules():
    """Re-sort the playback order after notes are added or cleared."""
    for track in schedules:
        schedule = sorted(tracks[track], key=play_time)
        schedules[track] = schedule
        # Point at the first event that hasn't played yet in this pass.
        index = 0
        while index < len(schedule) and schedule[index][5] <= last_position:
            index += 1
        next_event[track] = index


# --- Gruv capture ---
# Everything you hear goes into this list as (time_ms, status, data1, data2).
# When it gets long, the oldest quarter is dropped.
capture = []
CAPTURE_MAX_EVENTS = 20000
saved_flash_until = 0  # NeoPixels flash white until this time after a save


def capture_event(status_byte, data1, data2):
    capture.append((now_ms(), status_byte, data1, data2))
    if len(capture) > CAPTURE_MAX_EVENTS:
        del capture[: CAPTURE_MAX_EVENTS // 4]


def variable_length(number):
    """Encode a number the way MIDI files store times: 7 bits per byte."""
    groups = [number & 0x7F]  # lowest 7 bits last, with no "more" flag
    number >>= 7
    while number:
        groups.append((number & 0x7F) | 0x80)  # 0x80 = "more bytes follow"
        number >>= 7
    return bytes(reversed(groups))


def midi_track(name, events):
    """Build one MIDI file track from (time_ms, message_bytes) events."""
    data = bytearray(b"\x00\xff\x03") + variable_length(len(name)) + name.encode()
    last_time = 0
    for time_ms, message in events:
        data += variable_length(time_ms - last_time) + message
        last_time = time_ms
    data += b"\x00\xff\x2f\x00"  # end of track
    return b"MTrk" + len(data).to_bytes(4, "big") + data


def event_time(event):
    return event[0]


def save_gruv():
    """Save the last stretch of playing as a two-track MIDI file in /saves."""
    global saved_flash_until
    now = now_ms()
    events = [e for e in capture if e[0] >= now - CAPTURE_MAX_S * 1000]
    if not events:
        print("Nothing to save yet")
        return
    # Start at the first event after the last pause of CAPTURE_GAP_S or more.
    start = 0
    for i in range(1, len(events)):
        if events[i][0] - events[i - 1][0] >= CAPTURE_GAP_S * 1000:
            start = i
    events = events[start:]
    first_time = events[0][0]

    # The file's tempo makes 1 MIDI tick = 1 ms (500 ticks per beat at
    # 120 BPM), so our millisecond times go straight into the file.
    drum_events = []
    synth_events = []
    drums_down = {}  # drum notes whose note-off hasn't come yet: {note: channel}
    for time_ms, status_byte, data1, data2 in events:
        time_ms -= first_time
        command = status_byte & 0xF0
        if command in (0x80, 0x90) and data1 in DRUM_NOTES:
            if command == 0x90 and data2 > 0:
                if data1 in drums_down:
                    # Hit again before its note-off: end the earlier hit here.
                    channel = drums_down.pop(data1)
                    drum_events.append((time_ms, bytes((0x80 | channel, data1, 0))))
                drums_down[data1] = status_byte & 0x0F
            elif data1 in drums_down:
                drums_down.pop(data1)
            else:
                continue  # a note-off whose hit was before the saved stretch
            drum_events.append((time_ms, bytes((status_byte, data1, data2))))
        else:
            synth_events.append((time_ms, bytes((status_byte, data1, data2))))
    # Any drum hit still without a note-off gets a short one.
    end_time = events[-1][0] - first_time
    for note_number, channel in drums_down.items():
        drum_events.append((end_time + 50, bytes((0x80 | channel, note_number, 0))))
    drum_events.sort(key=event_time)

    tempo = b"\xff\x51\x03" + (500000).to_bytes(3, "big")  # 120 BPM (500000 us per beat)
    header = b"MThd" + (6).to_bytes(4, "big") + (1).to_bytes(2, "big")
    header += (3).to_bytes(2, "big") + (500).to_bytes(2, "big")  # 3 tracks, 500 ticks/beat
    number = 1
    for name in os.listdir("/saves"):
        if name.startswith("gruv_") and name.endswith(".mid"):
            number = max(number, int(name[5:-4]) + 1)
    filename = "/saves/gruv_%03d.mid" % number
    # Build the whole file first, then write it in one go.
    data = header + midi_track("Tempo", [(0, tempo)])
    data += midi_track("Drums", drum_events) + midi_track("Synth", synth_events)
    try:
        with open(filename, "wb") as file:
            file.write(data)
    except OSError as error:
        print("Couldn't save gruv:", error)
        return
    seconds = (events[-1][0] - first_time) / 1000
    print("Saved", filename, "(%d events, %.1f s)" % (len(events), seconds))
    saved_flash_until = time.monotonic() + 0.5


# --- Playing notes (live and looped) ---
# Each sounding synth note is remembered under (source, channel, note), where
# source is "live" or "loop", so a looped note and the same note played live
# don't cut each other off.
active_notes = {}


# Reuse synth Note objects instead of making a new one for every note played.
# A looped note sounds the same every pass, so it can use the same Note each
# time. {(source, channel, note, velocity): synthio.Note}
note_cache = {}


def get_note(source, channel, note_number, velocity):
    """Return a ready-to-press synth Note, made once and then reused."""
    key = (source, channel, note_number, velocity)
    note = note_cache.get(key)
    if note is None:
        note = synthio.Note(
            frequency=synthio.midi_to_hz(note_number),
            waveform=waveform,
            envelope=envelope,
            amplitude=MIDI_MAX_AMPLITUDE * (velocity / 127.0),
            filter=lowpass,
        )
        note_cache[key] = note
    else:
        note.waveform = waveform  # the Wave/Timbre/Shape knobs may have moved
    return note


def handle_note(status_byte, note_number, velocity, source="live"):
    """Play a note-on/off as a drum hit or synth voice, and record it."""
    global looper_state, loop_start_ms
    command = status_byte & 0xF0
    channel = status_byte & 0x0F
    key = (source, channel, note_number)
    is_note_on = command == 0x90 and velocity > 0
    capture_event(status_byte, note_number, velocity)  # for gruv saves

    # When armed, the first note played starts the recording: the loop
    # begins exactly on that note.
    if looper_state == ARMED and source == "live" and is_note_on:
        loop_start_ms = now_ms()
        looper_state = RECORDING
        print("Looper:", looper_state)
    recording = source == "live" and looper_state in (RECORDING, OVERDUB)

    if is_note_on:
        if trigger_drum(note_number, velocity):
            flash["drums"] = 1.0
            if recording:
                record_event(status_byte, note_number, velocity, False)
                # Drums are one-shots, but recording the key release too
                # keeps how long you held it for saved gruv files.
                open_notes.add((channel, note_number))
            return
        old_voice = active_notes.pop(key, None)
        if old_voice is not None:
            synth.release(old_voice)
        voice = get_note(source, channel, note_number, velocity)
        active_notes[key] = voice
        synth.press(voice)
        flash["synth"] = 1.0
        if recording:
            record_event(status_byte, note_number, velocity, False)
            open_notes.add((channel, note_number))
    elif command == 0x80 or (command == 0x90 and velocity == 0):  # Note Off
        voice = active_notes.pop(key, None)
        if voice is not None:
            synth.release(voice)
        # Record the note-off of any recorded note, even after recording has
        # stopped, so a note held past the end of the loop still gets released.
        if source == "live" and (channel, note_number) in open_notes:
            open_notes.discard((channel, note_number))
            record_event(status_byte, note_number, velocity, True)


def release_loop_notes():
    """Stop every synth note the looper is currently playing."""
    for key in list(active_notes):
        if key[0] == "loop":
            synth.release(active_notes.pop(key))


# --- Looper controls ---
def tap_record():
    """Button 1 tap: arm -> (first note) record -> play -> overdub -> play ..."""
    global looper_state, loop_start_ms, loop_length_ms, loop_beats, last_position, last_pass
    if looper_state == EMPTY:
        tracks["drums"].clear()
        tracks["synth"].clear()
        open_notes.clear()
        looper_state = ARMED  # recording starts with the first note
    elif looper_state == ARMED:
        looper_state = EMPTY  # no note played yet: cancel
    elif looper_state == RECORDING:
        loop_length_ms = now_ms() - loop_start_ms
        if loop_length_ms < 200:  # too short to be a loop: start again
            looper_state = EMPTY
        else:
            looper_state = PLAYING
            # Playback starts right now at the beginning of the second pass,
            # so the first note plays immediately.
            last_pass = 1
            last_position = -1
            print("Loop length: %.2f s" % (loop_length_ms / 1000))
            loop_beats = guess_beats(loop_length_ms)
            print("Tempo guess: %d BPM (%d beats)" % (60000 * loop_beats / loop_length_ms, loop_beats))
            update_play_times()  # also sorts the playback order
    elif looper_state == STOPPED:
        # Start from the top of the loop, right now. Pass numbers carry on
        # from before (rather than starting over at 0), so notes overdubbed
        # in an earlier pass aren't mistaken for brand-new ones and skipped.
        last_pass += 1
        loop_start_ms = now_ms() - last_pass * loop_length_ms
        last_position = -1
        rebuild_schedules()  # back to the first event
        looper_state = PLAYING
    elif looper_state == PLAYING:
        looper_state = OVERDUB
    else:  # OVERDUB
        looper_state = PLAYING
    print("Looper:", looper_state)
    update_playback()  # start playing straight away, not on the next pass


def stop_loop():
    """Button 1 hold while playing: stop, but keep the loop."""
    global looper_state
    release_loop_notes()
    looper_state = STOPPED
    print("Looper:", looper_state)


def clear_all():
    """Clear everything and go back to empty."""
    global looper_state, loop_length_ms
    release_loop_notes()
    tracks["drums"].clear()
    tracks["synth"].clear()
    open_notes.clear()
    muted["drums"] = muted["synth"] = False
    looper_state = EMPTY
    loop_length_ms = 0
    rebuild_schedules()
    cleared_until["looper"] = time.monotonic() + 0.5
    print("Looper: cleared")


def toggle_mute(track):
    muted[track] = not muted[track]
    if track == "synth" and muted[track]:
        release_loop_notes()
    print(track, "muted" if muted[track] else "unmuted")


def clear_track(track):
    tracks[track].clear()
    rebuild_schedules()
    if track == "synth":
        release_loop_notes()
    print(track, "cleared")
    cleared_until[track] = time.monotonic() + 0.5
    # Both tracks empty: nothing left to loop, so start over (but not while
    # arming or recording the first take).
    if not tracks["drums"] and not tracks["synth"]:
        if looper_state not in (EMPTY, ARMED, RECORDING):
            clear_all()


# --- Loop playback ---
last_position = 0  # loop position (ms) at the last playback check
last_pass = 0  # pass number at the last playback check


def play_events(end, pass_number):
    """Play each track's events that are due (play time up to end)."""
    for track in schedules:
        schedule = schedules[track]
        index = next_event[track]
        while index < len(schedule) and schedule[index][5] <= end:
            _, status_byte, note_number, velocity, pass_recorded, _ = schedule[index]
            index += 1
            if pass_recorded == pass_number:
                continue  # just recorded in this pass: it was heard live
            is_note_on = (status_byte & 0xF0) == 0x90 and velocity > 0
            if is_note_on and muted[track]:
                continue  # note-offs still play, so nothing gets stuck
            handle_note(status_byte, note_number, velocity, source="loop")
        next_event[track] = index


def update_playback():
    """Play every recorded event between the last check and now."""
    global last_position, last_pass
    if looper_state not in (PLAYING, OVERDUB):
        return
    elapsed = now_ms() - loop_start_ms
    position = elapsed % loop_length_ms
    pass_number = elapsed // loop_length_ms
    if pass_number == last_pass:
        play_events(position, pass_number)
    else:
        # The loop wrapped around: finish the old pass, then start the new one
        # from the first event.
        play_events(loop_length_ms, last_pass)
        next_event["drums"] = next_event["synth"] = 0
        play_events(position, pass_number)
    last_position = position
    last_pass = pass_number


# --- NeoPixels ---
pixels = fruit_jam.neopixels
pixels.brightness = PIXEL_BRIGHTNESS
pixels.auto_write = False
STATE_COLORS = {
    EMPTY: 0x000000,
    ARMED: 0xFF0000,  # blinks
    RECORDING: 0xFF0000,
    OVERDUB: 0xFF0000,  # red like recording; pixels 3-4 show the loop moving
    PLAYING: 0x00FF00,
    STOPPED: 0x00FF00,  # blinks slowly
}
TRACK_COLORS = {"drums": (0, 80, 255), "synth": (200, 0, 255)}
last_pixel_update = 0


def scale(color, level):
    return tuple(int(c * level) for c in color)


def update_pixels():
    """Show looper state, tracks and loop position, 30 times a second."""
    global last_pixel_update
    now = time.monotonic()
    if now - last_pixel_update < 1 / 30:
        return
    fade = (now - last_pixel_update) * 4  # flashes fade out in about 1/4 s
    last_pixel_update = now

    pixels[0] = STATE_COLORS[looper_state]
    if looper_state == ARMED and int(now * 4) % 2:
        pixels[0] = 0  # blink while waiting for the first note
    if looper_state == STOPPED and int(now * 2) % 2:
        pixels[0] = 0  # slow blink: a loop is waiting to be started
    for index, track in ((1, "drums"), (2, "synth")):
        flash[track] = max(0.0, flash[track] - fade)
        level = 0.0
        if tracks[track]:
            level = 0.08 if muted[track] else 0.3
        pixels[index] = scale(TRACK_COLORS[track], max(level, flash[track]))
        if now < cleared_until[track]:  # just cleared: quick white blink
            pixels[index] = (255, 255, 255) if int(now * 12) % 2 else 0
    if now < cleared_until["looper"]:
        pixels[0] = (255, 255, 255) if int(now * 12) % 2 else 0

    if now < saved_flash_until:  # just saved a gruv: all white
        pixels.fill((255, 255, 255))
        pixels.show()
        return

    pixels[3] = pixels[4] = 0
    if looper_state in (PLAYING, OVERDUB):
        position = (now_ms() - loop_start_ms) % loop_length_ms
        if position < loop_length_ms // 2:
            # Bright for the first 100 ms of each pass, then dim
            pixels[3] = (255, 255, 255) if position < 100 else (40, 40, 40)
        else:
            pixels[4] = (40, 40, 40)
    pixels.show()


# --- Buttons: tap and hold ---
button_down_at = [None, None, None]  # when each button was pressed
state_at_press = EMPTY  # looper state just before button 1 was pressed
hold_done = [False, False, False]  # hold action already ran for this press
combo_done = False  # buttons 2 + 3 already saved for this press


def tap_button(i):
    if i == 0:
        tap_record()
    elif i == 1:
        toggle_mute("drums")
    else:
        toggle_mute("synth")


def hold_button(i, state_before=None):
    if i == 0:
        # Holding button 1 only does something while playing: stop.
        if state_before is None:
            state_before = looper_state
        if state_before in (PLAYING, OVERDUB):
            stop_loop()
    elif i == 1:
        clear_track("drums")
    else:
        clear_track("synth")


def update_buttons():
    """Run each button's tap and hold actions.

    Button 1 acts the moment it's pressed when that sets the loop's timing
    (arming, ending the first recording, starting). While playing it acts on
    release instead, so holding it to stop doesn't toggle overdub first.
    Buttons 2 and 3 act on release, so holding them to clear a track doesn't
    toggle mute first.
    """
    global combo_done, state_at_press
    pressed = (fruit_jam.button1, fruit_jam.button2, fruit_jam.button3)
    now = time.monotonic()
    for i in range(3):
        if pressed[i] and button_down_at[i] is None:  # just pressed
            button_down_at[i] = now
            hold_done[i] = False
            if i == 0:
                state_at_press = looper_state
                if state_at_press not in (PLAYING, OVERDUB):
                    tap_button(0)  # timing matters: act right now
        elif pressed[i] and not hold_done[i] and now - button_down_at[i] >= HOLD_TIME:
            hold_button(i, state_at_press if i == 0 else None)
            hold_done[i] = True
        elif not pressed[i] and button_down_at[i] is not None:  # just released
            playing_tap = i == 0 and state_at_press in (PLAYING, OVERDUB)
            if (i != 0 or playing_tap) and not hold_done[i]:
                tap_button(i)
            button_down_at[i] = None

    # Buttons 2 and 3 together save a gruv. Mark both as done so letting go
    # doesn't also mute, and holding doesn't also clear.
    if pressed[1] and pressed[2] and not combo_done:
        save_gruv()
        combo_done = True
        hold_done[1] = hold_done[2] = True
    elif not pressed[1] and not pressed[2]:
        combo_done = False


# --- Serial commands ---
serial_line = ""


def run_command(command):
    """Act on one serial command, as if a button was used."""
    words = command.split()
    if len(words) == 2 and words[0] in ("tap", "hold") and words[1] in ("1", "2", "3"):
        button = int(words[1]) - 1
        if words[0] == "tap":
            tap_button(button)
        else:
            hold_button(button)
    elif command == "save":
        save_gruv()
    elif command == "state":
        print("Looper:", looper_state, "| loop %d ms" % loop_length_ms,
              "| drums", len(tracks["drums"]), "events, muted" if muted["drums"] else "events",
              "| synth", len(tracks["synth"]), "events, muted" if muted["synth"] else "events",
              "| captured", len(capture))
    elif command:
        print("Commands: tap 1|2|3, hold 1|2|3, save, state")


def update_serial():
    """Collect characters typed in the serial console; run each full line."""
    global serial_line
    while supervisor.runtime.serial_bytes_available:
        character = sys.stdin.read(1)
        if character in "\r\n":
            run_command(serial_line.strip())
            serial_line = ""
        else:
            serial_line += character


# --- Knobs ---
def handle_cc(control, value):
    """Turn knob movements (MIDI CC messages) into changes in the synth sound."""
    global wave_index, timbre, shape, waveform
    if PRINT_CC:
        print("CC", control, value)
    if control == CC_CUTOFF:
        lowpass.frequency = CUTOFF_MIN * (CUTOFF_MAX / CUTOFF_MIN) ** (value / 127)
    elif control == CC_RESONANCE:
        lowpass.Q = 0.707 + value / 127 * 5.3
    elif control in (CC_WAVE, CC_TIMBRE, CC_SHAPE):
        if control == CC_WAVE:
            new_index = value * len(BASE_WAVES) // 128
            if new_index != wave_index:
                print("Wave:", WAVE_NAMES[new_index])
            wave_index = new_index
        elif control == CC_TIMBRE:
            timbre = value / 127
        else:
            shape = value / 127
        waveform = build_waveform()
        for voice in active_notes.values():
            voice.waveform = waveform


# --- MIDI input ---
status = None
needed_data = 0
pending_data = []


def parse_midi_byte(value):
    """Assemble raw MIDI bytes into messages, including running status."""
    global status, needed_data, pending_data
    if value >= 0xF8:  # real-time bytes can arrive between any other bytes
        return
    if value & 0x80:
        if 0x80 <= value <= 0xEF:  # channel voice message
            status = value
            needed_data = 1 if (value & 0xF0) in (0xC0, 0xD0) else 2
        else:  # ignore system common and SysEx messages
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
            capture_event(status, pending_data[0], pending_data[1])  # for gruv saves
            handle_cc(pending_data[0], pending_data[1])
        pending_data = []


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
            # 20 ms timeout: in CircuitPython 10.x a message arriving just as a
            # read times out can be lost, so fewer timeouts = fewer lost notes.
            # See https://github.com/adafruit/circuitpython/issues/10554
            raw_midi = adafruit_usb_host_midi.MIDI(device, timeout=0.02)
        except (ValueError, usb.core.USBError):
            continue
        if raw_midi.in_ep == 0:
            continue  # not a MIDI device (e.g. a computer keyboard or mouse)
        print("Found MIDI keyboard:", hex(device.idVendor), hex(device.idProduct))
        return raw_midi
    return None


# --- Startup sound check ---
for midi_note in (72, 76, 79, 84):
    voice = synthio.Note(
        frequency=synthio.midi_to_hz(midi_note),
        waveform=waveform,
        envelope=envelope,
        amplitude=STARTUP_AMPLITUDE,
    )
    synth.press(voice)
    time.sleep(0.15)
    synth.release(voice)
    time.sleep(0.03)
print("Looper: empty (tap button 1 to record)")

# --- Main loop ---
while True:
    # Read everything waiting from the computer first, so its messages are
    # finished before any keyboard bytes reach the parser.
    data = midi_in.read(1)
    while data:
        for byte in data:
            parse_midi_byte(byte)
        data = midi_in.read(1)

    if USE_USB_HOST_MIDI:
        if keyboard is None and time.monotonic() - last_keyboard_scan > 2:
            last_keyboard_scan = time.monotonic()
            keyboard = find_keyboard()
        if keyboard is not None:
            try:
                data = keyboard.read(64)
                if data:
                    for byte in data:
                        parse_midi_byte(byte)
            except usb.core.USBError:
                print("MIDI keyboard disconnected")
                keyboard = None

    update_buttons()
    if SERIAL_COMMANDS:
        update_serial()
    update_playback()
    update_pixels()
