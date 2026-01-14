# can_test.py
# Sends 250 CAN frames via Canalyst-II using the canalystii Python library.
# Intended for IE6-BUL Bus Systems lab (CAN Bus Hands-On).

import time
import canalystii


def clear_rx_buffer(dev: canalystii.CanalystDevice, rx_channel: int) -> None:
    """Drain and print any pending RX frames (optional, helps in lab)."""
    for msg in dev.receive(rx_channel):
        print(msg)


def main():
    bitrate = 500000
    tx_channel = 1
    rx_channel = 1  # if you have loopback or another node echoing, you can observe here

    dev = canalystii.CanalystDevice(bitrate=bitrate)

    try:
        print(f"[INFO] Connected. Bitrate={bitrate}, TX={tx_channel}, RX={rx_channel}")
        print("[INFO] Clearing RX buffer...")
        clear_rx_buffer(dev, rx_channel)

        print("[INFO] Sending 250 frames...")
        for value in range(250):
            payload = (value, value, value, value, value, value, value, value)
            msg = canalystii.Message(
                can_id=0x3FE,
                remote=False,
                extended=False,
                data_len=8,
                data=payload,
            )
            dev.send(tx_channel, msg)

        # small pause to allow bus traffic to settle
        time.sleep(0.1)

        print("[INFO] Reading RX after send...")
        clear_rx_buffer(dev, rx_channel)

        print("[DONE] can_test completed.")

    finally:
        dev.stop(0)
        dev.stop(1)
        del dev


if __name__ == "__main__":
    main()
