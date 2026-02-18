# SPDX-FileCopyrightText: 2021 John Park for Adafruit Industries
# SPDX-License-Identifier: MIT
# midi_UARToutdemo.py - demonstrates sending MIDI notes
#
# Adapted for BLE MIDI by Michael Ang for NYUAD Music Devices

# For BLE MIDI on the ESP32 S3 Reverse TFT Feather with CircuitPython 9
# you need to flash a custom CircuitPython build that includes BLE support
# See https://github.com/mangtronix/MusicDevices/tree/main/Firmware for instructions


print("midi_buttons_ble")

import time
import board
import digitalio
import busio

import adafruit_ble
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
import adafruit_midi
from adafruit_midi.control_change import ControlChange
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_midi.pitch_bend import PitchBend
import adafruit_ble_midi


from adafruit_midi.control_change import ControlChange
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn

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

# BLE MIDI setup
# Use default HID descriptor
midi_service = adafruit_ble_midi.MIDIService()
advertisement = ProvideServicesAdvertisement(midi_service)
# advertisement.appearance = 961

ble = adafruit_ble.BLERadio()
if ble.connected:
    for c in ble.connections:
        c.disconnect()

midi = adafruit_midi.MIDI(midi_out=midi_service, out_channel=0)
print("Default output channel:", midi.out_channel + 1)

print("Advertising BLE MIDI service")
ble.start_advertising(advertisement)


"""Turn all of our notes off"""
def notesOff():
    for note in notes:
        midi.send(NoteOff(note, 0))

# Start by turning everything off, in case we left them on (e.g. hardware reset)
notesOff()

while True:
    print("Waiting for connection")
    while not ble.connected:
        pass
    print("Connected")
    # Sleep briefly so client can get ready and send setup
    # writes to the MIDIService. 0.5secs was insufficient.
    time.sleep(1.0)
    notesOff() # reset any stuck notes
    
    while ble.connected:
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



    print("Disconnected")
    print()
    ble.start_advertising(advertisement)



