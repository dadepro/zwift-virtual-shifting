"""
Zwift Virtual Shifting - Keyboard Control Version
Uses keyboard shortcuts for shifting instead of Zwift Clicks
Works with Zwift, TrainingPeaks, and other training platforms
"""

import asyncio
import json
import signal
import sys
from typing import Optional

from kickr_controller import KickrController
from gear_controller import GearController

try:
    from pynput import keyboard
except ImportError:
    print("Installing pynput for keyboard control...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pynput"])
    from pynput import keyboard


class VirtualShiftingKeyboardApp:
    """Main application for virtual shifting with keyboard control"""

    def __init__(self, config_path: str = "config.json"):
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = json.load(f)

        # Initialize components
        self.kickr = KickrController(self.config['bluetooth']['kickr_name'])
        self.gear_controller = GearController(config_path)

        # Set up gear controller callbacks
        self.gear_controller.on_gradient_change = self.handle_gradient_change

        # Running state
        self.running = False
        self.keyboard_listener = None

    async def handle_shift_up(self):
        """Handle shift up command"""
        await self.gear_controller.shift_up()

    async def handle_shift_down(self):
        """Handle shift down command"""
        await self.gear_controller.shift_down()

    async def handle_gradient_change(self, gradient: float):
        """Handle gradient change from gear controller"""
        if self.kickr.connected:
            await self.kickr.set_simulation_mode(
                grade=gradient,
                crr=0.004,
                wind_speed=0.0
            )

    def on_key_press(self, key):
        """Handle keyboard input"""
        try:
            # Check for specific keys
            if hasattr(key, 'char'):
                # Letter keys
                if key.char == 'w' or key.char == 'W':
                    # W = shift up (harder)
                    asyncio.create_task(self.handle_shift_up())
                elif key.char == 's' or key.char == 'S':
                    # S = shift down (easier)
                    asyncio.create_task(self.handle_shift_down())
                elif key.char == 'q' or key.char == 'Q':
                    # Q = quit
                    print("\nQuitting...")
                    self.running = False
            else:
                # Special keys
                if key == keyboard.Key.up:
                    # Up arrow = shift up (harder)
                    asyncio.create_task(self.handle_shift_up())
                elif key == keyboard.Key.down:
                    # Down arrow = shift down (easier)
                    asyncio.create_task(self.handle_shift_down())
                elif key == keyboard.Key.page_up:
                    # Page Up = shift up
                    asyncio.create_task(self.handle_shift_up())
                elif key == keyboard.Key.page_down:
                    # Page Down = shift down
                    asyncio.create_task(self.handle_shift_down())

        except Exception as e:
            print(f"Key error: {e}")

    async def connect_kickr(self) -> bool:
        """Connect to Kickr trainer"""
        print("=" * 50)
        print("Zwift Virtual Shifting - Keyboard Control")
        print("=" * 50)
        print()

        print("Connecting to Kickr trainer...")
        kickr_connected = await self.kickr.scan_and_connect(
            timeout=self.config['bluetooth']['scan_timeout']
        )

        if not kickr_connected:
            print("❌ Failed to connect to Kickr")
            return False

        print("✓ Kickr connected")
        print()
        return True

    async def initialize(self):
        """Initialize the virtual shifting system"""
        # Set initial gradient
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
        print("KEYBOARD CONTROLS:")
        print("  ↑ / W / Page Up   = Shift UP (harder gear)")
        print("  ↓ / S / Page Down = Shift DOWN (easier gear)")
        print("  Q                 = Quit")
        print()
        print("Now you can switch to Zwift and use keyboard to shift!")
        print("=" * 50)
        print()

    async def run(self):
        """Main run loop"""
        # Connect to Kickr
        if not await self.connect_kickr():
            print("Failed to connect. Exiting.")
            return

        # Initialize system
        await self.initialize()

        # Start keyboard listener
        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        self.keyboard_listener.start()

        # Set running flag
        self.running = True

        # Keep the application running
        try:
            while self.running:
                await asyncio.sleep(0.1)
        except KeyboardInterrupt:
            print("\n\nShutting down...")
        finally:
            await self.shutdown()

    async def shutdown(self):
        """Clean shutdown"""
        print("Disconnecting...")

        # Stop keyboard listener
        if self.keyboard_listener:
            self.keyboard_listener.stop()

        # Reset gradient
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
    app = VirtualShiftingKeyboardApp()

    # Set up signal handlers
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
