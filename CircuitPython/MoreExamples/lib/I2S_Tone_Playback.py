import time
import array
import math
import audiocore
import board
import audiobusio

audio = audiobusio.I2SOut(board.A0, board.A1, board.A2)

tone_volume = 0.58  # Increase this to increase the volume of the tone. ~.58 and above gets really loud
frequency = 440  # Set this to the Hz of the tone you want to generate.
length = 8000 // frequency
sine_wave = array.array("h", [0] * length)
for i in range(length):
    sine_wave[i] = int((math.sin(math.pi * 2 * i / length)) * tone_volume * (2 ** 15 - 1))
sine_wave_sample = audiocore.RawSample(sine_wave)

while True:
    audio.play(sine_wave_sample, loop=True)
    time.sleep(1)
    audio.stop()
    time.sleep(1)