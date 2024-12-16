import socket

def start_server(host='127.0.0.1', port=65432):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    print(f"Server listening on {host}:{port}")

    while True:
        # Receive a message from the client
        message, client_address = server_socket.recvfrom(1024)
        message = message.decode()
        print(f"Received message from {client_address}: {message}")

        # Convert message to uppercase and count characters
        uppercase_message = message.upper()
        char_count = len(message)

        # Prepare the response
        response = f"{uppercase_message}|{char_count}"
        server_socket.sendto(response.encode(), client_address)

if __name__ == "__main__":
    start_server()

