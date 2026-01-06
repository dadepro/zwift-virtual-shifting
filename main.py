"""
Zwift Virtual Shifting - Main Application
Bridges Zwift Click controllers to Wahoo Kickr V5 for virtual shifting
"""

import asyncio
import json
import signal
import sys
from typing import Optional

from kickr_controller import KickrController
from click_listener_v2 import ZwiftClickListener, DualZwiftClickListener
from gear_controller import GearController


class VirtualShiftingApp:
    """Main application for virtual shifting"""

    def __init__(self, config_path: str = "config.json"):
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = json.load(f)

        # Initialize components
        self.kickr = KickrController(self.config['bluetooth']['kickr_name'])
        self.gear_controller = GearController(config_path)

        # Use dual click listener for left/right buttons
        self.click_listener = DualZwiftClickListener(
            device_name=self.config['bluetooth']['click_name'],
            on_shift_up=self.handle_shift_up,
            on_shift_down=self.handle_shift_down
        )

        # Set up gear controller callbacks
        self.gear_controller.on_gradient_change = self.handle_gradient_change

        # Running state
        self.running = False

    async def handle_shift_up(self):
        """Handle shift up command from Click controller"""
        await self.gear_controller.shift_up()

    async def handle_shift_down(self):
        """Handle shift down command from Click controller"""
        await self.gear_controller.shift_down()

    async def handle_gradient_change(self, gradient: float):
        """Handle gradient change from gear controller"""
        if self.kickr.connected:
            # Use simulation mode with gradient offset
            # This works alongside Zwift's terrain simulation
            await self.kickr.set_simulation_mode(
                grade=gradient,
                crr=0.004,  # Coefficient of rolling resistance
                wind_speed=0.0
            )

    async def connect_devices(self) -> bool:
        """Connect to all Bluetooth devices"""
        print("=" * 50)
        print("Zwift Virtual Shifting")
        print("=" * 50)
        print()

        # Connect to Kickr
        print("[1/2] Connecting to Kickr trainer...")
        kickr_connected = await self.kickr.scan_and_connect(
            timeout=self.config['bluetooth']['scan_timeout']
        )

        if not kickr_connected:
            print("❌ Failed to connect to Kickr")
            return False

        print("✓ Kickr connected")
        print()

        # Connect to Click controllers
        print("[2/2] Connecting to Click controllers...")
        click_connected = await self.click_listener.scan_and_connect(
            timeout=self.config['bluetooth']['scan_timeout']
        )

        if not click_connected:
            print("❌ Failed to connect to Click controllers")
            return False

        print("✓ Click controllers connected")
        print()

        return True

    async def initialize(self):
        """Initialize the virtual shifting system"""
        # Set initial gradient based on starting gear
        initial_gradient = self.gear_controller.get_current_gradient()
        await self.kickr.set_simulation_mode(
            grade=initial_gradient,
            crr=0.004,
            wind_speed=0.0
        )

        print("=" * 50)
        print("Virtual Shifting Active!")
        print("=" * 50)
        print(f"Current Gear: {self.gear_controller.current_gear}/{self.gear_controller.max_gear}")
        gradient_pct = initial_gradient * 100
        if gradient_pct > 0:
            print(f"Gradient Offset: +{gradient_pct:.1f}% (harder)")
        elif gradient_pct < 0:
            print(f"Gradient Offset: {gradient_pct:.1f}% (easier)")
        else:
            print(f"Gradient Offset: neutral")
        print()
        print("Use Click controllers to shift gears")
        print("Press Ctrl+C to quit")
        print("=" * 50)
        print()

    async def run(self):
        """Main run loop"""
        # Connect to devices
        if not await self.connect_devices():
            print("Failed to connect to devices. Exiting.")
            return

        # Initialize system
        await self.initialize()

        # Set running flag
        self.running = True

        # Keep the application running
        try:
            while self.running:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\n\nShutting down...")
        finally:
            await self.shutdown()

    async def shutdown(self):
        """Clean shutdown of all connections"""
        print("Disconnecting devices...")

        # Disconnect Click controllers
        await self.click_listener.disconnect()

        # Reset gradient to neutral before disconnecting
        if self.kickr.connected:
            await self.kickr.set_simulation_mode(grade=0.0, crr=0.004, wind_speed=0.0)

        # Disconnect Kickr
        await self.kickr.disconnect()

        print("✓ Disconnected")
        self.running = False


def main():
    """Entry point"""
    print("\n")

    # Create app instance
    app = VirtualShiftingApp()

    # Set up signal handlers for clean shutdown
    def signal_handler(sig, frame):
        print("\n\nReceived interrupt signal")
        app.running = False

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Run the application
    try:
        asyncio.run(app.run())
    except KeyboardInterrupt:
        print("\n\nExiting...")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print("\nGoodbye!\n")


if __name__ == "__main__":
    main()
