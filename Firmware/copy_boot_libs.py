#!/bin/bash

# List of files and/or directories to copy (space-separated)
files="boot.py lib/adafruit_ble lib/adafruit_ble_midi.mpy lib/adafruit_midi"

# Source and target directories
src_dir="../CircuitPython"
tgt_dir="/Volumes/CIRCUITPY"

# Check if target directory exists
if [ ! -d "$tgt_dir" ]; then
    echo "Error: Target directory '$tgt_dir' not found."
    exit 1
fi

# Copy each file or directory from source to target
for item in $files; do
    src_item="$src_dir/$item"
    if [ -e "$src_item" ]; then
        echo "Copying $item to $tgt_dir"
        cp -r "$src_item" "$tgt_dir/"
    else
        echo "Warning: $src_item does not exist and will be skipped."
    fi
done

echo "Hard reset board to enable MIDI"
