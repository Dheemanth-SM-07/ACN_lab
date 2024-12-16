import socket

def calculate_checksum(segments):
    checksum = 0
    for segment in segments:
        # Convert segment to an integer
        value = int(segment, 16)
        checksum += value

        # Handle overflow by adding the carry bit
        checksum = (checksum & 0xFFFF) + (checksum >> 16)

    # One's complement of the final checksum
    checksum = ~checksum & 0xFFFF
    return checksum

def main():
    # Server setup
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 65432))
    server_socket.listen(1)
    print("Server is listening...")

    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

    # Receive data from the client
    data = conn.recv(1024).decode()
    if data:
        # Split the data into segments
        segments = data.split()
        checksum = calculate_checksum(segments)
        checksum_hex = f"0x{checksum:04X}"
        print("Checksum: ", checksum_hex)

        # Send the checksum back to the client
        conn.sendall(checksum_hex.encode())

    # Close the connection
    conn.close()

if __name__ == "__main__":
    main()

