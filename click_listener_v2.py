"""
Zwift Click Listener v2 - With Protobuf Support
Based on reverse-engineered Zwift Click protocol
Credit: @ajchellew1, @Makinolo2, @jat255
"""

import asyncio
from bleak import BleakClient, BleakScanner
from typing import Optional, Callable
import struct

try:
    import blackboxprotobuf
except ImportError:
    print("Installing blackboxprotobuf...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "blackboxprotobuf"])
    import blackboxprotobuf


# Zwift Click BLE UUIDs
ZWIFT_CUSTOM_SERVICE_UUID = "00000001-19ca-4651-86e5-fa29dcdd09d1"
ZWIFT_ASYNC_CHARACTERISTIC_UUID = "00000002-19ca-4651-86e5-fa29dcdd09d1"


class ZwiftClickListener:
    """Listener for Zwift Click button presses using protobuf protocol"""

    def __init__(self, device_name: str = "Zwift Click",
                 on_shift_up: Callable = None,
                 on_shift_down: Callable = None):
        self.device_name = device_name
        self.client: Optional[BleakClient] = None
        self.device = None
        self.connected = False
        self.on_shift_up = on_shift_up or (lambda: None)
        self.on_shift_down = on_shift_down or (lambda: None)

        # Track button states
        self.button_states = {
            '1': 1,  # Plus button (shift up) - 1 = released, 0 = pressed
            '2': 1   # Minus button (shift down) - 1 = released, 0 = pressed
        }

    async def scan_and_connect(self, timeout: int = 10) -> bool:
        """Scan for and connect to Zwift Click controller"""
        print(f"Scanning for {self.device_name}...")

        devices = await BleakScanner.discover(timeout=timeout)

        for device in devices:
            if device.name and self.device_name.lower() in device.name.lower():
                print(f"Found {device.name} ({device.address})")
                self.device = device
                break

        if not self.device:
            print(f"Could not find {self.device_name}")
            return False

        try:
            self.client = BleakClient(self.device.address)
            await self.client.connect()
            self.connected = True
            print(f"✓ Connected to {self.device.name}")

            # Subscribe to the Zwift async characteristic (button events)
            await self.client.start_notify(
                ZWIFT_ASYNC_CHARACTERISTIC_UUID,
                self._handle_notification
            )
            print(f"✓ Subscribed to button notifications")

            return True

        except Exception as e:
            print(f"Error connecting to Click: {e}")
            return False

    def _handle_notification(self, sender, data: bytearray):
        """Handle notifications from Zwift Click (protobuf encoded)"""
        try:
            # Decode protobuf message
            message, typedef = blackboxprotobuf.protobuf_to_json(bytes(data))

            # Parse button states from protobuf
            # Button '1' = shift up (plus/right)
            # Button '2' = shift down (minus/left)
            # Value 0 = pressed, 1 = released

            import json
            decoded = json.loads(message)

            # Check for button state changes
            if '1' in decoded:
                new_state = decoded['1']
                if new_state != self.button_states['1']:
                    if new_state == 0:
                        # Button pressed
                        print("→ Shift UP button pressed")
                    else:
                        # Button released - trigger shift
                        print("↑ SHIFT UP")
                        asyncio.create_task(self.on_shift_up())
                    self.button_states['1'] = new_state

            if '2' in decoded:
                new_state = decoded['2']
                if new_state != self.button_states['2']:
                    if new_state == 0:
                        # Button pressed
                        print("← Shift DOWN button pressed")
                    else:
                        # Button released - trigger shift
                        print("↓ SHIFT DOWN")
                        asyncio.create_task(self.on_shift_down())
                    self.button_states['2'] = new_state

        except Exception as e:
            # If protobuf parsing fails, show raw data for debugging
            print(f"Parse error: {e}")
            print(f"Raw data: {data.hex()}")

    async def disconnect(self):
        """Disconnect from the Click controller"""
        if self.client and self.connected:
            await self.client.disconnect()
            self.connected = False
            print("Disconnected from Click")


class DualZwiftClickListener:
    """Listener for both left and right Zwift Click controllers"""

    def __init__(self, device_name: str = "Zwift Click",
                 on_shift_up: Callable = None,
                 on_shift_down: Callable = None):
        self.device_name = device_name
        self.click_controllers = []
        self.on_shift_up = on_shift_up
        self.on_shift_down = on_shift_down

    async def scan_and_connect(self, timeout: int = 10) -> bool:
        """Connect to both Click controllers"""
        print(f"Scanning for {self.device_name} controllers...")

        devices = await BleakScanner.discover(timeout=timeout)

        # Find all Zwift Clicks
        click_devices = []
        for device in devices:
            if device.name and self.device_name.lower() in device.name.lower():
                click_devices.append(device)
                print(f"Found {device.name} ({device.address})")

        if len(click_devices) == 0:
            print(f"No {self.device_name} controllers found")
            return False

        # Connect to each Click (both will handle button presses)
        for device in click_devices:
            listener = ZwiftClickListener(
                device.name,
                on_shift_up=self.on_shift_up,
                on_shift_down=self.on_shift_down
            )

            listener.device = device
            try:
                listener.client = BleakClient(device.address)
                await listener.client.connect()
                listener.connected = True

                # Subscribe to notifications
                await listener.client.start_notify(
                    ZWIFT_ASYNC_CHARACTERISTIC_UUID,
                    listener._handle_notification
                )

                print(f"✓ Connected to {device.name}")
                self.click_controllers.append(listener)

            except Exception as e:
                print(f"Error connecting to {device.name}: {e}")

        if len(self.click_controllers) == 0:
            print("Could not connect to any Click controllers")
            return False

        print(f"\n✓ Connected to {len(self.click_controllers)} Click controller(s)")
        return True

    async def disconnect(self):
        """Disconnect from all Click controllers"""
        for listener in self.click_controllers:
            await listener.disconnect()
