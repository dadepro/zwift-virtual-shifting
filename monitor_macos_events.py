"""
macOS Input Monitor - Detect ANY input events including Zwift Clicks
Uses macOS Quartz Event Tap to monitor all input events
"""

# Install required packages if not available
try:
    from Quartz import CGEventTapCreate
except ImportError:
    print("Installing macOS frameworks...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyobjc-framework-Quartz", "pyobjc-framework-Cocoa"])
    print("✓ Installed! Please run the script again.")
    sys.exit(0)

import asyncio
from Quartz import (
    CGEventTapCreate,
    kCGHeadInsertEventTap,
    kCGEventTapOptionDefault,
    CGEventMaskBit,
    kCGEventKeyDown,
    kCGEventKeyUp,
    kCGEventLeftMouseDown,
    kCGEventLeftMouseUp,
    kCGEventRightMouseDown,
    kCGEventRightMouseUp,
    kCGEventOtherMouseDown,
    kCGEventOtherMouseUp,
    CFRunLoopAddSource,
    CFRunLoopGetCurrent,
    kCFRunLoopCommonModes,
    CFMachPortCreateRunLoopSource,
    CFRunLoopRun,
    CGEventGetIntegerValueField,
    kCGMouseEventButtonNumber,
    kCGKeyboardEventKeycode,
)
import time
from AppKit import NSEvent

last_event_time = 0
event_count = 0


def event_callback(proxy, event_type, event, refcon):
    """Callback for all system events"""
    global last_event_time, event_count

    current_time = time.time()

    # Debounce rapid events
    if current_time - last_event_time < 0.1:
        return event

    event_count += 1

    event_type_names = {
        kCGEventKeyDown: "Key Down",
        kCGEventKeyUp: "Key Up",
        kCGEventLeftMouseDown: "Left Mouse Down",
        kCGEventLeftMouseUp: "Left Mouse Up",
        kCGEventRightMouseDown: "Right Mouse Down",
        kCGEventRightMouseUp: "Right Mouse Up",
        kCGEventOtherMouseDown: "Other Mouse Down",
        kCGEventOtherMouseUp: "Other Mouse Up",
    }

    event_name = event_type_names.get(event_type, f"Unknown ({event_type})")

    print(f"\n[Event #{event_count}] {event_name}")
    print(f"  Time: {current_time:.3f}")

    # Get key code for keyboard events
    if event_type in [kCGEventKeyDown, kCGEventKeyUp]:
        try:
            keycode = CGEventGetIntegerValueField(event, kCGKeyboardEventKeycode)
            print(f"  ⭐ KEY CODE: {keycode}")

            # Map common key codes to names
            key_map = {
                123: "Left Arrow",
                124: "Right Arrow",
                125: "Down Arrow",
                126: "Up Arrow",
                36: "Return",
                49: "Space",
                51: "Delete",
                53: "Escape",
                48: "Tab",
                0: "A", 1: "S", 2: "D", 6: "Z", 7: "X", 13: "W",
            }

            key_name = key_map.get(keycode, f"Unknown key")
            print(f"  Key: {key_name}")
            print(f"  🎮 ZWIFT CLICK DETECTED!")
            last_event_time = current_time
        except Exception as e:
            print(f"  Error getting keycode: {e}")

    # Try to get button number for mouse events
    if event_type in [kCGEventOtherMouseDown, kCGEventOtherMouseUp]:
        try:
            button = CGEventGetIntegerValueField(event, kCGMouseEventButtonNumber)
            print(f"  Button: {button}")
            print("  ⭐ ZWIFT CLICK BUTTON DETECTED!")
            last_event_time = current_time
        except:
            pass

    # Pass event through to other apps
    return event


def main():
    """Monitor all input events"""
    print("=" * 60)
    print("macOS Input Event Monitor")
    print("=" * 60)
    print("\nMonitoring ALL input events...")
    print("Press your Zwift Click buttons!")
    print("Press Ctrl+C to stop\n")
    print("=" * 60)
    print()

    # Create event mask for all input events
    event_mask = (
        CGEventMaskBit(kCGEventKeyDown) |
        CGEventMaskBit(kCGEventKeyUp) |
        CGEventMaskBit(kCGEventLeftMouseDown) |
        CGEventMaskBit(kCGEventLeftMouseUp) |
        CGEventMaskBit(kCGEventRightMouseDown) |
        CGEventMaskBit(kCGEventRightMouseUp) |
        CGEventMaskBit(kCGEventOtherMouseDown) |
        CGEventMaskBit(kCGEventOtherMouseUp)
    )

    # Create event tap
    from Quartz import kCGSessionEventTap
    tap = CGEventTapCreate(
        kCGSessionEventTap,  # Tap location
        kCGHeadInsertEventTap,  # Place to insert tap
        kCGEventTapOptionDefault,  # Options
        event_mask,  # Events of interest
        event_callback,  # Callback function
        None  # User data
    )

    if not tap:
        print("❌ Failed to create event tap!")
        print("\nYou need to grant Accessibility permissions:")
        print("1. Go to System Preferences → Security & Privacy → Privacy")
        print("2. Select 'Accessibility' on the left")
        print("3. Add Terminal (or your Python app) to the list")
        print("4. Check the box to enable it")
        print("5. Restart this script")
        return

    # Create run loop source
    run_loop_source = CFMachPortCreateRunLoopSource(None, tap, 0)
    CFRunLoopAddSource(CFRunLoopGetCurrent(), run_loop_source, kCFRunLoopCommonModes)

    print("✓ Event monitoring started!")
    print("Waiting for input events...\n")

    try:
        # Run the event loop
        CFRunLoopRun()
    except KeyboardInterrupt:
        print(f"\n\n✓ Captured {event_count} events total")


if __name__ == "__main__":
    main()
