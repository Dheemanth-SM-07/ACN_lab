import socket
import struct
import logging

def calculate_checksum(data):
    checksum = 0
    step_by_step = []

    # Process the data 16 bits (2 bytes) at a time
    for i in range(0, len(data), 2):
        word = (data[i] << 8) + (data[i + 1] if i + 1 < len(data) else 0)
        checksum += word
        step_by_step.append((f"{word:016b}", f"{checksum:016b}"))
        if checksum > 0xFFFF:
            checksum = (checksum & 0xFFFF) + 1

    # Finalize the checksum
    checksum = ~checksum & 0xFFFF
    step_by_step.append(("Final Sum with Carry", f"{checksum:016b}"))
    return checksum, step_by_step

def start_server():
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    logging.info("Server is now listening for incoming ICMP packets...")

    # Create raw socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

    while True:
        data, addr = sock.recvfrom(1024)
        source_ip = addr[0]
        logging.info(f"Packet received from {source_ip}")

        # Extract the ICMP header and payload
        icmp_header = data[20:28]
        payload = data[28:]

        # Extract the received checksum
        received_checksum = struct.unpack(">H", icmp_header[2:4])[0]
        logging.info(f"Received Checksum: {received_checksum:016b}")

        # Recalculate checksum
        computed_checksum, steps = calculate_checksum(icmp_header[:2] + b'\x00\x00' + icmp_header[4:] + payload)
        for step in steps:
            logging.info(f"{step[0]} -> {step[1]}")

        if computed_checksum == received_checksum:
            logging.info("Checksum validated successfully!")
        else:
            logging.info("Checksum validation failed!")

# Start the server
if __name__ == "__main__":
    start_server()

