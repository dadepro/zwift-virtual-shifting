# Usage Guide

## First Time Setup

### 1. Install Python
Ensure you have Python 3.8 or later installed:
```bash
python --version
```

### 2. Install Dependencies
```bash
cd zwift-virtual-shifting
pip install -r requirements.txt
```

### 3. Pair Your Devices
Before running the app:
- Make sure your Kickr V5 is powered on
- Make sure your Zwift Click controllers have fresh batteries
- Ensure no other apps are connected to these devices

## Running the App

### Basic Usage
```bash
python main.py
```

The app will:
1. Scan for your Kickr trainer (10 second timeout)
2. Scan for your Click controllers (10 second timeout)
3. Connect to both devices
4. Start listening for gear shift commands

### With Custom Config
```bash
python main.py --config my-config.json
```

## Configuration

Edit `config.json` to customize behavior:

### Bluetooth Settings
```json
"bluetooth": {
  "kickr_name": "KICKR",        // Part of your Kickr's Bluetooth name
  "click_left_name": "CLICK L",  // Left Click controller name
  "click_right_name": "CLICK R", // Right Click controller name
  "scan_timeout": 10             // Seconds to scan for devices
}
```

### Gear Settings
```json
"gears": {
  "total_gears": 24,      // Total number of virtual gears
  "current_gear": 12,     // Starting gear
  "min_gear": 1,          // Lowest gear
  "max_gear": 24,         // Highest gear
  "shift_smoothing_ms": 200  // Delay between shifts (ms)
}
```

### Resistance Settings
```json
"resistance": {
  "base_resistance": 0,          // Base resistance percentage
  "resistance_per_gear": 2.5,    // Resistance increase per gear
  "min_resistance_percent": 0,   // Minimum resistance
  "max_resistance_percent": 100, // Maximum resistance
  "enable_erg_mode": false       // Use ERG mode instead
}
```

## Using with Training Apps

### Zwift

1. **Start the virtual shifting app first**
   ```bash
   python main.py
   ```

2. **Wait for devices to connect** (you'll see confirmation messages)

3. **Launch Zwift**

4. **In Zwift, pair your devices:**
   - Power: Select your Kickr
   - Controllable: Select your Kickr
   - Cadence: Select your Kickr (or separate cadence sensor)

5. **Start riding** - Use the Click controllers to shift gears

**Important**: The virtual shifting app runs alongside Zwift. Zwift controls the trainer for workout resistance/slope simulation, while the Click controllers add virtual shifting on top.

### TrainingPeaks

1. **Start the virtual shifting app first**

2. **Launch TrainingPeaks**

3. **Connect to your Kickr** in TrainingPeaks

4. **Start your workout** - Use Click controllers to shift during intervals

### Other Apps (Rouvy, FulGaz, etc.)

The app works with any training software that uses your Kickr. Just:
1. Start the virtual shifting app first
2. Launch your training app
3. Connect to the Kickr in your app
4. Use Click controllers to shift

## Troubleshooting

### Kickr Not Found

**Problem**: App can't find your Kickr

**Solutions**:
- Ensure Kickr is powered on (spin the flywheel)
- Make sure no other apps are connected (close Zwift, TrainingPeaks, etc.)
- Check Bluetooth is enabled on your computer
- Move closer to the Kickr
- Try changing `kickr_name` in config to match your Kickr's exact name

### Click Controllers Not Responding

**Problem**: Click buttons don't change gears

**Solutions**:
- Replace batteries in Click controllers
- Re-pair Click controllers with your computer's Bluetooth settings
- Check that Click controllers are within range
- Verify the device names in config.json match your controllers

### Resistance Not Changing

**Problem**: Gears shift on screen but resistance doesn't change

**Solutions**:
- Make sure you're not in an ERG mode workout (ERG mode overrides resistance)
- Try increasing `resistance_per_gear` in config.json
- Check that Kickr is properly connected
- Restart the app and reconnect

### Connection Drops

**Problem**: Devices disconnect during use

**Solutions**:
- Ensure strong Bluetooth signal (move computer closer)
- Close other Bluetooth applications
- Restart Bluetooth on your computer
- Update Kickr firmware via Wahoo app

## Advanced Configuration

### Custom Gear Ratios

You can simulate specific bike gearing by modifying `gear_controller.py`:

```python
# Edit the get_gear_display() method to match your bike's gearing
cassette = [28, 25, 23, 21, 19, 17, 15, 14, 13, 12, 11]  # Your cassette
chainrings = [53, 39]  # Your chainrings
```

### ERG Mode

To use power-based ERG mode instead of resistance:

1. Set `"enable_erg_mode": true` in config.json
2. The app will adjust target power instead of resistance
3. Each gear shift changes power by a fixed wattage

### Multiple Profiles

Create multiple config files for different use cases:

```bash
# Climbing profile (wider gear range)
python main.py --config config-climbing.json

# Flat racing profile (narrower, higher gears)
python main.py --config config-racing.json
```

## Command Line Options

```bash
python main.py [OPTIONS]

Options:
  --config PATH    Path to config file (default: config.json)
  --verbose        Enable verbose logging
  --help          Show help message
```

## Tips for Best Experience

1. **Start the app before your training software** - This ensures clean Bluetooth connections

2. **Test your setup** - Do a short test ride to verify shifting works before a workout

3. **Adjust resistance per gear** - Experiment with the `resistance_per_gear` setting to find what feels right

4. **Use starting gear wisely** - Set `current_gear` to match your usual starting position (middle of range)

5. **Battery life** - Keep fresh batteries in Click controllers for reliable shifting

## FAQ

**Q: Will this work with Zwift's built-in virtual shifting?**

A: This app is for older Kickr models (V5 and earlier) that don't support Zwift's native virtual shifting. If you have a newer Kickr with official support, use Zwift's built-in feature instead.

**Q: Can I use other button controllers instead of Zwift Clicks?**

A: Yes! Any Bluetooth button/remote that sends notifications can work. You may need to adjust the UUID values in `click_listener.py`.

**Q: Does this interfere with ERG mode workouts?**

A: ERG mode (power target) takes priority over resistance mode. During ERG workouts, gear shifting may not affect feel as much since the trainer maintains target power.

**Q: Can I use this with a real bike on the trainer?**

A: Yes! You can use your bike's real gears AND virtual shifting together for an extended gear range.

## Support

For issues, questions, or feature requests:
- Open an issue on GitHub
- Check existing issues for solutions
- Include your config.json and error messages when reporting bugs
