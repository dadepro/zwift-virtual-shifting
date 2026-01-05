"""
Zwift Click Listener
Handles communication with Zwift Click controllers via Bluetooth LE
"""

import asyncio
from bleak import BleakClient, BleakScanner
from typing import Optional, Callable
import struct

# Bluetooth UUIDs for Zwift Click
# These are standard button/remote control UUIDs
REMOTE_CONTROL_SERVICE_UUID = "00001812-0000-1000-8000-00805f9b34fb"  # HID Service
BUTTON_CHARACTERISTIC_UUID = "00002a4d-0000-1000-8000-00805f9b34fb"   # Report

# Alternative UUIDs if Click uses custom service
ZWIFT_CLICK_SERVICE_UUID = "00001816-0000-1000-8000-00805f9b34fb"
ZWIFT_CLICK_BUTTON_UUID = "00002a5b-0000-1000-8000-00805f9b34fb"


class ClickListener:
    """Listener for Zwift Click button presses"""

    def __init__(self, device_name: str = "CLICK", on_shift_up: Callable = None, on_shift_down: Callable = None):
        self.device_name = device_name
        self.client: Optional[BleakClient] = None
        self.device = None
        self.connected = False
        self.on_shift_up = on_shift_up or (lambda: None)
        self.on_shift_down = on_shift_down or (lambda: None)

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
            print(f"Connected to {self.device.name}")

            # Try to find the correct characteristic for button presses
            # First try HID Report characteristic
            services = self.client.services

            button_char = None
            for service in services:
                for char in service.characteristics:
                    # Look for notify-capable characteristics
                    if "notify" in char.properties:
                        print(f"Found notify characteristic: {char.uuid}")
                        button_char = char.uuid
                        break
                if button_char:
                    break

            if button_char:
                # Subscribe to button notifications
                await self.client.start_notify(
                    button_char,
                    self._handle_button_press
                )
                print(f"Subscribed to button notifications on {button_char}")
            else:
                print("Warning: Could not find button characteristic")

            return True

        except Exception as e:
            print(f"Error connecting to Click: {e}")
            return False

    def _handle_button_press(self, sender, data: bytearray):
        """Handle button press notifications"""
        try:
            # Parse button data
            # The exact format depends on how Zwift Click sends data
            # Typically: button press = non-zero value, release = zero

            if len(data) > 0:
                button_value = data[0]

                # Detect shift up (right button) vs shift down (left button)
                # This may need adjustment based on actual Click behavior
                if button_value == 1:  # Shift up
                    print("↑ Shift UP")
                    asyncio.create_task(self.on_shift_up())
                elif button_value == 2:  # Shift down
                    print("↓ Shift DOWN")
                    asyncio.create_task(self.on_shift_down())

        except Exception as e:
            print(f"Error handling button press: {e}")

    async def disconnect(self):
        """Disconnect from the Click controller"""
        if self.client and self.connected:
            await self.client.disconnect()
            self.connected = False
            print("Disconnected from Click")


class DualClickListener:
    """Listener for both left and right Zwift Click controllers"""

    def __init__(self, on_shift_up: Callable = None, on_shift_down: Callable = None):
        self.left_click = ClickListener("CLICK L", on_shift_down=on_shift_down)
        self.right_click = ClickListener("CLICK R", on_shift_up=on_shift_up)
        self.on_shift_up = on_shift_up
        self.on_shift_down = on_shift_down

    async def scan_and_connect(self, timeout: int = 10) -> bool:
        """Connect to both Click controllers"""
        print("Connecting to Zwift Click controllers...")

        # Try to connect to both
        left_connected = await self.left_click.scan_and_connect(timeout)
        right_connected = await self.right_click.scan_and_connect(timeout)

        # At least one should connect
        if not left_connected and not right_connected:
            print("Could not connect to any Click controllers")
            return False

        if left_connected and right_connected:
            print("✓ Both Click controllers connected")
        elif left_connected:
            print("✓ Left Click connected (right not found)")
        else:
            print("✓ Right Click connected (left not found)")

        return True

    async def disconnect(self):
        """Disconnect from both Click controllers"""
        await self.left_click.disconnect()
        await self.right_click.disconnect()
