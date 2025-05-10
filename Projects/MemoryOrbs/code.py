# import board
# import busio
# import neopixel
# import adafruit_mpr121
# import time
# import touchio
# import usb_midi
# import adafruit_midi
# from adafruit_midi.note_on import NoteOn

# # === CONFIGURATION ===
# PIXELS_PER_ORB = 6
# DELAY = 0.05
# LOOP_DURATION = 4.0
# last_loop_time = time.monotonic()

# # MIDI setup
# midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

# orbs_config = [
#     {"touch_pin": 0, "neopixel_pin": board.D10, "start_pixel": 0,  "color": (0, 255, 0, 0), "midi_note": 60},
#     {"touch_pin": 1, "neopixel_pin": board.D10, "start_pixel": 6,  "color": (0, 255, 0, 0), "midi_note": 61},
#     {"touch_pin": 2, "neopixel_pin": board.D10, "start_pixel": 12, "color": (0, 255, 0, 0), "midi_note": 62},
#     {"touch_pin": 3, "neopixel_pin": board.A1,  "start_pixel": 0,  "color": (255, 0, 0, 0), "midi_note": 63},
#     {"touch_pin": 4, "neopixel_pin": board.A1,  "start_pixel": 6,  "color": (255, 0, 0, 0), "midi_note": 64},
#     {"touch_pin": 5, "neopixel_pin": board.A1,  "start_pixel": 12, "color": (255, 0, 0, 0), "midi_note": 65},
#     {"touch_pin": 6, "neopixel_pin": board.D9,  "start_pixel": 0,  "color": (255, 130, 0, 0), "midi_note": 66},
#     {"touch_pin": 7, "neopixel_pin": board.D9,  "start_pixel": 6,  "color": (255, 130, 0, 0), "midi_note": 67},
#     {"touch_pin": 8, "neopixel_pin": board.D9,  "start_pixel": 12, "color": (255, 130, 0, 0), "midi_note": 68},
#     {"touch_pin": 9, "neopixel_pin": board.D5,  "start_pixel": 0,  "color": (128, 0, 128, 0), "midi_note": 69},
#     {"touch_pin": 10,"neopixel_pin": board.D5,  "start_pixel": 6,  "color": (128, 0, 128, 0), "midi_note": 70},
#     {"touch_pin": 11,"neopixel_pin": board.D5,  "start_pixel": 12, "color": (128, 0, 128, 0), "midi_note": 71},
# ]

# orbs_config_esp = [
#     {"touch_pin": board.D12, "neopixel_pin": board.D6, "start_pixel": 0,  "color": (0, 0, 255, 0), "midi_note": 72},
#     {"touch_pin": board.D11, "neopixel_pin": board.D6, "start_pixel": 6,  "color": (0, 0, 255, 0), "midi_note": 73},
#     {"touch_pin": board.A4,  "neopixel_pin": board.D6, "start_pixel": 12, "color": (0, 0, 255, 0), "midi_note": 74},
# ]

# GOLDEN = (255, 100, 0, 0)

# # MPR121
# i2c = busio.I2C(board.SCL, board.SDA)
# mpr121 = adafruit_mpr121.MPR121(i2c)
# print('MIDI Orbs initialized')

# # Pixel buffer per strip
# pixel_strips = {}
# for orb in orbs_config + orbs_config_esp:
#     pin = orb["neopixel_pin"]
#     if pin not in pixel_strips:
#         pixel_strips[pin] = neopixel.NeoPixel(
#             pin, 18, brightness=0.7, auto_write=False, pixel_order=neopixel.GRBW
#         )

# # === ORB CLASSES ===
# class Orb:
#     def __init__(self, config):
#         self.touch_pin = config["touch_pin"]
#         self.start_pixel = config["start_pixel"]
#         self.color = config["color"]
#         self.midi_note = config["midi_note"]
#         self.strip = pixel_strips[config["neopixel_pin"]]
#         self.state = False
#         self.prev_touched = False
#         self.requested_start = False
#         self.last_touch_time = 0
#         self.debounce_ms = 200

