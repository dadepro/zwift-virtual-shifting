"""
Debug Click Controllers
Test script to see what data the Zwift Click controllers are sending
"""

import asyncio
from bleak import BleakClient, BleakScanner


async def debug_click():
    """Connect to Click and show all characteristics and data"""
    print("Scanning for Zwift Click controllers...")

    devices = await BleakScanner.discover(timeout=10.0)

    # Find first Zwift Click
    click_device = None
    for device in devices:
        if device.name and "zwift click" in device.name.lower():
            click_device = device
            print(f"\n✓ Found: {device.name} ({device.address})")
            break

    if not click_device:
        print("❌ No Zwift Click found")
        return

    # Connect
    print("\nConnecting...")
    async with BleakClient(click_device.address) as client:
        print(f"✓ Connected to {click_device.name}\n")

        # List all services and characteristics
        print("=" * 60)
        print("SERVICES AND CHARACTERISTICS:")
        print("=" * 60)

        for service in client.services:
            print(f"\n📦 Service: {service.uuid}")
            print(f"   Description: {service.description}")

            for char in service.characteristics:
                print(f"\n   📌 Characteristic: {char.uuid}")
                print(f"      Properties: {', '.join(char.properties)}")
                print(f"      Description: {char.description}")

                # Try to read if readable
                if "read" in char.properties:
                    try:
                        value = await client.read_gatt_char(char.uuid)
                        print(f"      Value: {value.hex()}")
                    except Exception as e:
                        print(f"      Read error: {e}")

        print("\n" + "=" * 60)
        print("MONITORING BUTTON PRESSES")
        print("=" * 60)
        print("\nPress buttons on your Click controllers...")
        print("Watching for notifications...\n")

        # Function to handle any notification
        def notification_handler(sender, data):
            print(f"📨 Notification from {sender}:")
            print(f"   Raw bytes: {data.hex()}")
            print(f"   As integers: {[b for b in data]}")
            print(f"   Length: {len(data)} bytes")
            print()

        # Subscribe to ALL characteristics that support notify
        notify_chars = []
        for service in client.services:
            for char in service.characteristics:
                if "notify" in char.properties:
                    try:
                        await client.start_notify(char.uuid, notification_handler)
                        notify_chars.append(char.uuid)
                        print(f"✓ Subscribed to {char.uuid}")
                    except Exception as e:
                        print(f"✗ Failed to subscribe to {char.uuid}: {e}")

        print(f"\n✓ Monitoring {len(notify_chars)} notification characteristics")
        print("Press Ctrl+C to stop\n")

        # Keep running and listening
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\n\n✓ Stopping...")


if __name__ == "__main__":
    print("\nZwift Click Debug Tool\n")
    asyncio.run(debug_click())
