# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT
#
# Modified by Michael Ang for NYUAD IM Music Devices
# - faster color cycling
# - lower default brightness
#
# Instructions:
# - rotate encoder to change color
# - push and rotate encoder to change brightness

"""I2C rotary encoder NeoPixel color picker and brightness setting example."""

print("demo_rotaryneopixel")

import board
from rainbowio import colorwheel
from adafruit_seesaw import seesaw, neopixel, rotaryio, digitalio

# How fast to cycle through color wheel with each detent of encoder
color_increment = 2

# For use with the STEMMA connector on QT Py RP2040
# import busio
# i2c = busio.I2C(board.SCL1, board.SDA1)
# seesaw = seesaw.Seesaw(i2c, 0x36)

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
seesaw = seesaw.Seesaw(i2c, 0x36)

encoder = rotaryio.IncrementalEncoder(seesaw)
seesaw.pin_mode(24, seesaw.INPUT_PULLUP)
switch = digitalio.DigitalIO(seesaw, 24)

pixel = neopixel.NeoPixel(seesaw, 6, 1)
pixel.brightness = 0.25

last_position = -1
color = 0  # start at red

while True:
    # negate the position to make clockwise rotation positive
    position = -encoder.position

    if position != last_position:
        print(position)

        if switch.value:
            # Change the LED color.
            if position > last_position:  # Advance forward through the colorwheel.
                color += color_increment
            else:
                color -= color_increment  # Advance backward through the colorwheel.
            color = (color + 256) % 256  # wrap around to 0-256
            pixel.fill(colorwheel(color))

        else:  # If the button is pressed...
            # ...change the brightness.
            if position > last_position:  # Increase the brightness.
                pixel.brightness = min(1.0, pixel.brightness + 0.1)
            else:  # Decrease the brightness.
                pixel.brightness = max(0, pixel.brightness - 0.1)

    last_position = position
