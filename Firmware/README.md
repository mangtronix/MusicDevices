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

To get esptool.py
* With Homebrew on Mac ```brew install esptool```
