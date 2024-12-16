import socket

def request_file(filename, host='127.0.0.1', port=65432):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    client_socket.sendall(filename.encode())
    response = client_socket.recv(4096).decode()

    print(f"Response from server:\n{response}")
    client_socket.close()

if __name__ == "__main__":
    host = '127.0.0.1'  # Server address
    port = 65432        # Server port

    while True:
        filename = input("Enter the filename to request (or type 'exit' to quit): ") 
        if filename.lower() == 'exit':
            print("Exiting client.")
            break
        
        request_file(filename, host, port)
