import argparse
import socket
import sys
import threading
import time

def scan_port(target_host, port):
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set timeout to 1 second
        sock.settimeout(1)
        # Try to connect to the target host and port
        result = sock.connect_ex((target_host, port))
        if result == 0:
            print(f"Port {port} is open")
        # Close the socket
        sock.close()
    except socket.error:
        pass

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Simple port scanner')
    parser.add_argument('target', help='IP address or DNS address of the target')
    parser.add_argument('start_port', type=int, help='Start of port range to scan')
    parser.add_argument('end_port', type=int, help='End of port range to scan')
    args = parser.parse_args()

    # Resolve target to IP address if it's a DNS address
    try:
        target_ip = socket.gethostbyname(args.target)
    except socket.gaierror as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Start timer for total scan time
    start_time = time.time()
    
    # Perform port scanning
    print(f"Scanning target {args.target} ({target_ip})...")
    threads = []
    for port in range(args.start_port, args.end_port + 1):
        # Create a thread for each port scan to speed up the process
        thread = threading.Thread(target=scan_port, args=(target_ip, port))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Print total scan time
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Scan completed in {total_time:.2f} seconds")

if __name__ == "__main__":
    main()
