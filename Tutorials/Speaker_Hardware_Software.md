# Setting up Speaker Hardware & Software
Full tutorial here: [Adafruit Metro ESP32-S3](https://learn.adafruit.com/adafruit-metro-esp32-s3/i2s#i2s-tone-playback-3124643)
# Hardware
1. Soldering
  - Solder red and black wires to the speaker: red for (+), black for (-).
    - <img src="Media/Speaker_Tutorial_2.jpeg" width="200"> 
  - Solder the male pin header strip to the Amplifier Breakout (solder shorter end of pins to amplifier)
    - <img src="Media/Speaker_Tutorial_5.jpg" width="200">
  - Solder green terminal block to the breakout board
    - <img src="Media/Speaker_Tutorial_6.png" width="200">
2. Pin Connections
  -  The board in this example image is a little different than ours, but you can still find the same pins:
    - <img src="Media/Speaker_Tutorial_7.png" width="450">
  - As pictured: GND to GND in black, 3V to VIN in red, A0 to BCLK in blue, A1 to LRC in yellow, A2 to DIN in purple
  - Connect the (+) on the speaker via red wire to the (+) on the green terminal block. Screw in the screw on top of the green terminal block to secure wires.
    - <img src="Media/Speaker_Tutorial_1.jpeg" width="200">
    - <img src="Media/Speaker_Tutorial_3.jpeg" width="200">
3. Final outcome
  - You'll need to use screw extensions to put our feather board back onto the portable 3D printed backing.
    - <img src="Media/Speaker_Tutorial_8.JPG" width="200">
  - You can also screw in the amplifier board like so:
    - <img src="Media/Speaker_Tutorial_4.jpeg" width="200">

# Software
1. Tone playback example
   - Copy this code into your code.py file to get a tone/frequency to play from the speaker: 
   - [Tone Playback python file](CircuitPython/MoreExamples/lib/I2S_Tone_Playback.py)

