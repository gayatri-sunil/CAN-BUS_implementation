# CAN Bus Hands-On Lab

Hands-on laboratory project for the course **IE6-BUL – Bus Systems** (Summer Semester 2025).

This project explores Controller Area Network (CAN) communication through practical experiments involving message transmission, physical layer analysis, sensor data exchange, and automated error detection. Automated test requires a serial source (e.g., microcontroller output) and a CAN node that echoes frames for verification.

## Objectives
- Configure and test CAN communication using USB-CAN hardware
- Transmit and receive CAN messages using Python
- Analyze CAN physical layer signals at different bitrates
- Validate data integrity and detect transmission errors
- Integrate multiple nodes into a shared CAN network

## Technical setup
- CAN interface: Canalyst-II USB-CAN
- Programming language: Python
- Bitrates tested: 500 kbps and 250 kbps
- Sensor data transmitted over CAN frames
- Oscilloscope-based physical layer analysis (CANH / CANL)

## Experiments
- CAN interface initialization and loopback testing
- Message transmission with different payloads and CAN IDs
- Physical layer signal comparison for different bitrates
- Sensor data transmission and verification
- Automated error detection and consistency checks
- Multi-node CAN network communication

## Results
- Reliable transmission and reception of CAN frames
- Clear physical-layer differences between 500 kbps and 250 kbps
- Zero transmission errors during automated testing
- Successful integration into a shared CAN network with multiple groups

## What I learned
- Practical CAN bus configuration and debugging
- Importance of bitrate consistency and termination resistors
- CAN frame structure, payload encoding, and ID filtering
- Physical layer behavior of CAN networks
- Automated testing and validation of bus communication

## Notes
- Educational laboratory project
- Focus on practical bus systems engineering and analysis
