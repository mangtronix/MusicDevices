print("Keeb")

# Keys + NeoPixels

# Includes code from:
# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT


"""CircuitPython Essentials Digital In Out example"""
import time
import board
import digitalio
from digitalio import DigitalInOut, Direction, Pull
from adafruit_debouncer import Debouncer
import neopixel

import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff

# Set true to log
serial_debug = False


# Pins for our keys
keeb_pins = [board.D5, board.D6, board.D9, board.D10]
keeb_colors = [(255, 23, 123), (255, 155, 0), (0,0,255,0), (139,0,139)]
keeb_notes = [60,61,62,63] # MIDI notes

# NeoPixel strip
pixel_pin = board.A1
num_pixels = 6
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False)
pixels.fill(0)
pixels.show()

# To hold objects
keeb_switches = []

# LED setup.
led = DigitalInOut(board.LED)
# For QT Py M0. QT Py M0 does not have a D13 LED, so you can connect an external LED instead.
# led = DigitalInOut(board.SCK)
led.direction = Direction.OUTPUT


for keeb_pin in keeb_pins:
    pin = digitalio.DigitalInOut(keeb_pin)
    pin.direction = digitalio.Direction.INPUT
    pin.pull = digitalio.Pull.UP
    switch = Debouncer(pin)
    keeb_switches.append(switch)


# MIDI setup
midi_channel = 1
midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1],
                          out_channel=midi_channel-1)

while True:
    pixels_need_update = False # True if we need to redisplay

    # Update switches
    for index, switch in enumerate(keeb_switches):
        switch.update()

        # Switches are pullups - go low when pressed
        if switch.fell:
            if serial_debug:
                print("Switch %d pressed" % (index + 1))
            pixels[index] = keeb_colors[index]
            midi.send(NoteOn(keeb_notes[index]))
            pixels_need_update = True

        elif switch.rose:
            pixels[index] = (0, 0, 0)
            pixels_need_update = True
            midi.send(NoteOff(keeb_notes[index]))


        # Map LED to first button
        if index == 0:
            if switch.fell:
                led.value = True
            elif switch.rose:
                led.value = False

    if pixels_need_update:
        pixels.show()


    time.sleep(0.01)  # debounce delay


#type: ignore
