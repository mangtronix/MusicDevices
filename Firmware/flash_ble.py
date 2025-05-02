#!/bin/bash

tty="$1"

if [ -z "$tty" ]; then
  echo "run with serial port argument, e.g. flash_ble.py /dev/tty.usbmodem101"
  exit 1
else
  echo "Flashinug BLE firmware to $tty"
fi

esptool.py -p $tty erase_flash
esptool.py -p $tty write_flash 0x0 esp32s3_reverse_tft_cp92_no_ota.bin

echo "Physically reset board and look for CIRCUITPY" drive
