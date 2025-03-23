import time, board, digitalio, audiobusio, audiocore

try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        print("This board does not support AudioOut")
        pass # not all boards support 

audio = audiobusio.I2SOut(board.D5, board.D6, board.D9)

def play_sound(filename):
    wav = audiocore.WaveFile(open(filename, "rb"))
    audio.play(wav)
    while audio.playing:
        pass # add code you want to run while sound is playing

play_sound("StreetChicken.wav")