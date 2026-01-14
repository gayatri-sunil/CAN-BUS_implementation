# -*- coding: utf-8 -*-

# pip install canalystii
# pip install "python-can[canalystii]"
# not sure, if both are required

import canalystii

# Connect to the Canalyst-II device
# Passing a bitrate to the constructor causes both channels to be initialized and started.
dev = canalystii.CanalystDevice(bitrate=500000)

# Receive all pending messages on channel 0
while True:
    msg=dev.receive(0)
    if msg: print(msg)

# The canalystii.Message class is a ctypes Structure, to minimize overhead

#for value in range(255):
#    pl=(value, value, value, value, value, value, value, value)
#    new_message = canalystii.Message(can_id=0x3FE,
#                                 remote=False,
#                                 extended=True,
#                                 data_len=8,
#                                 data=pl)
#     # Send one copy to channel 1
#    dev.send(1, new_message)

for msg in dev.receive(0):
     print(msg)


