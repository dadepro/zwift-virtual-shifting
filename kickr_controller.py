"""
Wahoo Kickr Controller
Handles communication with Wahoo Kickr trainers via Bluetooth LE
"""

import asyncio
from bleak import BleakClient, BleakScanner
from typing import Optional
import struct

# Bluetooth UUIDs for Fitness Machine Service (FTMS)
FTMS_SERVICE_UUID = "00001826-0000-1000-8000-00805f9b34fb"
FTMS_CONTROL_POINT_UUID = "00002ad9-0000-1000-8000-00805f9b34fb"
FTMS_FEATURE_UUID = "00002acc-0000-1000-8000-00805f9b34fb"
INDOOR_BIKE_DATA_UUID = "00002ad2-0000-1000-8000-00805f9b34fb"

# Wahoo-specific service
WAHOO_TRAINER_SERVICE_UUID = "a026ee0b-0a7d-4ab3-97fa-f1500f9feb8b"
WAHOO_TRAINER_CONTROL_UUID = "a026e005-0a7d-4ab3-97fa-f1500f9feb8b"


class KickrController:
    """Controller for Wahoo Kickr trainers"""

    def __init__(self, device_name: str = "KICKR"):
        self.device_name = device_name
        self.client: Optional[BleakClient] = None
        self.device = None
        self.current_resistance = 0
        self.connected = False

    async def scan_and_connect(self, timeout: int = 10) -> bool:
        """Scan for and connect to Kickr trainer"""
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

            # Subscribe to indoor bike data notifications
            await self.client.start_notify(
                INDOOR_BIKE_DATA_UUID,
                self._handle_bike_data
            )

            return True
        except Exception as e:
            print(f"Error connecting to Kickr: {e}")
            return False

    def _handle_bike_data(self, sender, data: bytearray):
        """Handle notifications from the trainer"""
        # Parse indoor bike data (speed, cadence, power, etc.)
        # This is for monitoring purposes
        pass

    async def set_resistance(self, resistance_percent: float):
        """
        Set resistance level (0-100%)
        Uses FTMS Target Resistance Level control
        """
        if not self.connected or not self.client:
            print("Not connected to Kickr")
            return False

        try:
            # Clamp resistance to valid range
            resistance_percent = max(0, min(100, resistance_percent))

            # FTMS Set Target Resistance Level (opcode 0x04)
            # Resistance is sent as signed 8-bit integer (-100 to 100)
            # We'll use 0-100 range
            resistance_value = int(resistance_percent)

            # Build control point message
            # Byte 0: Opcode (0x04 = Set Target Resistance Level)
            # Byte 1: Resistance level
            message = bytearray([0x04, resistance_value])

            await self.client.write_gatt_char(
                FTMS_CONTROL_POINT_UUID,
                message,
                response=True
            )

            self.current_resistance = resistance_percent
            return True

        except Exception as e:
            print(f"Error setting resistance: {e}")
            return False

    async def set_target_power(self, watts: int):
        """
        Set target power in ERG mode
        Uses FTMS Target Power control
        """
        if not self.connected or not self.client:
            print("Not connected to Kickr")
            return False

        try:
            # FTMS Set Target Power (opcode 0x05)
            # Power is sent as signed 16-bit integer in watts
            message = bytearray([0x05]) + struct.pack('<h', watts)

            await self.client.write_gatt_char(
                FTMS_CONTROL_POINT_UUID,
                message,
                response=True
            )

            return True

        except Exception as e:
            print(f"Error setting target power: {e}")
            return False

    async def set_simulation_mode(self, grade: float, crr: float = 0.004, wind_speed: float = 0.0):
        """
        Set simulation mode parameters
        grade: -1.0 to 1.0 (gradient percentage / 100)
        crr: Coefficient of rolling resistance (default 0.004)
        wind_speed: Wind speed in m/s
        """
        if not self.connected or not self.client:
            print("Not connected to Kickr")
            return False

        try:
            # FTMS Set Indoor Bike Simulation Parameters (opcode 0x11)
            # This is more sophisticated than simple resistance
            wind_speed_int = int(wind_speed * 1000)  # m/s to mm/s
            grade_int = int(grade * 100)  # percentage to 0.01%
            crr_int = int(crr * 10000)  # to 0.0001
            wind_resistance = 0  # kg/m (not typically used)

            message = bytearray([0x11]) + \
                     struct.pack('<hhhH',
                                wind_speed_int,
                                grade_int,
                                crr_int,
                                wind_resistance)

            await self.client.write_gatt_char(
                FTMS_CONTROL_POINT_UUID,
                message,
                response=True
            )

            return True

        except Exception as e:
            print(f"Error setting simulation mode: {e}")
            return False

    async def disconnect(self):
        """Disconnect from the Kickr"""
        if self.client and self.connected:
            await self.client.disconnect()
            self.connected = False
            print("Disconnected from Kickr")
