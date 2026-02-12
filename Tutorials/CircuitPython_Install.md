# CircuitPython full reset / install

ESP32-S3 Reverse TFT Feather
- We need to perform low level reset to install the latest bootloader which enables BLE MIDI
- The UF2 Bootloader only needs to be installed once
- These instructions can also be used if the board software overwritten (e.g. by installing Arduino)
- [Factory reset and bootloader repair](https://learn.adafruit.com/esp32-s3-reverse-tft-feather/factory-reset#factory-reset-and-bootloader-repair-3107941)

UF2 Bootloader
- Low level code that allows loading UF2 binaries

CircuitPython UF2
- Binary machine code that iruns the python interpreter and includes basic libraries

CIRCUITPY/Code.py
- Our main script run by the CircuitPython system at startup

[CircuitPython installer page for ESP32-S3 Reverse TFT Feather](https://circuitpython.org/board/adafruit_feather_esp32s3_reverse_tft/)
<img width="2812" height="1058" alt="Screenshot 2026-02-09 at 4 38 52 PM" src="https://github.com/user-attachments/assets/ef902d6d-dcd7-43b7-8258-c6740a824f61" />
Select "Open Installer"


<img width="1288" height="876" alt="Screenshot 2026-02-09 at 4 39 16 PM" src="https://github.com/user-attachments/assets/e731e78b-ef15-410c-8953-61f237941d2b" />
Hold D0 and click Reset to enter the lowest level reprogramming mode. The board will *not* show up as a USB drive but rather as a serial port


<img width="920" height="520" alt="Screenshot 2026-02-09 at 4 39 05 PM" src="https://github.com/user-attachments/assets/c86147e6-1f79-4b79-a17c-bf65504d43ad" />
Select the full install to install both the bootloader and the CircuitPython 10.x UF2 software binary


<img width="902" height="902" alt="Screenshot 2026-02-09 at 4 39 56 PM" src="https://github.com/user-attachments/assets/55f1ddc1-2bf5-4fe5-afa8-780b4b913567" />
Find the USB JTAG serial port


<img width="1096" height="364" alt="Screenshot 2026-02-09 at 4 57 51 PM" src="https://github.com/user-attachments/assets/9aea240b-52da-4768-9cf2-4171c42647e1" />


<img width="676" height="458" alt="Screenshot 2026-02-09 at 4 57 59 PM" src="https://github.com/user-attachments/assets/d1ac2a84-c333-458d-aefa-40bce8da66c4" />


<img width="1052" height="482" alt="Screenshot 2026-02-09 at 4 58 11 PM" src="https://github.com/user-attachments/assets/5f6d5d1b-b247-404e-b76c-acf8590249fa" />


<img width="1280" height="540" alt="Screenshot 2026-02-09 at 4 41 55 PM" src="https://github.com/user-attachments/assets/e8c90cbe-66f0-459e-bf62-8b4fbda60911" />
Once the bootloader is flashed press reset on the board. You should see a FTHRS3BOOT virtual drive appear. You can physically unplug and reconnect if having issues.


<img width="452" height="128" alt="Screenshot 2026-02-09 at 4 50 27 PM" src="https://github.com/user-attachments/assets/704d91db-40e4-4032-898a-a8ea26578b49" />


<img width="1280" height="540" alt="Screenshot 2026-02-09 at 4 41 55 PM" src="https://github.com/user-attachments/assets/caae4f5d-d46a-4cad-9799-06aace4a536f" />


<img width="1286" height="442" alt="Screenshot 2026-02-09 at 4 47 47 PM" src="https://github.com/user-attachments/assets/0e2cefb1-50bc-43cd-91a0-78eea1e6e681" />


<img width="428" height="128" alt="Screenshot 2026-02-09 at 4 48 15 PM" src="https://github.com/user-attachments/assets/a6a7a54f-01c6-4394-b904-4dbf1fc496ed" />
Hit reset and you should see the CIRCUITPY drive appear


<img width="428" height="128" alt="Screenshot 2026-02-09 at 4 48 15 PM" src="https://github.com/user-attachments/assets/799c0319-1129-46ff-b378-d1923f0748b6" />


<img width="1356" height="748" alt="Screenshot 2026-02-09 at 4 48 50 PM" src="https://github.com/user-attachments/assets/b3218f07-ad75-40b6-97d3-1750c172fb79" />
Verify that CircuitPython 10.x is installed by viewing CIRCUITPY/boot_out.txt
