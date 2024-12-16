import socket
import struct

# Constants
IP_HEADER_SIZE = 20  # Standard IPv4 header size (in bytes)

# Helper function to fragment the packet
def fragment_packet(data, mtu, df_flag=0):
    fragments = []
    packet_id = 12345  # Unique identifier for this packet
    total_len = len(data)
    
    # The first fragment is an IP header + data
    offset = 0
    while offset < total_len:
        # Calculate the size of the current fragment
        remaining_data = total_len - offset
        current_fragment_size = min(mtu, remaining_data + IP_HEADER_SIZE)
        
        # Set the "More Fragments" flag except for the last fragment
        more_fragments = 0 if offset + current_fragment_size >= total_len else 1
        
        # Calculate the offset in the original packet
        fragment_offset = offset // 8  # Offset is in 8-byte units
        
        # Create the IP header for this fragment
        fragment_header = struct.pack('!BBHHHBBH4s4s', 69, df_flag, current_fragment_size, packet_id, fragment_offset, more_fragments, 0, 0, b'0.0.0.0', b'0.0.0.0')
        
        # Create the fragment (just combine the header and the data)
        fragment_data = fragment_header + data[offset:offset + mtu - IP_HEADER_SIZE]
        fragments.append(fragment_data)
        
        # Print the details about the fragment
        print(f"Fragment ID: {packet_id}, Offset: {fragment_offset}, More Fragments: {more_fragments}, Do Not Fragment: {df_flag}, Fragment Size: {len(fragment_data)} bytes")
        
        # Move the offset for the next fragment
        offset += mtu - IP_HEADER_SIZE
    
    return fragments

# Function to send data
def send_packet(packet, host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(packet, (host, port))
    sock.close()

def main():
    while True:
        mtu = int(input('Enter MTU size: '))  # Prompt for MTU size
        df_flag_input = input("Do you want to set 'Do Not Fragment' flag (DF)? (y/n): ")
        df_flag = 1 if df_flag_input.lower() == 'y' else 0
        
        host = "127.0.0.1"
        port = 12345
        message = b"Some piece of text that is transmitted over the network. This is repeated ten times!" * 10  # Simulate a large message
        
        fragments = fragment_packet(message, mtu, df_flag)
        
        for fragment in fragments:
            send_packet(fragment, host, port)
            print(f"Sent fragment with size {len(fragment)} bytes")

        # Ask the user if they want to try again with a different MTU size
        again = input('Do you want to try again with a different MTU size? (y/n): ')
        if again.lower() != 'y':
            break
        
if __name__ == "__main__":
    main()

#700
#y
#y
#350
#y
#n


