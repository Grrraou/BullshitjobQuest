from pynput import keyboard, mouse
import math
from core.stats import stats

prevMousePosition = None

def on_key_press(key):
    stats["key_press_count"] += 1
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
