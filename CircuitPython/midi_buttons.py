# SPDX-FileCopyrightText: 2021 John Park for Adafruit Industries
# SPDX-License-Identifier: MIT
# midi_UARToutdemo.py - demonstrates sending MIDI notes
#
# Adapted for USB MIDI by Michael Ang for NYUAD Music Devices

# For USB MIDI on the ESP32 S3 Reverse TFT Feather you must put this
# code into your boot.py file and physically unplug the board
# to enable USB MIDI
# See https://learn.adafruit.com/customizing-usb-devices-in-circuitpython/circuitpy-midi-serial

print("midi_buttons")

import time
import board
import digitalio
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

# Button setup
button0 = digitalio.DigitalInOut(board.D0)
button0.switch_to_input(pull=digitalio.Pull.UP)

button1 = digitalio.DigitalInOut(board.D1)
button1.switch_to_input(pull=digitalio.Pull.DOWN)

button2 = digitalio.DigitalInOut(board.D2)
button2.switch_to_input(pull=digitalio.Pull.DOWN)

# Keep track if button was previously pressed so we can trigger
# note on/off at moment a button is pressed / released
button_was_pressed = [False, False, False]

# Which notes to play
# See examples at
# https://learn.adafruit.com/midi-melody-maker/circuitpython-code-walkthrough#create-the-midi-note-arrays-3073059
c_scale = [60, 62, 64, 65, 67, 69, 71, 72]
e_minor_scale = [64, 66, 67, 69, 71, 72, 74]
imperial_march = [51, 55, 58]
notes = imperial_march

# What velocity to send for note on events
velocity = 100

print("MIDI buttons")
print("Default output channel:", midi.out_channel + 1)

"""Turn all of our notes off"""
def notesOff():
    for note in notes:
        midi.send(NoteOff(note, 0))

# Start by turning everything off, in case we left them on (e.g. hardware reset)
notesOff()

while True:
    # Check buttons and send note on / off as appropriate

    # Button D0 goes false when it's pressed
    if button0.value == False:
        # Pressed
        if not button_was_pressed[0]:
            note = notes[0]
            print(f"Note {note} ON")
            midi.send(NoteOn(note, velocity))
            button_was_pressed[0] = True
    else:
        # Not pressed
        if button_was_pressed[0]:
            note = notes[0]
            print(f"Note {note} off")
            midi.send(NoteOff(note, 0))
            button_was_pressed[0] = False

    # Button D1 goes true when it's pressed
    if button1.value == True:
        # Pressed
        if not button_was_pressed[1]:
            note = notes[1]
            print(f"Note {note} ON")
            midi.send(NoteOn(note, velocity))
            button_was_pressed[1] = True
    else:
        # Not pressed
        if button_was_pressed[1]:
            note = notes[1]
            print(f"Note {note} off")
            midi.send(NoteOff(note, 0))
            button_was_pressed[1] = False

    # Button D2 goes false when it's pressed
    if button2.value == True:
        # Pressed
        if not button_was_pressed[2]:
            note = notes[2]
            print(f"Note {note} ON")
            midi.send(NoteOn(note, velocity))
            button_was_pressed[2] = True
    else:
        # Not pressed
        if button_was_pressed[2]:
            note = notes[2]
            print(f"Note {note} off")
            midi.send(NoteOff(note, 0))
            button_was_pressed[2] = False


      # Write your code here :-)
