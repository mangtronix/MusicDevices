# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT
#
# Modified by Michael Ang for NYUAD IM Music Devices
# - Use address 0x37 to avoid conflict with ESP32-S3 Reverse TFT battery monitor
# - Faster color cycling
# - Lower default brightness
# - Additional debug output
#
# Instructions:
# - rotate encoder to change color
# - push and rotate encoder to change brightness

"""I2C rotary encoder NeoPixel color picker and brightness setting example."""

print("demo_encoder_neopixel")

# IMPORTANT§
# The default address of 0x36 conflicts with the default address of the
# ESP32-S3 Reverse TFT battery monitor. To use the rotary encoder we
# can change the address by soldering the A0 jumper on the back of the
# board to change the address to 0x37
encoder_address = 0x37
print("Using rotary encoder at address: ", hex(encoder_address))
print("Make sure to solder the A0 jumper on the back of the board to change the address to 0x37")
print("Turn to change hue, push and turn to change brightness")


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
seesaw = seesaw.Seesaw(i2c, encoder_address)

encoder = rotaryio.IncrementalEncoder(seesaw)
seesaw.pin_mode(24, seesaw.INPUT_PULLUP)
button = digitalio.DigitalIO(seesaw, 24)

pixel = neopixel.NeoPixel(seesaw, 6, 1)
pixel.brightness = 0.2

last_position = -1
color = 0  # start at red

# Boolean to track button state so can detect when it is pressed and released as
# discrete transitions
button_was_held = False

while True:
    # Get the current encoder position. We could negate this value to change
    # the direction of rotation if desired
    position = encoder.position

    # Debug output for the switch state and position
    # button.value is False when the button is pressed
    if not button.value:
        # Button currently pressed
        if not button_was_held:
            # Button was just pressed
            print("Button pressed")
            button_was_held = True
    else:
        # Button currently not pressed
        if button_was_held:
            # Button was just released
            print("Button released")
            button_was_held = False

    if position != last_position:
        print("Position:", position)

        if button.value:
            # Change the LED color.
            if position > last_position:  # Advance forward through the colorwheel.
                color += color_increment
            else:
                color -= color_increment  # Advance backward through the colorwheel.
            color = (color + 256) % 256  # wrap around to 0-256
            pixel.fill(colorwheel(color))

        else:  # If the button is pressed...
            # ...change the brightness.
            if position < last_position: # Decrease the brightness.
                pixel.brightness = max(0, pixel.brightness - 0.1)
            else: # Increase the brightness.
                pixel.brightness = min(1.0, pixel.brightness + 0.1)

    last_position = position
