from pynput import keyboard, mouse
import math
from core.stats import stats, updateKeyStats

prevMousePosition = None

def on_key_press(key):
    try:
        # Convert key to string representation
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
    
    stats["key_press_count"] += 1
    updateKeyStats(key_str)
    xp_gain = max(1, round(int(stats["mouse_distance"]) / 100000))
    stats["hero_xp"] += xp_gain

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
    key_listener = keyboard.Listener(on_press=on_key_press)
    mouse_listener = mouse.Listener(on_click=on_mouse_click, on_move=on_mouse_move)

    key_listener.start()
    mouse_listener.start()

    key_listener.join()
    mouse_listener.join()
