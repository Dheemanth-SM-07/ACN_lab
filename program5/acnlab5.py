import socket
import struct
from collections import defaultdict

# Constants
MTU = 500  # The MTU of the link (for example, 500 bytes)
IP_HEADER_SIZE = 20  # Standard IPv4 header size (in bytes)

# Function to reassemble fragments
def reassemble_packet(fragments):
    fragments_dict = defaultdict(list)
    
    for fragment in fragments:
        # Extract the IP header
        ip_header = fragment[:IP_HEADER_SIZE]
        _, df_flag, _, packet_id, offset, more_fragments, _, _, _, _ = struct.unpack('!BBHHHBBH4s4s', ip_header)
        
        # Append the fragment's data to the corresponding list of fragments by packet_id
        fragments_dict[packet_id].append((offset, more_fragments, fragment[IP_HEADER_SIZE:]))
        
        # Print the details about the fragment
        print(f"Received Fragment ID: {packet_id}, Offset: {offset}, More Fragments: {more_fragments}, Do Not Fragment: {df_flag}, Fragment Size: {len(fragment[IP_HEADER_SIZE:])} bytes")
    
    # Reassemble the packet
    for packet_id, fragment_data in fragments_dict.items():
        # Sort by offset
        fragment_data.sort(key=lambda x: x[0])
        
        reassembled_data = b''.join(f[2] for f in fragment_data)
        print(f"Reassembled packet {packet_id} of size {len(reassembled_data)} bytes")
        return reassembled_data

# Function to receive and process packets
def receive_packet(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    
    print(f"Listening on {host}:{port}...")
    
    while True:
        fragments = []
        
        while True:
            data, addr = sock.recvfrom(MTU)
            fragments.append(data)
            
            # Check if the last fragment (based on the "More Fragments" flag) has been received
            ip_header = data[:IP_HEADER_SIZE]
            _, _, _, packet_id, _, more_fragments, _, _, _, _ = struct.unpack('!BBHHHBBH4s4s', ip_header)
            
            # Print fragment info for each received fragment
            print(f"Received Fragment ID: {packet_id}, Offset: {packet_id // 8}, More Fragments: {more_fragments}, Fragment Size: {len(data)} bytes")
            
            # If it's the last fragment, reassemble and break the loop
            if more_fragments == 0:
                print(f"Received last fragment for packet {packet_id}")
                reassembled_data = reassemble_packet(fragments)
                print(f"Reassembled packet from {addr}:\n{reassembled_data}")
                break
        
        # You can add any additional code to process reassembled packets here.
        # The loop will continue to listen for new packets after each reassembly.

def main():
    host = "127.0.0.1"
    port = 12345
    receive_packet(host, port)

if __name__ == "__main__":
    main()

