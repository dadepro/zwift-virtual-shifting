"""
Gear Controller v2 - Gradient-based Virtual Shifting
Uses gradient simulation instead of direct resistance control
Works alongside Zwift by adding/subtracting gradient based on gear selection
"""

import asyncio
from typing import Callable, Optional
import json


class GearController:
    """Manages virtual gearing using gradient simulation"""

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

        # Gradient settings (new approach)
        # Each gear adds/removes gradient
        # Range: -0.10 to +0.10 (±10% gradient)
        self.gradient_per_gear = 0.01  # 1% gradient change per gear
        self.base_gradient = 0.0

        # Callbacks
        self.on_gear_change: Optional[Callable[[int, float], None]] = None
        self.on_gradient_change: Optional[Callable[[float], None]] = None

        # Display settings
        self.show_gear_changes = self.config['display']['show_gear_changes']

    def get_gradient_for_gear(self, gear: int) -> float:
        """
        Calculate gradient offset for a given gear

        Lower gears (1-12) = positive gradient (like going uphill, harder)
        Higher gears (13-24) = negative gradient (like going downhill, easier)

        This adds to whatever gradient Zwift is sending based on terrain
        """
        # Center gear (12) = 0% gradient offset
        # Gear 1 = +11% gradient (much harder)
        # Gear 24 = -12% gradient (much easier)

        middle_gear = (self.max_gear + self.min_gear) / 2
        gear_offset = gear - middle_gear

        # Convert to gradient (-1.0 to 1.0 where 1.0 = 100% grade)
        gradient = -gear_offset * self.gradient_per_gear

        # Clamp to reasonable range (-10% to +10%)
        gradient = max(-0.10, min(0.10, gradient))

        return gradient

    async def shift_up(self):
        """Shift to a harder gear (increase gear number, reduce gradient)"""
        if self.current_gear < self.max_gear:
            self.current_gear += 1
            await self._apply_gear_change()
        else:
            if self.show_gear_changes:
                print(f"Already in highest gear ({self.max_gear})")

    async def shift_down(self):
        """Shift to an easier gear (decrease gear number, increase gradient)"""
        if self.current_gear > self.min_gear:
            self.current_gear -= 1
            await self._apply_gear_change()
        else:
            if self.show_gear_changes:
                print(f"Already in lowest gear ({self.min_gear})")

    async def _apply_gear_change(self):
        """Apply the gear change and update gradient"""
        gradient = self.get_gradient_for_gear(self.current_gear)

        if self.show_gear_changes:
            gear_display = self.get_gear_display()
            gradient_pct = gradient * 100
            if gradient > 0:
                print(f"⚙️  Gear: {self.current_gear}/{self.max_gear} ({gear_display}) | +{gradient_pct:.1f}% gradient (harder)")
            elif gradient < 0:
                print(f"⚙️  Gear: {self.current_gear}/{self.max_gear} ({gear_display}) | {gradient_pct:.1f}% gradient (easier)")
            else:
                print(f"⚙️  Gear: {self.current_gear}/{self.max_gear} ({gear_display}) | neutral")

        # Trigger callbacks
        if self.on_gear_change:
            await self.on_gear_change(self.current_gear, gradient)

        if self.on_gradient_change:
            await self.on_gradient_change(gradient)

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

    def get_current_gradient(self) -> float:
        """Get current gradient offset"""
        return self.get_gradient_for_gear(self.current_gear)

    def get_gear_display(self) -> str:
        """Get formatted gear display string"""
        # Display as chainring-cassette format
        # Simulate 2x12 gearing (53/39 chainrings, 11-28 cassette)

        # Determine front chainring
        if self.current_gear <= 12:
            front = 39  # Small chainring (gears 1-12)
            rear_index = self.current_gear - 1
        else:
            front = 53  # Large chainring (gears 13-24)
            rear_index = self.current_gear - 13

        # 12-speed cassette: 11-28
        cassette = [28, 25, 23, 21, 19, 17, 15, 14, 13, 12, 11, 11]

        if 0 <= rear_index < len(cassette):
            rear = cassette[rear_index]
        else:
            rear = 15  # Default

        return f"{front}-{rear}"
