This firmware was built **with** BLE support and without over the air update (OTA) support.
This firmware must be flashed using esptool (either on your computer or using the web tool).

[Enter bootloader mode](https://learn.adafruit.com/esp32-s3-reverse-tft-feather/factory-reset#step-2-enter-rom-bootloader-mode-3106832)

```
esptool.py -p {/dev/tty.usbmodem...} erase_flash
esptool.py -p {/dev/tty.usbmodem...} write_flash 0x0 esp32s3_reverse_tft_cp92_no_ota.bin
```

To get esptool.py
* With Homebrew on Mac ```brew install esptool```
