# SPDX-FileCopyrightText: 2021 John Park for Adafruit Industries
# SPDX-License-Identifier: MIT
# midi_UARToutdemo.py - demonstrates sending MIDI notes
#
# Adapted for USB MIDI by Michael Ang for NYUAD Music Devices

# For USB MIDI on the ESP32 S3 Reverse TFT Feather you must put this
# code into your boot.py file and physically unplug the board
# to enable USB MIDI
# See https://learn.adafruit.com/customizing-usb-devices-in-circuitpython/circuitpy-midi-serial

print("midi_demo")

code_for_boot_py = """
import usb_hid, usb_midi

# On some boards, we need to give up HID to free up a resource for MIDI.
print("Enabling MIDI")
usb_hid.disable()
usb_midi.enable()
"""

import time
import board
import busio
import adafruit_midi
import usb_midi

from adafruit_midi.control_change import ControlChange
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn

# Hardware serial port for physical MIDI Featherwing
# uart = busio.UART(board.TX, board.RX, baudrate=31250, timeout=0.001)  # init UART

# USB MIDI
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
note_hold = 0.85
rest = note_hold / 5

print("MIDI Out demo")
print("Default output channel:", midi.out_channel + 1)
print("Check the output with a MIDI monitor or synth")

while True:
    print("Sending MIDI messages on channel", midi.out_channel + 1)
    # midi.send(ControlChange(64, 0))  # sustain CC
    midi.send(ControlChange(1, 0))  # modulation CC

    midi.send(NoteOn(48, 20))  # play note
    time.sleep(note_hold)  # hold note
    midi.send(NoteOff(48, 0))  # release note
    time.sleep(rest)  # rest

    midi.send(NoteOn(55, 40))
    time.sleep(note_hold)
    midi.send(NoteOff(55, 0))
    time.sleep(rest)

    midi.send(NoteOn(51, 60))
    time.sleep(note_hold)
    midi.send(NoteOff(51, 0))
    time.sleep(rest)

    midi.send(NoteOn(58, 80))
    time.sleep(note_hold)
    midi.send(NoteOff(58, 0))
    time.sleep(rest)

    # midi.send(ControlChange(64, 32))
    midi.send(ControlChange(1, 127))

    midi.send(NoteOn(48, 20))  # play note
    time.sleep(note_hold)  # hold note
    midi.send(NoteOff(48, 0))  # release note
    time.sleep(rest)  # rest

    midi.send(NoteOn(55, 40))
    time.sleep(note_hold)
    midi.send(NoteOff(55, 0))
    time.sleep(rest)

    midi.send(NoteOn(51, 60))
    time.sleep(note_hold)
    midi.send(NoteOff(51, 0))
    time.sleep(rest)

    midi.send(NoteOn(50, 80))
    time.sleep(note_hold)
    midi.send(NoteOff(50, 0))
    time.sleep(rest)
