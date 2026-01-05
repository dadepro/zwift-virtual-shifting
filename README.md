# Zwift Virtual Shifting for Kickr V5

A Python application that enables virtual shifting on Wahoo Kickr V5 (and older models) using Zwift Click controllers. Works with Zwift, TrainingPeaks, and other training platforms.

## Overview

This app bridges the gap between Zwift Click controllers and older Kickr trainers that don't have official virtual shifting support. It listens for gear shift commands from Zwift Clicks and automatically adjusts the resistance on your Kickr V5 to simulate different gears.

## Features

- ✅ Virtual shifting with Zwift Click controllers
- ✅ Compatible with Kickr V5 (2020) and older models
- ✅ Works with Zwift
- ✅ Works with TrainingPeaks
- ✅ Customizable gear ratios
- ✅ Smooth resistance transitions
- ✅ Bluetooth LE connectivity
- ✅ Cross-platform (Windows, macOS, Linux)

## How It Works

1. Connects to your Zwift Click controllers via Bluetooth LE
2. Connects to your Wahoo Kickr V5 via Bluetooth LE
3. Listens for button presses (gear shifts) from the Click controllers
4. Translates gear changes into resistance adjustments
5. Sends updated resistance commands to the Kickr
6. Works alongside your training app (Zwift, TrainingPeaks, etc.)

## Requirements

- Python 3.8 or higher
- Wahoo Kickr V5 (2020) or older Kickr model
- Zwift Click controllers (or compatible Bluetooth buttons)
- Bluetooth LE adapter (built-in on most modern computers)

## Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/zwift-virtual-shifting.git
cd zwift-virtual-shifting

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

```bash
# Run the application
python main.py
```

The app will:
1. Scan for your Zwift Click controllers
2. Scan for your Kickr V5
3. Start bridging gear shift commands

## Configuration

Edit `config.json` to customize:
- Gear ratios
- Resistance multipliers
- Bluetooth device names
- Shift timing and smoothness

## Usage with Training Apps

### Zwift
1. Start this app first
2. Launch Zwift
3. Connect to your Kickr as usual in Zwift
4. Use Click controllers to shift gears
5. The app will adjust resistance automatically

### TrainingPeaks
1. Start this app first
2. Launch TrainingPeaks
3. Connect to your Kickr
4. Use Click controllers during workouts

## Troubleshooting

**Kickr not found**: Make sure your Kickr is powered on and not connected to other apps

**Clicks not responding**: Ensure Click controllers have fresh batteries

**Resistance not changing**: Check Bluetooth connections and try restarting the app

## Technical Details

This app uses:
- `bleak` for Bluetooth LE communication
- FTMS (Fitness Machine Service) protocol for trainer control
- Custom gear ratio calculations for smooth shifting

## Credits

Inspired by the QZ app and the community's work on virtual shifting for older trainers.

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please open an issue or PR.

## Support

For issues, questions, or suggestions, please open a GitHub issue.
