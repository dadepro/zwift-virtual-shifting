"""
Zwift Click Test - Verbose Debug Mode
Shows exactly what's happening with button notifications
"""

import asyncio
from bleak import BleakClient, BleakScanner

try:
    import blackboxprotobuf
except ImportError:
    print("Installing blackboxprotobuf...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "blackboxprotobuf"])
    import blackboxprotobuf

import json

# Zwift Click UUIDs
ZWIFT_ASYNC_CHARACTERISTIC_UUID = "00000002-19ca-4651-86e5-fa29dcdd09d1"


async def test_click_verbose():
    """Connect and show verbose button data"""
    print("Scanning for Zwift Click...")

    devices = await BleakScanner.discover(timeout=10.0)

    click_device = None
    for device in devices:
        if device.name and "zwift click" in device.name.lower():
            click_device = device
            print(f"✓ Found {device.name}")
            break

    if not click_device:
        print("❌ No Click found")
        return

    print("\nConnecting...")

    async with BleakClient(click_device.address) as client:
        print(f"✓ Connected\n")

        notification_count = 0

        def verbose_handler(sender, data: bytearray):
            nonlocal notification_count
            notification_count += 1

            print("=" * 60)
            print(f"NOTIFICATION #{notification_count}")
            print("=" * 60)
            print(f"Sender: {sender}")
            print(f"Raw hex: {data.hex()}")
            print(f"Raw bytes: {[b for b in data]}")
            print(f"Length: {len(data)}")
            print()

            # Try to decode as protobuf
            try:
                message, typedef = blackboxprotobuf.protobuf_to_json(bytes(data))
                print("✓ Protobuf decoded successfully!")
                print(f"Message: {message}")
                print(f"Typedef: {typedef}")

                # Parse JSON
                decoded = json.loads(message)
                print(f"Parsed JSON: {decoded}")

                # Check for button keys
                if '1' in decoded:
                    print(f"  → Button 1 (UP): {decoded['1']} ({'PRESSED' if decoded['1'] == 0 else 'RELEASED'})")
                if '2' in decoded:
                    print(f"  → Button 2 (DOWN): {decoded['2']} ({'PRESSED' if decoded['2'] == 0 else 'RELEASED'})")

            except Exception as e:
                print(f"✗ Protobuf decode failed: {e}")
                print(f"Error type: {type(e).__name__}")

                # Try simple parsing
                print("\nTrying simple byte analysis:")
                for i, byte in enumerate(data):
                    print(f"  Byte {i}: {byte} (0x{byte:02x}) = {chr(byte) if 32 <= byte < 127 else '?'}")

            print()

        # Subscribe to button notifications
        print("Subscribing to button characteristic...")
        await client.start_notify(ZWIFT_ASYNC_CHARACTERISTIC_UUID, verbose_handler)
        print(f"✓ Subscribed to {ZWIFT_ASYNC_CHARACTERISTIC_UUID}\n")

        print("=" * 60)
        print("READY - Press Click buttons now!")
        print("=" * 60)
        print("Watching for notifications...")
        print("Press Ctrl+C to stop\n")

        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print(f"\n\n✓ Received {notification_count} notifications total")


if __name__ == "__main__":
    print("\nZwift Click - Verbose Debug\n")
    asyncio.run(test_click_verbose())
