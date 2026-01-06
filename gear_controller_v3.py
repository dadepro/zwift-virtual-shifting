"""
Gear Controller v3 - Gear Ratio Simulation (QZ Approach)
Simulates actual bike gearing using chainring/cog combinations
This is how QZ implements virtual shifting successfully
"""

import asyncio
from typing import Callable, Optional
import json


class GearController:
    """Manages virtual gearing using gear ratio simulation (QZ method)"""

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

        # Bike gearing configuration (like QZ)
        # 2x12 setup: 53/39 chainrings, 11-34 cassette
        self.chainrings = [39, 53]  # Small and large chainring
        self.cassette = [34, 30, 26, 23, 21, 19, 17, 15, 13, 12, 11, 10]  # 12-speed

        # Wheel parameters (standard road bike)
        self.wheel_diameter = 0.700  # 700c wheel in meters
        self.wheel_circumference = self.wheel_diameter * 3.14159

        # Callbacks
        self.on_gear_change: Optional[Callable[[int, dict], None]] = None
        self.on_gear_ratio_change: Optional[Callable[[float, int, int], None]] = None

        # Display settings
        self.show_gear_changes = self.config['display']['show_gear_changes']

    def get_chainring_cog_for_gear(self, gear: int) -> tuple:
        """
        Get the chainring and cog combination for a given gear

        Gears 1-12: Small chainring (39T) with cassette
        Gears 13-24: Large chainring (53T) with cassette

        Returns: (chainring_teeth, cog_teeth)
        """
        if gear <= 12:
            # Small chainring
            chainring = self.chainrings[0]
            cog_index = 12 - gear  # Reverse order (easier gears = bigger cogs)
        else:
            # Large chainring
            chainring = self.chainrings[1]
            cog_index = 24 - gear  # Reverse order

        # Clamp to cassette range
        cog_index = max(0, min(len(self.cassette) - 1, cog_index))
        cog = self.cassette[cog_index]

        return (chainring, cog)

    def get_gear_ratio(self, gear: int) -> float:
        """
        Calculate gear ratio for a given gear
        Gear ratio = chainring teeth / cog teeth

        Higher ratio = harder to pedal, faster speed
        Lower ratio = easier to pedal, slower speed
        """
        chainring, cog = self.get_chainring_cog_for_gear(gear)
        ratio = chainring / cog
        return ratio

    def get_gradient_for_gear_ratio(self, ratio: float) -> float:
        """
        Convert gear ratio to gradient offset for trainer simulation

        Lower ratios (easier gears) → positive gradient (harder resistance)
        Higher ratios (harder gears) → negative gradient (easier resistance)

        This simulates the effect of being in a lower vs higher gear
        """
        # Reference ratio (middle gear ≈ 2.5)
        reference_ratio = 2.5

        # Calculate gradient offset
        # Ratio below reference = climbing (positive gradient)
        # Ratio above reference = descending (negative gradient)
        gradient = (reference_ratio - ratio) * 0.05  # 5% per ratio unit

        # Clamp to reasonable range
        gradient = max(-0.15, min(0.15, gradient))

        return gradient

    async def shift_up(self):
        """Shift to a harder gear (increase gear number, higher ratio)"""
        if self.current_gear < self.max_gear:
            self.current_gear += 1
            await self._apply_gear_change()
        else:
            if self.show_gear_changes:
                print(f"Already in highest gear ({self.max_gear})")

    async def shift_down(self):
        """Shift to an easier gear (decrease gear number, lower ratio)"""
        if self.current_gear > self.min_gear:
            self.current_gear -= 1
            await self._apply_gear_change()
        else:
            if self.show_gear_changes:
                print(f"Already in lowest gear ({self.min_gear})")

    async def _apply_gear_change(self):
        """Apply the gear change and update simulation"""
        chainring, cog = self.get_chainring_cog_for_gear(self.current_gear)
        ratio = self.get_gear_ratio(self.current_gear)
        gradient = self.get_gradient_for_gear_ratio(ratio)

        if self.show_gear_changes:
            gradient_pct = gradient * 100
            if gradient > 0:
                feel = "harder"
            elif gradient < 0:
                feel = "easier"
            else:
                feel = "neutral"

            print(f"⚙️  Gear: {self.current_gear}/{self.max_gear} "
                  f"({chainring}T-{cog}T) | "
                  f"Ratio: {ratio:.2f} | "
                  f"Gradient: {gradient_pct:+.1f}% ({feel})")

        # Trigger callbacks
        if self.on_gear_change:
            gear_info = {
                'gear': self.current_gear,
                'chainring': chainring,
                'cog': cog,
                'ratio': ratio,
                'gradient': gradient
            }
            await self.on_gear_change(self.current_gear, gear_info)

        if self.on_gear_ratio_change:
            await self.on_gear_ratio_change(ratio, chainring, cog)

        # Smooth shifting
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
        ratio = self.get_gear_ratio(self.current_gear)
        return self.get_gradient_for_gear_ratio(ratio)

    def get_current_gear_info(self) -> dict:
        """Get complete current gear information"""
        chainring, cog = self.get_chainring_cog_for_gear(self.current_gear)
        ratio = self.get_gear_ratio(self.current_gear)
        gradient = self.get_gradient_for_gear_ratio(ratio)

        return {
            'gear': self.current_gear,
            'chainring': chainring,
            'cog': cog,
            'ratio': ratio,
            'gradient': gradient,
            'display': f"{chainring}-{cog}"
        }

    def get_gear_display(self) -> str:
        """Get formatted gear display string"""
        chainring, cog = self.get_chainring_cog_for_gear(self.current_gear)
        return f"{chainring}-{cog}"
