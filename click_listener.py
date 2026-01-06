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

    def __init__(self, device_name: str = "Zwift Click", on_shift_up: Callable = None, on_shift_down: Callable = None):
        self.device_name = device_name
        self.click_controllers = []
        self.on_shift_up = on_shift_up
        self.on_shift_down = on_shift_down

    async def scan_and_connect(self, timeout: int = 10) -> bool:
        """Connect to both Click controllers (same name, different addresses)"""
        print(f"Scanning for {self.device_name} controllers...")

        devices = await BleakScanner.discover(timeout=timeout)

        # Find all devices matching the Click name
        click_devices = []
        for device in devices:
            if device.name and self.device_name.lower() in device.name.lower():
                click_devices.append(device)
                print(f"Found {device.name} ({device.address})")

        if len(click_devices) == 0:
            print(f"Could not find any {self.device_name} controllers")
            print("\nTroubleshooting:")
            print("1. Make sure Click controllers have batteries")
            print("2. Press the buttons to wake them up")
            print("3. Check they're not connected to another device")
            return False

        # Connect to the first two Click devices found
        # First one = shift down (left), Second one = shift up (right)
        for i, device in enumerate(click_devices[:2]):
            if i == 0:
                # First Click = Left (shift down)
                listener = ClickListener(device.name, on_shift_down=self.on_shift_down)
            else:
                # Second Click = Right (shift up)
                listener = ClickListener(device.name, on_shift_up=self.on_shift_up)

            listener.device = device
            try:
                listener.client = BleakClient(device.address)
                await listener.client.connect()
                listener.connected = True
                print(f"✓ Connected to {device.name} ({device.address[:8]}...)")

                # Subscribe to notifications
                services = listener.client.services
                button_char = None
                for service in services:
                    for char in service.characteristics:
                        if "notify" in char.properties:
                            button_char = char.uuid
                            break
                    if button_char:
                        break

                if button_char:
                    await listener.client.start_notify(button_char, listener._handle_button_press)
                    print(f"  ✓ Subscribed to button notifications")

                self.click_controllers.append(listener)

            except Exception as e:
                print(f"Error connecting to {device.name}: {e}")

        if len(self.click_controllers) == 0:
            print("Could not connect to any Click controllers")
            return False

        print(f"\n✓ Connected to {len(self.click_controllers)} Click controller(s)")
        if len(self.click_controllers) == 1:
            print("  Note: Only one Click found. Both shift directions will use the same button.")

        return True

    async def disconnect(self):
        """Disconnect from all Click controllers"""
        for listener in self.click_controllers:
            await listener.disconnect()
