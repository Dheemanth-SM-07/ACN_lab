import socket

def crc_division(data, generator):
    """ Perform CRC division and return the checksum. """
    data = data + '0' * (len(generator) - 1)
    data_len = len(data)
    generator_len = len(generator)

    data = list(data)
    generator = list(generator)

    for i in range(data_len - generator_len + 1):
        if data[i] == '1':  # Only divide if the leading bit is 1
            for j in range(generator_len):
                data[i + j] = str(int(data[i + j]) ^ int(generator[j]))

    return ''.join(data[-(generator_len - 1):])

def client():
    while True:
        message = input("Enter message (binary) or type 'exit' to quit: ")
        if message.lower() == 'exit':
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.sendto("exit,exit".encode(), ('localhost', 6000))
            print("Exiting client.")
            break

        generator = input("Enter generator (binary): ")

        checksum = crc_division(message, generator)
        print("Checksum code: ", checksum)

        # Sending data to the server
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(f"{message},{checksum}".encode(), ('localhost', 6000))

if __name__ == "__main__":
    client()


