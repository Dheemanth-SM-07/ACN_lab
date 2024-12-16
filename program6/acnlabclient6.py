import socket
import struct
import logging

def string_to_binary(string):
    # Convert the string to binary representation
    return ''.join(format(ord(char), '08b') for char in string)

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
    return checksum, step_by_step

def send_icmp_packet(target_ip, word):
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    # Convert the word to binary and then bytes
    binary_representation = string_to_binary(word)
    payload = bytearray(int(binary_representation[i:i+8], 2) for i in range(0, len(binary_representation), 8))

    # Log the binary representation
    logging.info(f"Input Word: {word}")
    logging.info(f"Binary Representation: {binary_representation}")

    # ICMP Header
    icmp_type = 8  # Echo Request
    icmp_code = 0
    identifier = 1
    sequence = 9  # Match the example
    header = struct.pack(">BBHHH", icmp_type, icmp_code, 0, identifier, sequence)

    # Calculate checksum for the full ICMP packet (header + payload)
    checksum, steps = calculate_checksum(header + payload)
    for step in steps:
        logging.info(f"{step[0]} -> {step[1]}")

    # Include the calculated checksum in the header
    icmp_packet = struct.pack(">BBHHH", icmp_type, icmp_code, checksum, identifier, sequence) + payload

    # Log the sum and checksum to match the image example
    logging.info(f"Sum = {steps[-1][1]}")
    logging.info(f"Checksum = {checksum:016b}")

    # Send the ICMP packet
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    sock.sendto(icmp_packet, (target_ip, 1))
    logging.info(f"Packet sent to {target_ip}. Final Checksum: {checksum:016b}")

# Input from the user
if __name__ == "__main__":
    target_ip = input("Enter target IP: ")
    word = input("Enter the word to send (e.g., TEST): ")
    send_icmp_packet(target_ip, word)
