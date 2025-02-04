import usb_hid, usb_midi

# On some boards, we need to give up HID to free up a resource for MIDI.
print("Enabling MIDI")
usb_hid.disable()
usb_midi.enable()