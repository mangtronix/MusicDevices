import time
import serial
import re

sender_port = 'COM13'

# 👇 Edit this line to control which types are relayed and to which ports
receiver_ports = {
    0: 'COM15',
    1: 'COM17',
    2: 'COM19'  # Comment this out to ignore type 2
}

baudrate = 115200

def open_serial(port):
    while True:
        try:
            return serial.Serial(port, baudrate, timeout=0.1)
        except serial.SerialException:
            print(f"Waiting for {port}...")
            time.sleep(1)

stable_time = 0.3  # seconds to consider input stable

# Initialize state only for used types
pending = {msg_type: {"line": None, "since": None, "last": None}
           for msg_type in receiver_ports.keys()}

def extract_type(line):
    try:
        match = re.match(rb"\[(\d+),", line)
        if match:
            return int(match.group(1))
    except Exception:
        pass
    return None

while True:
    try:
        ser_in = open_serial(sender_port)
        ser_outs = {t: open_serial(port) for t, port in receiver_ports.items()}
        print("Relay running. Press Ctrl+C to stop.")
        buffer = b""
        while True:
            try:
                data = ser_in.read(1024)
                if data:
                    buffer += data
                    while b"\n" in buffer:
                        line, buffer = buffer.split(b"\n", 1)
                        line += b"\n"
                        msg_type = extract_type(line)
                        if msg_type in pending:
                            p = pending[msg_type]
                            if line != p["line"]:
                                p["line"] = line
                                p["since"] = time.monotonic()
                            else:
                                if (p["since"] is not None and
                                    (time.monotonic() - p["since"]) >= stable_time and
                                    line != p["last"]):
                                    print(f"Relaying (stable) type {msg_type}:", line)
                                    ser_outs[msg_type].write(line)
                                    p["last"] = line
                time.sleep(0.01)
            except serial.SerialException as e:
                print("Serial error (inner loop):", e)
                break
    except serial.SerialException as e:
        print("Serial error (outer loop):", e)
        print("Attempting to reconnect...")
        try: ser_in.close()
        except: pass
        for s in ser_outs.values():
            try: s.close()
            except: pass
        time.sleep(20)
