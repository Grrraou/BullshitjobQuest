from pynput import keyboard, mouse
import math
from core.stats import stats

prev_mouse_position = None

def on_key_press(key):
    stats["key_press_count"] += 1

def on_mouse_click(x, y, button, pressed):
    if pressed:
        stats["mouse_click_count"] += 1

def on_mouse_move(x, y):
    global prev_mouse_position
    if prev_mouse_position is not None:
        dx, dy = x - prev_mouse_position[0], y - prev_mouse_position[1]
        stats["mouse_distance"] += math.sqrt(dx**2 + dy**2)
    prev_mouse_position = (x, y)

def start_listeners():
    key_listener = keyboard.Listener(on_press=on_key_press)
    mouse_listener = mouse.Listener(on_click=on_mouse_click, on_move=on_mouse_move)

    key_listener.start()
    mouse_listener.start()

    key_listener.join()
    mouse_listener.join()