#     def update(self):
#         try:
#             touched = mpr121[self.touch_pin].value
#         except Exception as e:
#             print(f"Touch read error: {e}")
#             touched = False
#         now = time.monotonic() * 1000
#         if touched and not self.prev_touched and (now - self.last_touch_time > self.debounce_ms):
#             self.last_touch_time = now
#             self.toggle()
#         self.prev_touched = touched

#     def toggle(self):
#         if not self.state:
#             self.state = True
#             self.requested_start = True
#         else:
#             self.state = False
#             self.requested_start = False
#             midi.send(NoteOn(self.midi_note, 127))
#         self.apply_lighting()

#     def apply_lighting(self, override_color=None):
#         color = override_color if override_color else (self.color if self.state else (0, 0, 0, 0))
#         for i in range(self.start_pixel, self.start_pixel + PIXELS_PER_ORB):
#             self.strip[i] = color

# class ESPTouchOrb:
#     def __init__(self, config):
#         self.touch = touchio.TouchIn(config["touch_pin"])
#         self.start_pixel = config["start_pixel"]
#         self.color = config["color"]
#         self.midi_note = config["midi_note"]
#         self.strip = pixel_strips[config["neopixel_pin"]]
#         self.state = False
#         self.prev_touched = False
#         self.requested_start = False
#         self.THRESHOLD = 40000
#         self.last_touch_time = 0
#         self.debounce_ms = 200

#     def update(self):
#         raw = self.touch.raw_value
#         touched = raw > self.THRESHOLD
#         now = time.monotonic() * 1000
#         if touched and not self.prev_touched and (now - self.last_touch_time > self.debounce_ms):
#             self.last_touch_time = now
#             self.toggle()
#         self.prev_touched = touched

#     def toggle(self):
#         if not self.state:
#             self.state = True
#             self.requested_start = True
#         else:
#             self.state = False
#             self.requested_start = False
#             midi.send(NoteOn(self.midi_note, 127))
#         self.apply_lighting()

#     def apply_lighting(self, override_color=None):
#         color = override_color if override_color else (self.color if self.state else (0, 0, 0, 0))
#         for i in range(self.start_pixel, self.start_pixel + PIXELS_PER_ORB):
#             self.strip[i] = color

# # === INIT ORBS ===
# orbs = [Orb(config) for config in orbs_config] + [ESPTouchOrb(config) for config in orbs_config_esp]

# # === MAIN LOOP ===
# while True:
#     current_time = time.monotonic()

#     for orb in orbs:
#         orb.update()

#     active_pin_ids = set()
#     for orb in orbs:
#         is_touched = False
#         if isinstance(orb, Orb):
#             try:
#                 is_touched = mpr121[orb.touch_pin].value
#             except:
#                 pass
#         else:
#             is_touched = orb.touch.raw_value > orb.THRESHOLD
#         if is_touched:
#             for pin, strip in pixel_strips.items():
#                 if strip is orb.strip:
#                     active_pin_ids.add(pin)

#     golden_mode = len(active_pin_ids) >= 3

#     for orb in orbs:
#         if golden_mode:
#             orb.apply_lighting(GOLDEN)
#         else:
#             orb.apply_lighting()

#     # MIDI Loop Sync
#     if current_time - last_loop_time >= LOOP_DURATION:
#         last_loop_time = current_time
#         for orb in orbs:
#             if orb.requested_start:
#                 midi.send(NoteOn(orb.midi_note, 127))
#                 orb.requested_start = False
#                 print(f"Orb {orb.midi_note}: MIDI STARTED at loop sync")

#     # Update NeoPixel strips
#     for strip in pixel_strips.values():
#         strip.show()

#     time.sleep(DELAY)

import board
import busio
import neopixel
import adafruit_mpr121
import time
import touchio
import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
from adafruit_midi.control_change import ControlChange

# === CONFIGURATION ===
PIXELS_PER_ORB = 6
DELAY = 0.05
LOOP_DURATION = 4.0
last_loop_time = time.monotonic()
active_notes = set()


# MIDI setup
midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

# MIDI CC to trigger Inside Out theme song in Ableton
THEME_SONG_CC = 100  # Choose an appropriate CC number
THEME_SONG_VALUE = 127  # Value to send when triggering

