"""
Zwift Companion Network Monitor
Monitors network traffic between Zwift Companion app and Zwift desktop
to see what commands are sent when Clicks are pressed
"""

import socket
import struct
import threading
import time
from datetime import datetime


def get_local_ip():
    """Get the local IP address"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Connect to a public DNS server (doesn't actually send data)
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip


def listen_for_companion_broadcasts():
    """Listen for Zwift Companion broadcast packets"""
    print("=" * 70)
    print("Zwift Companion Network Monitor")
    print("=" * 70)
    print()
    print(f"Local IP: {get_local_ip()}")
    print()
    print("Listening for Zwift Companion traffic...")
    print("Make sure:")
    print("  1. Zwift is running on this computer")
    print("  2. Zwift Companion is connected on your phone")
    print("  3. Zwift Clicks are connected to Companion")
    print()
    print("Press your Click buttons and watch for network activity!")
    print("=" * 70)
    print()

    # Create UDP socket to listen for broadcasts
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind to all interfaces
    sock.bind(('', 3024))  # Zwift Companion uses port 3024

    print(f"✓ Listening on UDP port 3024 (Zwift Companion protocol)")
    print()

    packet_count = 0

    try:
        while True:
            data, addr = sock.recvfrom(4096)
            packet_count += 1

            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]

            print(f"\n[{timestamp}] Packet #{packet_count} from {addr[0]}:{addr[1]}")
            print(f"  Length: {len(data)} bytes")
            print(f"  Raw hex: {data[:100].hex()}{'...' if len(data) > 100 else ''}")

            # Try to decode as ASCII
            try:
                text = data.decode('ascii', errors='ignore')
                if text.isprintable():
                    print(f"  ASCII: {text[:200]}{'...' if len(text) > 200 else ''}")
            except:
                pass

            # Look for specific patterns
            if b'click' in data.lower() or b'button' in data.lower() or b'gear' in data.lower():
                print("  ⭐ POSSIBLE CLICK/GEAR COMMAND DETECTED!")

            if b'slope' in data.lower() or b'resistance' in data.lower():
                print("  ⭐ SLOPE/RESISTANCE COMMAND DETECTED!")

    except KeyboardInterrupt:
        print(f"\n\n✓ Captured {packet_count} packets")
    finally:
        sock.close()


def listen_for_tcp_connections():
    """Listen for TCP connections from Companion"""
    print("\nAlso listening for TCP connections on port 3025...")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 3025))
    sock.listen(5)

    print("✓ Listening on TCP port 3025")

    while True:
        try:
            conn, addr = sock.accept()
            print(f"\n🔗 TCP Connection from {addr}")

            # Read data
            data = conn.recv(4096)
            if data:
                print(f"  Data: {data.hex()}")
                print(f"  ASCII: {data.decode('ascii', errors='ignore')}")

            conn.close()
        except Exception as e:
            print(f"TCP error: {e}")


if __name__ == "__main__":
    print("\n")

    # Start UDP listener in main thread
    try:
        listen_for_companion_broadcasts()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nNote: You may need to run this with sudo on some systems:")
        print("  sudo python monitor_companion.py")
