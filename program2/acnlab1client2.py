import socket

def start_client(host='127.0.0.1', port=65432):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        message = input("Enter a message to send to the server (or type 'exit' to quit): ")
        if message.lower() == 'exit':
            print("Exiting client.")
            break
        
        # Send the message to the server
        client_socket.sendto(message.encode(), (host, port))
        
        # Receive the server's response
        response, _ = client_socket.recvfrom(4096)
        uppercase_text, char_count = response.decode().split('|')
        print(f"Server response:\nUppercase Text: {uppercase_text}\nCharacter Count: {char_count}\n")

    client_socket.close()

if __name__ == "__main__":
    start_client()