orbs_config = [
    {"touch_pin": 0, "neopixel_pin": board.D10, "start_pixel": 0,  "color": (0, 255, 0, 0), "midi_note": 60},
    {"touch_pin": 1, "neopixel_pin": board.D10, "start_pixel": 6,  "color": (0, 255, 0, 0), "midi_note": 61},
    {"touch_pin": 2, "neopixel_pin": board.D10, "start_pixel": 12, "color": (0, 255, 0, 0), "midi_note": 62},
    {"touch_pin": 3, "neopixel_pin": board.A1,  "start_pixel": 0,  "color": (255, 0, 0, 0), "midi_note": 63},
    {"touch_pin": 4, "neopixel_pin": board.A1,  "start_pixel": 6,  "color": (255, 0, 0, 0), "midi_note": 64},
    {"touch_pin": 5, "neopixel_pin": board.A1,  "start_pixel": 12, "color": (255, 0, 0, 0), "midi_note": 65},
    {"touch_pin": 6, "neopixel_pin": board.D9,  "start_pixel": 0,  "color": (255, 130, 0, 0), "midi_note": 66},
    {"touch_pin": 7, "neopixel_pin": board.D9,  "start_pixel": 6,  "color": (255, 130, 0, 0), "midi_note": 67},
    {"touch_pin": 8, "neopixel_pin": board.D9,  "start_pixel": 12, "color": (255, 130, 0, 0), "midi_note": 68},
    {"touch_pin": 9, "neopixel_pin": board.D5,  "start_pixel": 0,  "color": (128, 0, 128, 0), "midi_note": 69},
    {"touch_pin": 10,"neopixel_pin": board.D5,  "start_pixel": 6,  "color": (128, 0, 128, 0), "midi_note": 70},
    {"touch_pin": 11,"neopixel_pin": board.D5,  "start_pixel": 12, "color": (128, 0, 128, 0), "midi_note": 71},
]

orbs_config_esp = [
    {"touch_pin": board.D12, "neopixel_pin": board.D6, "start_pixel": 0,  "color": (0, 0, 255, 0), "midi_note": 72},
    {"touch_pin": board.D11, "neopixel_pin": board.D6, "start_pixel": 6,  "color": (0, 0, 255, 0), "midi_note": 73},
    {"touch_pin": board.A4,  "neopixel_pin": board.D6, "start_pixel": 12, "color": (0, 0, 255, 0), "midi_note": 74},
]

GOLDEN = (255, 100, 0, 0)

# MPR121
i2c = busio.I2C(board.SCL, board.SDA)
mpr121 = adafruit_mpr121.MPR121(i2c)
print('MIDI Orbs initialized')

# Pixel buffer per strip
pixel_strips = {}
for orb in orbs_config + orbs_config_esp:
    pin = orb["neopixel_pin"]
    if pin not in pixel_strips:
        pixel_strips[pin] = neopixel.NeoPixel(
            pin, 18, brightness=0.7, auto_write=False, pixel_order=neopixel.GRBW
        )

# === ORB CLASSES ===
class Orb:
    def __init__(self, config):
        self.touch_pin = config["touch_pin"]
        self.start_pixel = config["start_pixel"]
        self.color = config["color"]
        self.midi_note = config["midi_note"]
        self.strip = pixel_strips[config["neopixel_pin"]]
        self.state = False
        self.prev_touched = False
        self.requested_start = False
        self.last_touch_time = 0
        self.debounce_ms = 200
        self.note_playing = False

    def update(self):
        try:
            touched = mpr121[self.touch_pin].value
        except Exception as e:
            print(f"Touch read error: {e}")
            touched = False
        now = time.monotonic() * 1000
        if touched and not self.prev_touched and (now - self.last_touch_time > self.debounce_ms):
            self.last_touch_time = now
            self.toggle()
        self.prev_touched = touched

    def toggle(self):
        if not self.state:
            self.state = True
            self.requested_start = True
        else:
            self.state = False
            self.requested_start = False
            if not golden_active:  # Only play individual notes when not in golden mode
                midi.send(NoteOn(self.midi_note, 127))
                self.note_playing = True
        self.apply_lighting()

    def stop_sound(self):
        if self.note_playing:
            midi.send(NoteOn(self.midi_note, 127))
            self.note_playing = False

    def apply_lighting(self, override_color=None):
        color = override_color if override_color else (self.color if self.state else (0, 0, 0, 0))
        for i in range(self.start_pixel, self.start_pixel + PIXELS_PER_ORB):
            self.strip[i] = color

