This firmware was built **with** BLE support and without over the air update (OTA) support.
This firmware must be flashed using esptool (either on your computer or using the web tool).

[Enter bootloader mode](https://learn.adafruit.com/esp32-s3-reverse-tft-feather/factory-reset#step-2-enter-rom-bootloader-mode-3106832)

Flash custom firmware:
```
esptool.py -p {/dev/tty.usbmodem...} erase_flash
esptool.py -p {/dev/tty.usbmodem...} write_flash 0x0 esp32s3_reverse_tft_cp92_no_ota.bin
```

Press reset button or plug / unplug to do a hard reset. You should now see ```CIRCUITPY``` drive.  ```boot_out.txt``` should start with:
```
Adafruit CircuitPython 9.2.4-247-g6e7baead68-dirty on 2025-03-04; Adafruit Feather ESP32-S3 Reverse TFT with ESP32S3
```

Copy [boot.py](https://github.com/mangtronix/MusicDevices/blob/main/CircuitPython/boot.py) to ```CIRCUITPY/```

Hard reset with button or plug/unplug
```boot_out.txt``` should end with "Enabling MIDI":
```
Adafruit CircuitPython 9.2.4-247-g6e7baead68-dirty on 2025-03-04; Adafruit Feather ESP32-S3 Reverse TFT with ESP32S3
Board ID:adafruit_feather_esp32s3_reverse_tft
UID:468E3347E588
boot.py output:
Enabling MIDI
```

To get esptool.py
* With Homebrew on Mac ```brew install esptool```

Copy [necessary libraries](https://github.com/mangtronix/MusicDevices/tree/main/CircuitPython/lib) to ```CIRCUITPY/lib```:
* adafruit_ble
* adafruit_ble_midi.mpy
* adafruit_midi
