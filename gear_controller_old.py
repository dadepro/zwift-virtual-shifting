"""
Gear Controller
Manages virtual gear state and calculates resistance based on gear selection
"""

import asyncio
from typing import Callable, Optional
import json


class GearController:
    """Manages virtual gearing and resistance calculations"""

    def __init__(self, config_path: str = "config.json"):
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = json.load(f)

        # Gear settings
        self.total_gears = self.config['gears']['total_gears']
        self.current_gear = self.config['gears']['current_gear']
        self.min_gear = self.config['gears']['min_gear']
        self.max_gear = self.config['gears']['max_gear']
        self.shift_smoothing_ms = self.config['gears']['shift_smoothing_ms']

        # Resistance settings
        self.base_resistance = self.config['resistance']['base_resistance']
        self.resistance_per_gear = self.config['resistance']['resistance_per_gear']
        self.min_resistance = self.config['resistance']['min_resistance_percent']
        self.max_resistance = self.config['resistance']['max_resistance_percent']

        # Callbacks
        self.on_gear_change: Optional[Callable[[int, float], None]] = None
        self.on_resistance_change: Optional[Callable[[float], None]] = None

        # Display settings
        self.show_gear_changes = self.config['display']['show_gear_changes']
        self.show_resistance_changes = self.config['display']['show_resistance_changes']

    def get_resistance_for_gear(self, gear: int) -> float:
        """
        Calculate resistance percentage for a given gear
        Lower gears = higher resistance (easier to pedal, lower speed)
        Higher gears = lower resistance (harder to pedal, higher speed)

        Note: This is inverted from traditional thinking because we're
        simulating resistance, not mechanical advantage
        """
        # Normalize gear to 0-1 range
        gear_ratio = (gear - self.min_gear) / (self.max_gear - self.min_gear)

        # Calculate resistance
        # Lower gears (easier) = lower resistance needed
        # Higher gears (harder) = higher resistance needed
        resistance = self.base_resistance + (gear_ratio * self.resistance_per_gear * self.total_gears)

        # Clamp to valid range
        resistance = max(self.min_resistance, min(self.max_resistance, resistance))

        return resistance

    async def shift_up(self):
        """Shift to a harder gear (increase gear number)"""
        if self.current_gear < self.max_gear:
            self.current_gear += 1
            await self._apply_gear_change()
        else:
            if self.show_gear_changes:
                print(f"Already in highest gear ({self.max_gear})")

    async def shift_down(self):
        """Shift to an easier gear (decrease gear number)"""
        if self.current_gear > self.min_gear:
            self.current_gear -= 1
            await self._apply_gear_change()
        else:
            if self.show_gear_changes:
                print(f"Already in lowest gear ({self.min_gear})")

    async def _apply_gear_change(self):
        """Apply the gear change and update resistance"""
        resistance = self.get_resistance_for_gear(self.current_gear)

        if self.show_gear_changes:
            print(f"⚙️  Gear: {self.current_gear}/{self.max_gear} | Resistance: {resistance:.1f}%")

        # Trigger callbacks
        if self.on_gear_change:
            await self.on_gear_change(self.current_gear, resistance)

        if self.on_resistance_change:
            await self.on_resistance_change(resistance)

        # Smooth shifting (optional delay)
        if self.shift_smoothing_ms > 0:
            await asyncio.sleep(self.shift_smoothing_ms / 1000.0)

    def set_gear(self, gear: int):
        """Directly set a specific gear"""
        if self.min_gear <= gear <= self.max_gear:
            self.current_gear = gear
            return self._apply_gear_change()
        else:
            print(f"Invalid gear: {gear} (valid range: {self.min_gear}-{self.max_gear})")

    def get_current_gear(self) -> int:
        """Get current gear number"""
        return self.current_gear

    def get_current_resistance(self) -> float:
        """Get current resistance percentage"""
        return self.get_resistance_for_gear(self.current_gear)

    def get_gear_display(self) -> str:
        """Get formatted gear display string"""
        # Display as chainring-cassette format (simulated)
        # e.g., "53-17" for road bike gearing

        # Simulate front chainring (2 rings)
        if self.current_gear <= self.total_gears / 2:
            front = 39  # Small chainring
            rear_index = self.current_gear
        else:
            front = 53  # Large chainring
            rear_index = self.current_gear - int(self.total_gears / 2)

        # Simulate rear cassette (11-28 range)
        cassette = [28, 25, 23, 21, 19, 17, 15, 14, 13, 12, 11]
        rear_gears = int(self.total_gears / 2)

        if rear_index < len(cassette):
            rear = cassette[rear_index]
        else:
            rear = cassette[-1]

        return f"{front}-{rear}"
