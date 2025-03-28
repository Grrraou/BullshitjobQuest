from pynput import keyboard, mouse
import math
from core.stats import stats, updateKeyStats
import time

prevMousePosition = None
pressed_keys = set()  # Track currently pressed keys to prevent multiple counts
last_combo_time = 0  # Track when the last combination was counted
COMBO_COOLDOWN = 0.5  # Minimum time between counting the same combination

def format_key_name(key_str):
    # Format special keys
    if key_str.startswith('Key.'):
        # Remove 'Key.' prefix and capitalize
        return key_str[4:].capitalize()
    return key_str.upper()

def on_key_combo(combo):
    """Handle key combination press"""
    # Check if enough time has passed since last combo
    current_time = time.time()
    if current_time - last_combo_time >= COMBO_COOLDOWN:
        # Initialize combo stats if not exists
        if combo not in stats["key_combo_stats"]:
            stats["key_combo_stats"][combo] = 0
        
        # Update combo stats
        stats["key_combo_stats"][combo] += 1
        stats["key_combo_count"] += 1
        
        # Update most used combo
        if stats["key_combo_stats"][combo] > stats["key_combo_stats"].get(stats["most_used_combo"], 0):
            stats["most_used_combo"] = combo
        
        # Update last combo time
        last_combo_time = current_time

def on_key_press(key):
    """Handle key press events"""
    try:
        # Convert key to string representation
        try:
            key_str = key.char
        except AttributeError:
            # Handle special keys
            if hasattr(key, 'vk'):
                # Handle number pad keys
                if key.vk == 96:  # NumPad0
                    key_str = 'Key.numpad0'
                elif key.vk == 97:  # NumPad1
                    key_str = 'Key.numpad1'
                elif key.vk == 98:  # NumPad2
                    key_str = 'Key.numpad2'
                elif key.vk == 99:  # NumPad3
                    key_str = 'Key.numpad3'
                elif key.vk == 100:  # NumPad4
                    key_str = 'Key.numpad4'
                elif key.vk == 101:  # NumPad5
                    key_str = 'Key.numpad5'
                elif key.vk == 102:  # NumPad6
                    key_str = 'Key.numpad6'
                elif key.vk == 103:  # NumPad7
                    key_str = 'Key.numpad7'
                elif key.vk == 104:  # NumPad8
                    key_str = 'Key.numpad8'
                elif key.vk == 105:  # NumPad9
                    key_str = 'Key.numpad9'
                elif key.vk == 144:  # NumLock
                    key_str = 'Key.numlock'
                else:
                    key_str = str(key)
            else:
                key_str = str(key)
        
        # Format key name
        key_name = format_key_name(key_str)
        
        # Update key press count
        stats["key_press_count"] += 1
        
        # Only update detailed stats if tracking is enabled
        if stats["track_detailed_keys"]:
            # Update individual key stats
            if key_name not in stats["key_stats"]:
                stats["key_stats"][key_name] = 0
            stats["key_stats"][key_name] += 1
            
            # Update most pressed key
            if stats["key_stats"][key_name] > stats["most_used_key"]["count"]:
                stats["most_used_key"] = {"key": key_name, "count": stats["key_stats"][key_name]}
            
            # Add to current keys for combination tracking
            pressed_keys.add(key_name)
            
            # Check for combinations
            if len(pressed_keys) > 1:
                # Sort keys for consistent ordering
                sorted_keys = sorted(pressed_keys)
                combo = " + ".join(sorted_keys)
                
                # Initialize combo stats if not exists
                if combo not in stats["key_combo_stats"]:
                    stats["key_combo_stats"][combo] = 0
                
                # Update combo stats
                stats["key_combo_stats"][combo] += 1
                stats["key_combo_count"] += 1
                
                # Update most used combo
                if stats["key_combo_stats"][combo] > stats["most_used_combo"]["count"]:
                    stats["most_used_combo"] = {"combo": combo, "count": stats["key_combo_stats"][combo]}
            
    except Exception as e:
        print(f"Error in on_key_press: {e}")

def on_key_release(key):
    try:
        # Convert key to string representation
        try:
            key_str = key.char
        except AttributeError:
            # Handle special keys
            if hasattr(key, 'vk'):
                # Handle number pad keys
                if key.vk == 96:  # NumPad0
                    key_str = 'Key.numpad0'
                elif key.vk == 97:  # NumPad1
                    key_str = 'Key.numpad1'
                elif key.vk == 98:  # NumPad2
                    key_str = 'Key.numpad2'
                elif key.vk == 99:  # NumPad3
                    key_str = 'Key.numpad3'
                elif key.vk == 100:  # NumPad4
                    key_str = 'Key.numpad4'
                elif key.vk == 101:  # NumPad5
                    key_str = 'Key.numpad5'
                elif key.vk == 102:  # NumPad6
                    key_str = 'Key.numpad6'
                elif key.vk == 103:  # NumPad7
                    key_str = 'Key.numpad7'
                elif key.vk == 104:  # NumPad8
                    key_str = 'Key.numpad8'
                elif key.vk == 105:  # NumPad9
                    key_str = 'Key.numpad9'
                elif key.vk == 144:  # NumLock
                    key_str = 'Key.numlock'
                else:
                    key_str = str(key)
            else:
                key_str = str(key)
        
        # Format key name
        key_name = format_key_name(key_str)
        
        # Remove key from pressed keys when released
        if key_name in pressed_keys:
            pressed_keys.remove(key_name)
            
    except Exception as e:
        print(f"Error in on_key_release: {e}")

def on_mouse_click(x, y, button, pressed):
    if pressed:
        print(f"Button pressed: {button}")
        if str(button) == "Button.left":
            stats["Button.left"] += 1
        elif str(button) == "Button.right":
            stats["Button.right"] += 1
        elif str(button) == "Button.middle":
            stats["Button.middle"] += 1
        else:
            stats["Button.other"] += 1
            
        xp_gain = max(1, round(int(stats["mouse_distance"]) / 100000))
        stats["hero_xp"] += xp_gain

def on_mouse_move(x, y):
    global prevMousePosition
    if prevMousePosition is not None:
        dx, dy = x - prevMousePosition[0], y - prevMousePosition[1]
        moveDistance = math.sqrt(dx**2 + dy**2)
        stats["mouse_distance"] += moveDistance
    prevMousePosition = (x, y)

def startListeners():
    key_listener = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)
    mouse_listener = mouse.Listener(on_click=on_mouse_click, on_move=on_mouse_move)

    key_listener.start()
    mouse_listener.start()

    key_listener.join()
    mouse_listener.join()
