#!/usr/bin/env python3
"""Forward MIDI from one port to another.

Usage:
  python midi_forward.py --list
  python midi_forward.py <a_substring> <b_substring> [--monitor] [--bidirectional]

Example (CircuitPython controller → iPad over BLE MIDI on macOS):
  1. On the iPad, open a MIDI app that advertises BLE (e.g. AUM, MIDI Wrench).
  2. On the Mac, open Audio MIDI Setup → Window → Show MIDI Studio →
     double-click "Bluetooth" and connect to the advertising iPad.
  3. Plug in the CircuitPython device over USB.
  4. List ports to confirm names:
         python midi_forward.py --list
  5. Forward, matching on substrings of the port names:
         python midi_forward.py CircuitPython iPad --monitor
     Add --bidirectional (or -b) to also route iPad → CircuitPython.
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


def print_ports():
    print("Inputs:")
    for n in mido.get_input_names():
        print(f"  {n}")
    print("\nOutputs:")
    for n in mido.get_output_names():
        print(f"  {n}")


def make_callback(out, label, monitor):
    def _cb(msg):
        out.send(msg)
        if monitor:
            print(f"[{label}] {msg}")
    return _cb


def main():
    args = sys.argv[1:]

    if not args:
        print(__doc__)
        print_ports()
        return

    if args[0] in ('-l', '--list'):
        print_ports()
        return

    if args[0] in ('-h', '--help'):
        print(__doc__)
        return

    flags = {'--monitor', '-m', '--bidirectional', '-b'}
    positional = [a for a in args if a not in flags]
    if len(positional) < 2:
        raise SystemExit(
            "Usage: midi_forward.py <a> <b> [--monitor] [--bidirectional]"
        )

    monitor = '--monitor' in args or '-m' in args
    bidirectional = '--bidirectional' in args or '-b' in args

    a_in = find_port(mido.get_input_names(), positional[0])
    b_out = find_port(mido.get_output_names(), positional[1])

    arrow = '↔' if bidirectional else '→'
    print(f"Forwarding:  {a_in}  {arrow}  {b_out}")
    if monitor:
        print("Monitor on. Ctrl+C to quit.\n")

    if not bidirectional:
        with mido.open_input(a_in) as inp, mido.open_output(b_out) as out:
            try:
                for msg in inp:
                    out.send(msg)
                    if monitor:
                        print(msg)
            except KeyboardInterrupt:
                print("\nStopped.")
        return

    # Bidirectional: need the reverse pair too.
    b_in = find_port(mido.get_input_names(), positional[1])
    a_out = find_port(mido.get_output_names(), positional[0])

    inp_a = mido.open_input(a_in)
    inp_b = mido.open_input(b_in)
    out_a = mido.open_output(a_out)
    out_b = mido.open_output(b_out)

    inp_a.callback = make_callback(out_b, f"{positional[0]}→{positional[1]}", monitor)
    inp_b.callback = make_callback(out_a, f"{positional[1]}→{positional[0]}", monitor)

    try:
        import time
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        for p in (inp_a, inp_b, out_a, out_b):
            p.close()


if __name__ == '__main__':
    main()