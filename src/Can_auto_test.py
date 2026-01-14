# can_auto_test.py
# Automated CAN test:
# - Reads distance from Serial (e.g., Arduino sending raw ultrasound timings or cm values)
# - Sends the distance over CAN (first two bytes, big-endian)
# - Listens for a response and validates the echoed distance
# - Tracks cycles, errors, missed responses and prints a summary

import time
import canalystii
import serial


def read_distance_from_serial(ser: serial.Serial, mode: str) -> int | None:
    """
    Reads one line from serial and returns distance in cm (int).
    mode:
      - "cm": Arduino already sends cm as a number per line
      - "us": Arduino sends microseconds; we convert using us // 58
    """
    try:
        line = ser.readline().decode(errors="ignore").strip()
        if not line:
            return None
        if not line.isdigit():
            return None

        val = int(line)
        if mode == "us":
            return val // 58
        return val  # mode == "cm"

    except Exception:
        return None


def encode_distance_payload(distance_cm: int) -> tuple[int, int, int, int, int, int, int, int]:
    """
    Encode distance into first two bytes (big-endian), pad rest with zeros.
    distance is clamped to 0..65535
    """
    distance_cm = max(0, min(distance_cm, 65535))
    high = (distance_cm >> 8) & 0xFF
    low = distance_cm & 0xFF
    return (high, low, 0, 0, 0, 0, 0, 0)


def decode_distance_payload(data_bytes) -> int:
    """Decode first two bytes as big-endian distance."""
    data = list(data_bytes)
    return (data[0] << 8) | data[1]


def main():
    # --- Adjust these to your setup ---
    bitrate = 500000
    tx_channel = 1
    rx_channel = 0

    serial_port = "COM6"     # change to your port (e.g. COM6 on Windows, /dev/ttyUSB0 on Linux/macOS)
    serial_baud = 9600
    serial_mode = "cm"       # "cm" if Arduino prints cm; "us" if it prints microseconds
    timeout_s = 1

    can_id = 0x3FE
    total_cycles = 100
    response_wait_s = 0.20   # how long to wait for a reply frame

    # -------------------------------

    ser = serial.Serial(serial_port, serial_baud, timeout=timeout_s)
    dev = canalystii.CanalystDevice(bitrate=bitrate)

    cycles = 0
    errors = 0
    missed = 0

    try:
        print("[INFO] Starting automated CAN test...")
        print(f"[INFO] Serial: {serial_port} @ {serial_baud} ({serial_mode})")
        print(f"[INFO] CAN: bitrate={bitrate}, TX={tx_channel}, RX={rx_channel}, CAN_ID=0x{can_id:X}")
        print(f"[INFO] Cycles: {total_cycles}\n")

        # Clear buffer once
        for _ in dev.receive(rx_channel):
            pass

        while cycles < total_cycles:
            distance = read_distance_from_serial(ser, serial_mode)
            if distance is None:
                continue

            payload = encode_distance_payload(distance)

            msg = canalystii.Message(
                can_id=can_id,
                remote=False,
                extended=False,
                data_len=8,
                data=payload,
            )

            # Send one frame
            dev.send(tx_channel, msg)

            # Wait for matching response
            start = time.perf_counter()
            received_ok = False

            while (time.perf_counter() - start) < response_wait_s:
                rx_msgs = dev.receive(rx_channel)
                if not rx_msgs:
                    time.sleep(0.01)
                    continue

                for rx in rx_msgs:
                    if rx.can_id != can_id:
                        continue  # ignore other IDs on a shared bus

                    rx_dist = decode_distance_payload(rx.data)

                    if rx_dist != max(0, min(distance, 65535)):
                        errors += 1
                        print(f"[Cycle {cycles+1}] ERROR: Sent {distance} cm, Received {rx_dist} cm, Raw={list(rx.data)}")
                    else:
                        print(f"[Cycle {cycles+1}] OK: Sent {distance} cm, Received {rx_dist} cm, Raw={list(rx.data)}")

                    received_ok = True
                    break

                if received_ok:
                    break

            cycles += 1

            if not received_ok:
                missed += 1
                print(f"[Cycle {cycles}] NO RESPONSE (timeout)")

            # small pacing delay (keeps output readable + reduces bus spam)
            time.sleep(0.05)

        print("\n--- Test Summary ---")
        print(f"Total messages sent         : {total_cycles}")
        print(f"Successful transmissions    : {total_cycles - errors - missed}")
        print(f"Transmission errors         : {errors}")
        print(f"Messages lost (no reply)    : {missed}")
        print("---------------------")

    except KeyboardInterrupt:
        print("\n[STOP] Manual stop requested.")

    finally:
        dev.stop(0)
        dev.stop(1)
        del dev
        ser.close()


if __name__ == "__main__":
    main()
