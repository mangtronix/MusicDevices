#!/usr/bin/env python3
"""Forward MIDI from one port to another.

Usage:
  python midi_forward.py --list
  python midi_forward.py <input_substring> <output_substring> [--monitor]

Example (CircuitPython controller → iPad over BLE MIDI on macOS):
  1. On the iPad, open a MIDI app that advertises BLE (e.g. AUM, MIDI Wrench).
  2. On the Mac, open Audio MIDI Setup → Window → Show MIDI Studio →
     double-click "Bluetooth" and connect to the advertising iPad.
  3. Plug in the CircuitPython device over USB.
  4. List ports to confirm names:
         python midi_forward.py --list
  5. Forward, matching on substrings of the port names:
         python midi_forward.py CircuitPython iPad --monitor
"""
import sys

INSTALL_INSTRUCTIONS = """\
Missing dependency. Install with:

    pip install mido python-rtmidi

If you're on macOS and python-rtmidi fails to build, you may need:

    xcode-select --install
"""

try:
    import mido
except ImportError:
    sys.exit(INSTALL_INSTRUCTIONS)


def find_port(names, substring):
    matches = [n for n in names if substring.lower() in n.lower()]
    if not matches:
        raise SystemExit(f"No port matching {substring!r}.\nAvailable: {names}")
    if len(matches) > 1:
        print(f"Multiple matches for {substring!r}: {matches}. Using first.")
    return matches[0]


def main():
    args = sys.argv[1:]
    if not args or args[0] in ('-l', '--list'):
        print("Inputs:")
        for n in mido.get_input_names():
            print(f"  {n}")
        print("\nOutputs:")
        for n in mido.get_output_names():
            print(f"  {n}")
        return

    if len(args) < 2:
        raise SystemExit("Usage: midi_forward.py <input> <output> [--monitor]")

    in_name = find_port(mido.get_input_names(), args[0])
    out_name = find_port(mido.get_output_names(), args[1])
    monitor = '--monitor' in args or '-m' in args

    print(f"Forwarding:  {in_name}  →  {out_name}")
    if monitor:
        print("Monitor on. Ctrl+C to quit.\n")

    with mido.open_input(in_name) as inp, mido.open_output(out_name) as out:
        try:
            for msg in inp:
                out.send(msg)
                if monitor:
                    print(msg)
        except KeyboardInterrupt:
            print("\nStopped.")


if __name__ == '__main__':
    main()
