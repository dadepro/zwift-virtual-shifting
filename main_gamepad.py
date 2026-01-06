"""
Zwift Virtual Shifting - Gamepad/Controller Mode
Intercepts Zwift Click button presses (as game controller inputs)
and uses them to control virtual shifting on Kickr V5
"""

import asyncio
import json
import signal
import sys
from typing import Optional

from kickr_controller import KickrController
from gear_controller import GearController

try:
    import pygame
    import pygame.joystick
except ImportError:
    print("Installing pygame for gamepad support...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
    import pygame
    import pygame.joystick


class VirtualShiftingGamepadApp:
    """Virtual shifting using Zwift Clicks as game controller"""

    def __init__(self, config_path: str = "config.json"):
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = json.load(f)

        # Initialize components
        self.kickr = KickrController(self.config['bluetooth']['kickr_name'])
        self.gear_controller = GearController(config_path)
        self.gear_controller.on_gradient_change = self.handle_gradient_change

        # Pygame joystick
        pygame.init()
        pygame.joystick.init()
        self.joystick = None

        # Running state
        self.running = False

        # Button state tracking (to detect press/release)
        self.button_states = {}

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

    def find_click_controller(self):
        """Find Zwift Click controller among connected joysticks"""
        joystick_count = pygame.joystick.get_count()

        print(f"Found {joystick_count} game controller(s):")
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            name = joystick.get_name()
            print(f"  {i}: {name}")

            # Check if this looks like a Zwift Click
            if "click" in name.lower() or "zwift" in name.lower():
                print(f"  ⭐ This looks like a Zwift Click!")
                return joystick

        # If no Click found by name, use first controller
        if joystick_count > 0:
            print(f"\nNo Click found by name, using first controller")
            return pygame.joystick.Joystick(0)

        return None

    async def connect_kickr(self) -> bool:
        """Connect to Kickr trainer"""
        print("=" * 50)
        print("Zwift Virtual Shifting - Gamepad Mode")
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
        """Initialize the system"""
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
        gear_info = self.gear_controller.get_current_gear_info()
        print(f"Current Gear: {gear_info['gear']}/{self.gear_controller.max_gear} ({gear_info['display']})")
        gradient_pct = initial_gradient * 100
        if gradient_pct > 0:
            print(f"Gradient Offset: +{gradient_pct:.1f}% (harder)")
        elif gradient_pct < 0:
            print(f"Gradient Offset: {gradient_pct:.1f}% (easier)")
        else:
            print(f"Gradient Offset: neutral")
        print()
        print("Zwift Click Controller detected!")
        print("Press Click buttons to shift gears")
        print("(The buttons will also control Zwift, that's OK)")
        print()
        print("Press Ctrl+C to quit")
        print("=" * 50)
        print()

    async def process_controller_events(self):
        """Process game controller button events"""
        if not self.joystick:
            return

        # Process all pygame events
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                button = event.button
                print(f"Button {button} pressed")

                # Button mapping for Zwift Click
                # You may need to adjust these button numbers
                # Try pressing buttons to see which numbers they are
                if button == 0:  # Adjust this number
                    await self.handle_shift_down()
                elif button == 1:  # Adjust this number
                    await self.handle_shift_up()

            elif event.type == pygame.JOYBUTTONUP:
                button = event.button
                # Button released

            elif event.type == pygame.JOYAXISMOTION:
                # D-pad on some controllers
                axis = event.axis
                value = event.value

                # Might be useful if Clicks use axis instead of buttons
                if abs(value) > 0.5:  # Threshold
                    if value > 0:
                        print(f"Axis {axis} positive")
                    else:
                        print(f"Axis {axis} negative")

    async def run(self):
        """Main run loop"""
        # Find and initialize controller
        print("Looking for game controllers...")
        self.joystick = self.find_click_controller()

        if not self.joystick:
            print("❌ No game controller found!")
            print("\nMake sure:")
            print("1. Zwift Click is powered on")
            print("2. Click is paired with your computer")
            print("3. Zwift can see the Click")
            return

        self.joystick.init()
        print(f"✓ Using controller: {self.joystick.get_name()}")
        print(f"  Buttons: {self.joystick.get_numbuttons()}")
        print(f"  Axes: {self.joystick.get_numaxes()}")
        print()

        # Connect to Kickr
        if not await self.connect_kickr():
            print("Failed to connect. Exiting.")
            return

        # Initialize
        await self.initialize()

        # Set running flag
        self.running = True

        # Main event loop
        try:
            while self.running:
                await self.process_controller_events()
                await asyncio.sleep(0.05)  # 20 Hz polling
        except KeyboardInterrupt:
            print("\n\nShutting down...")
        finally:
            await self.shutdown()

    async def shutdown(self):
        """Clean shutdown"""
        print("Disconnecting...")

        # Reset gradient
        if self.kickr.connected:
            await self.kickr.set_simulation_mode(grade=0.0, crr=0.004, wind_speed=0.0)

        # Disconnect Kickr
        await self.kickr.disconnect()

        # Quit pygame
        pygame.quit()

        print("✓ Disconnected")
        self.running = False


def main():
    """Entry point"""
    print("\n")

    app = VirtualShiftingGamepadApp()

    # Signal handlers
    def signal_handler(sig, frame):
        print("\n\nReceived interrupt signal")
        app.running = False

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Run
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
