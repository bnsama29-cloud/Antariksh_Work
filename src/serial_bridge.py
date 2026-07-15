"""
serial_bridge.py
Owner: Hardware Integration Team
Purpose: Reads live CSV-formatted data from the Arduino serial port and logs it to a file.
Usage: python serial_bridge.py COM3
"""

import serial
import time
import sys
import csv

def main():
    if len(sys.argv) < 2:
        print("Usage: python serial_bridge.py <PORT>")
        print("Example: python serial_bridge.py COM3")
        sys.exit(1)

    port = sys.argv[1]
    baud_rate = 9600
    log_file = "data/live_telemetry.csv"

    try:
        ser = serial.Serial(port, baud_rate, timeout=1)
        print(f"Connected to {port} at {baud_rate} baud.")
    except serial.SerialException as e:
        print(f"Error opening serial port {port}: {e}")
        sys.exit(1)

    print(f"Logging data to {log_file}. Press Ctrl+C to stop.")

    with open(log_file, "a", newline='') as f:
        writer = csv.writer(f)
        
        try:
            while True:
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8').strip()
                    if line:
                        print(f"Rx: {line}")
                        writer.writerow(line.split(","))
                        f.flush()
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nLogging stopped by user.")
        finally:
            ser.close()
            print("Serial port closed.")

if __name__ == "__main__":
    main()