class ESPTouchOrb:
    def __init__(self, config):
        self.touch = touchio.TouchIn(config["touch_pin"])
        self.start_pixel = config["start_pixel"]
        self.color = config["color"]
        self.midi_note = config["midi_note"]
        self.strip = pixel_strips[config["neopixel_pin"]]
        self.state = False
        self.prev_touched = False
        self.requested_start = False
        self.THRESHOLD = 40000
        self.last_touch_time = 0
        self.debounce_ms = 200
        self.note_playing = False

    def update(self):
        raw = self.touch.raw_value
        touched = raw > self.THRESHOLD
        now = time.monotonic() * 1000
        if touched and not self.prev_touched and (now - self.last_touch_time > self.debounce_ms):
            self.last_touch_time = now
            self.toggle()
        self.prev_touched = touched

    def toggle(self):
        if not self.state:
            self.state = True
            self.requested_start = True
        else:
            self.state = False
            self.requested_start = False
            if not golden_active:  # Only play individual notes when not in golden mode
                midi.send(NoteOn(self.midi_note, 127))
                self.note_playing = True
        self.apply_lighting()

    def stop_sound(self):
        if self.note_playing:
            midi.send(NoteOff(self.midi_note, 0))
            self.note_playing = False

    def apply_lighting(self, override_color=None):
        color = override_color if override_color else (self.color if self.state else (0, 0, 0, 0))
        for i in range(self.start_pixel, self.start_pixel + PIXELS_PER_ORB):
            self.strip[i] = color

# === INIT ORBS ===
orbs = [Orb(config) for config in orbs_config] + [ESPTouchOrb(config) for config in orbs_config_esp]

# === GLOBAL STATE ===
golden_active = False
was_golden_active = False

# === MAIN LOOP ===
while True:
    current_time = time.monotonic()

    for orb in orbs:
        orb.update()

    active_pin_ids = set()
    for orb in orbs:
        is_touched = False
        if isinstance(orb, Orb):
            try:
                is_touched = mpr121[orb.touch_pin].value
            except:
                pass
        else:
            is_touched = orb.touch.raw_value > orb.THRESHOLD
        if is_touched:
            for pin, strip in pixel_strips.items():
                if strip is orb.strip:
                    active_pin_ids.add(pin)

    # Detect when we enter golden mode
    was_golden_active = golden_active
    golden_active = len(active_pin_ids) >= 5
    
    # If we just entered golden mode, stop all sounds and play theme
    if golden_active and not was_golden_active:
        print("Golden mode activated!")
        
        # Stop all orb sounds
        for orb in orbs:
            orb.stop_sound()
            
        # Trigger Inside Out theme song in Ableton
        midi.send(ControlChange(THEME_SONG_CC, THEME_SONG_VALUE))
    
    # When golden mode ends, turn off all orbs
    if was_golden_active and not golden_active:
        print("Golden mode deactivated - resetting all orbs")
        for orb in orbs:
            orb.state = False
            orb.requested_start = False
            orb.stop_sound()
            
        midi.send(ControlChange(THEME_SONG_CC, THEME_SONG_VALUE))  # Sends a "stop" or "off" signal

    
    # Update orb lighting based on current state
    for orb in orbs:
        if golden_active:
            orb.apply_lighting(GOLDEN)
        else:
            orb.apply_lighting()

    # MIDI Loop Sync
    if current_time - last_loop_time >= LOOP_DURATION:
        last_loop_time = current_time
        for orb in orbs:
            if orb.requested_start and not golden_active:  # Only start new notes when not in golden mode
                midi.send(NoteOn(orb.midi_note, 127))
                orb.note_playing = True
                orb.requested_start = False
                print(f"Orb {orb.midi_note}: MIDI STARTED at loop sync")

    # Update NeoPixel strips
    for strip in pixel_strips.values():
        strip.show()

    time.sleep(DELAY)