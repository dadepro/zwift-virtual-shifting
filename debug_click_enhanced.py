"""
Enhanced Click Debug - Test Reading and Writing
Try different approaches to detect button presses
"""

import asyncio
from bleak import BleakClient, BleakScanner
import struct


# Wahoo Click custom UUIDs we found
WAHOO_CHAR_0002 = "00000002-19ca-4651-86e5-fa29dcdd09d1"
WAHOO_CHAR_0100 = "00000100-19ca-4651-86e5-fa29dcdd09d1"
WAHOO_CHAR_0101 = "00000101-19ca-4651-86e5-fa29dcdd09d1"
WAHOO_CHAR_0102 = "00000102-19ca-4651-86e5-fa29dcdd09d1"


async def test_click_reading():
    """Test reading from Click characteristics"""
    print("Scanning for Zwift Click...")

    devices = await BleakScanner.discover(timeout=10.0)

    click_device = None
    for device in devices:
        if device.name and "zwift click" in device.name.lower():
            click_device = device
            break

    if not click_device:
        print("❌ No Click found")
        return

    print(f"✓ Found {click_device.name}\n")

    async with BleakClient(click_device.address) as client:
        print(f"✓ Connected\n")

        # Test reading from Wahoo characteristics
        wahoo_chars = [WAHOO_CHAR_0002, WAHOO_CHAR_0100, WAHOO_CHAR_0101, WAHOO_CHAR_0102]

        print("=" * 60)
        print("TESTING WAHOO CHARACTERISTICS")
        print("=" * 60)

        for char_uuid in wahoo_chars:
            print(f"\n📌 Testing {char_uuid}")

            try:
                # Try reading
                value = await client.read_gatt_char(char_uuid)
                print(f"   ✓ Read: {value.hex()} = {[b for b in value]}")
            except Exception as e:
                print(f"   ✗ Can't read: {e}")

        print("\n" + "=" * 60)
        print("POLLING MODE - Press buttons now!")
        print("=" * 60)
        print("Repeatedly reading characteristics...")
        print("Press Ctrl+C to stop\n")

        last_values = {}

        try:
            iteration = 0
            while True:
                iteration += 1
                if iteration % 10 == 0:
                    print(f"Polling iteration {iteration}...")

                for char_uuid in wahoo_chars:
                    try:
                        value = await client.read_gatt_char(char_uuid)
                        value_bytes = bytes(value)

                        # Check if value changed
                        if char_uuid not in last_values or last_values[char_uuid] != value_bytes:
                            if char_uuid in last_values:
                                print(f"\n🔔 CHANGE DETECTED on {char_uuid}!")
                                print(f"   Old: {last_values[char_uuid].hex()} = {[b for b in last_values[char_uuid]]}")
                                print(f"   New: {value_bytes.hex()} = {[b for b in value_bytes]}")
                                print()
                            last_values[char_uuid] = value_bytes

                    except Exception:
                        pass

                await asyncio.sleep(0.1)  # Poll every 100ms

        except KeyboardInterrupt:
            print("\n✓ Stopped")


if __name__ == "__main__":
    print("\nZwift Click - Enhanced Debug\n")
    asyncio.run(test_click_reading())
