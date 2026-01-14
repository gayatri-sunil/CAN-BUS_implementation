# can_listen.py
# Continuously listens to CAN traffic and prints received frames.

import time
import canalystii


def main():
    bitrate = 500000
    rx_channel = 0

    dev = canalystii.CanalystDevice(bitrate=bitrate)

    try:
        print(f"[INFO] Listening... Bitrate={bitrate}, RX channel={rx_channel}")
        print("[INFO] Press Ctrl+C to stop.\n")

        while True:
            msgs = dev.receive(rx_channel)
            if msgs:
                # dev.receive may return a list-like iterable of frames
                for m in msgs:
                    print(m)
            else:
                # avoid busy loop
                time.sleep(0.01)

    except KeyboardInterrupt:
        print("\n[STOP] Listener stopped by user.")

    finally:
        dev.stop(0)
        dev.stop(1)
        del dev


if __name__ == "__main__":
    main()
