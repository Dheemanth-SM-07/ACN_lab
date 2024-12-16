import socket
import os

def start_server(host='127.0.0.1', port=65432):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connection from {addr}")

        try:
            filename = conn.recv(1024).decode()
            print(f"Requested file: {filename}")

            if os.path.isfile(filename):
                with open(filename, 'r') as file:
                    content = file.read()
                conn.sendall(content.encode())
            else:
                conn.sendall(b"File not found.\n")
        finally:
            conn.close()

if __name__ == "__main__":
    start_server()

