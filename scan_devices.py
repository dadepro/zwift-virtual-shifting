"""
Bluetooth Device Scanner
Scans for all nearby Bluetooth LE devices to help identify device names
"""

import asyncio
from bleak import BleakScanner


async def scan_devices():
    """Scan for all Bluetooth LE devices"""
    print("Scanning for Bluetooth LE devices...")
    print("Make sure your Zwift Click controllers are powered on and nearby.")
    print("=" * 60)
    print()

    devices = await BleakScanner.discover(timeout=15.0)

    if not devices:
        print("No Bluetooth devices found!")
        print("\nTroubleshooting:")
        print("1. Make sure Bluetooth is enabled on your computer")
        print("2. Check that Click controllers have batteries installed")
        print("3. Try pressing the buttons on the Clicks to wake them up")
        return

    print(f"Found {len(devices)} Bluetooth devices:\n")

    # Sort by name (rssi not always available on macOS)
    devices_sorted = sorted(devices, key=lambda d: d.name if d.name else "zzz")

    for i, device in enumerate(devices_sorted, 1):
        name = device.name if device.name else "(Unknown)"
        address = device.address

        print(f"{i}. Name: {name}")
        print(f"   Address: {address}")

        # Highlight potential Click controllers
        if device.name and any(keyword in device.name.upper() for keyword in ["CLICK", "WAHOO", "BUTTON", "REMOTE"]):
            print(f"   ⭐ POSSIBLE ZWIFT CLICK!")

        print()

    print("=" * 60)
    print("\nLook for devices named something like:")
    print("  - CLICK")
    print("  - CLICK L / CLICK R")
    print("  - Wahoo CLICK")
    print("  - Or any device with 'CLICK' in the name")
    print("\nUpdate config.json with the exact device names you see above.")


if __name__ == "__main__":
    asyncio.run(scan_devices())
