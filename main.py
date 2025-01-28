import tkinter as tk
from tkinter import ttk, StringVar, messagebox, filedialog
from random import randint, choice
from pynput import keyboard, mouse
import threading
import math
import os
import json

# File to store statistics
log_file = "stats.json"

# Stats
stats = {
    "key_press_count": 0,
    "mouse_click_count": 0,
    "mouse_distance": 0.0,
    "hero_level": 1,
    "hero_xp": 0,
    "xp_threshold": 100,
    "inventory": [],
}

# Previous mouse position
prev_mouse_position = None

# Quests and achievements
quests = [
    {"name": "Complete 10 key presses", "condition": lambda: stats["key_press_count"], "target": 10, "completed": False},
    {"name": "Click 5 times", "condition": lambda: stats["mouse_click_count"], "target": 5, "completed": False},
    {"name": "Move mouse 500 pixels", "condition": lambda: stats["mouse_distance"], "target": 500, "completed": False},
]
achievements = [
    {"name": "Key Master (100 key presses)", "condition": lambda: stats["key_press_count"], "target": 100, "completed": False},
    {"name": "Clicker Pro (50 clicks)", "condition": lambda: stats["mouse_click_count"], "target": 50, "completed": False},
    {"name": "Traveler (5000 pixels moved)", "condition": lambda: stats["mouse_distance"], "target": 5000, "completed": False},
]

# Load stats from file
def load_stats(filepath=log_file):
    global stats
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            stats.update(json.load(f))

# Save stats to file
def save_stats(filepath=log_file):
    with open(filepath, "w") as f:
        json.dump(stats, f, indent=4)

# Import stats
def import_save():
    filepath = filedialog.askopenfilename(title="Import Save File", filetypes=[("JSON Files", "*.json")])
    if filepath:
        load_stats(filepath)
        messagebox.showinfo("Import Successful", "Save file imported successfully!")
        update_gui()

# Export stats
def export_save():
    filepath = filedialog.asksaveasfilename(title="Export Save File", defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if filepath:
        save_stats(filepath)
        messagebox.showinfo("Export Successful", "Save file exported successfully!")

# Log events to the Adventure console
def log_event(message):
    adventure_log.insert(tk.END, message)
    adventure_log.see(tk.END)

# Update quests and achievements
def update_quests_and_achievements():
    for quest in quests:
        if not quest["completed"] and quest["condition"]() >= quest["target"]:
            quest["completed"] = True
            log_event(f"Quest Completed: {quest['name']}")
    for achievement in achievements:
        if not achievement["completed"] and achievement["condition"]() >= achievement["target"]:
            achievement["completed"] = True
            log_event(f"Achievement Unlocked: {achievement['name']}")

# Level up hero
def level_up():
    while stats["hero_xp"] >= stats["xp_threshold"]:
        stats["hero_xp"] -= stats["xp_threshold"]
        stats["hero_level"] += 1
        stats["xp_threshold"] = int(stats["xp_threshold"] * 1.5)
        log_event(f"Level Up! Hero is now level {stats['hero_level']}")

# Update GUI
def update_gui():
    stats["hero_xp"] += stats["key_press_count"] + stats["mouse_click_count"] + int(stats["mouse_distance"] // 100)
    level_up()
    update_quests_and_achievements()

    # Update labels
    key_var.set(f"Keys Pressed: {stats['key_press_count']}")
    click_var.set(f"Mouse Clicks: {stats['mouse_click_count']}")
    distance_var.set(f"Mouse Distance: {stats['mouse_distance']:.2f} pixels")
    level_var.set(f"Level: {stats['hero_level']}")
    xp_var.set(f"XP: {stats['hero_xp']}/{stats['xp_threshold']}")

    # Update quest progress
    for i, quest in enumerate(quests):
        quest_progress[i].set(quest["condition"]() / quest["target"] * 100)

    # Update achievement progress
    for i, achievement in enumerate(achievements):
        achievement_progress[i].set(achievement["condition"]() / achievement["target"] * 100)

    save_stats()
    root.after(1000, update_gui)

# Handle key presses
def on_key_press(key):
    stats["key_press_count"] += 1

# Handle mouse clicks
def on_mouse_click(x, y, button, pressed):
    if pressed:
        stats["mouse_click_count"] += 1

# Handle mouse movement
def on_mouse_move(x, y):
    global prev_mouse_position
    if prev_mouse_position is not None:
        dx = x - prev_mouse_position[0]
        dy = y - prev_mouse_position[1]
        distance = math.sqrt(dx**2 + dy**2)
        stats["mouse_distance"] += distance
    prev_mouse_position = (x, y)

# Start listeners
def start_listeners():
    global prev_mouse_position
    prev_mouse_position = (0, 0)

    key_listener = keyboard.Listener(on_press=on_key_press)
    mouse_listener = mouse.Listener(on_click=on_mouse_click, on_move=on_mouse_move)

    key_listener.start()
    mouse_listener.start()

    key_listener.join()
    mouse_listener.join()

# Load stats on startup
load_stats()

# GUI Setup
root = tk.Tk()
root.title("Idle RPG Tracker")

# Tabs
notebook = ttk.Notebook(root)
notebook.pack(padx=10, pady=10, expand=True)

# Hero Tab
hero_tab = ttk.Frame(notebook)
notebook.add(hero_tab, text="Hero")

key_var = StringVar(value=f"Keys Pressed: {stats['key_press_count']}")
click_var = StringVar(value=f"Mouse Clicks: {stats['mouse_click_count']}")
distance_var = StringVar(value=f"Mouse Distance: {stats['mouse_distance']:.2f} pixels")
level_var = StringVar(value=f"Level: {stats['hero_level']}")
xp_var = StringVar(value=f"XP: {stats['hero_xp']}/{stats['xp_threshold']}")

tk.Label(hero_tab, textvariable=key_var, font=("Helvetica", 14)).pack(pady=5)
tk.Label(hero_tab, textvariable=click_var, font=("Helvetica", 14)).pack(pady=5)
tk.Label(hero_tab, textvariable=distance_var, font=("Helvetica", 14)).pack(pady=5)
tk.Label(hero_tab, textvariable=level_var, font=("Helvetica", 14)).pack(pady=5)
tk.Label(hero_tab, textvariable=xp_var, font=("Helvetica", 14)).pack(pady=5)

# Quest Tab
quest_tab = ttk.Frame(notebook)
notebook.add(quest_tab, text="Quests")

quest_progress = [tk.DoubleVar() for _ in quests]
for i, quest in enumerate(quests):
    ttk.Label(quest_tab, text=quest["name"]).pack(anchor="w", padx=10)
    ttk.Progressbar(quest_tab, variable=quest_progress[i], maximum=100).pack(fill="x", padx=10, pady=5)

# Achievements Tab
achievement_tab = ttk.Frame(notebook)
notebook.add(achievement_tab, text="Achievements")

achievement_progress = [tk.DoubleVar() for _ in achievements]
for i, achievement in enumerate(achievements):
    ttk.Label(achievement_tab, text=achievement["name"]).pack(anchor="w", padx=10)
    ttk.Progressbar(achievement_tab, variable=achievement_progress[i], maximum=100).pack(fill="x", padx=10, pady=5)

# Inventory Tab
inventory_tab = ttk.Frame(notebook)
notebook.add(inventory_tab, text="Inventory")

inventory_var = StringVar(value="No items yet.")
tk.Label(inventory_tab, textvariable=inventory_var, font=("Helvetica", 14), justify="left").pack(pady=5)

# Adventure Tab
adventure_tab = ttk.Frame(notebook)
notebook.add(adventure_tab, text="Adventure")

adventure_log = tk.Listbox(adventure_tab, height=15, font=("Courier", 10))
adventure_log.pack(fill="both", expand=True, padx=5, pady=5)

# Config Tab
config_tab = ttk.Frame(notebook)
notebook.add(config_tab, text="Config")

# Import/Export Save Buttons
tk.Button(config_tab, text="Import Save", command=import_save).pack(pady=5)
tk.Button(config_tab, text="Export Save", command=export_save).pack(pady=5)

# Boolean variable for Always on Top
always_on_top_var = tk.BooleanVar(value=False)

def toggle_always_on_top():
    root.wm_attributes("-topmost", always_on_top_var.get())

# Add Checkbutton for Always on Top
tk.Checkbutton(config_tab, text="Always on Top", variable=always_on_top_var, command=toggle_always_on_top).pack(pady=5)


# Start listeners and GUI loop
listener_thread = threading.Thread(target=start_listeners, daemon=True)
listener_thread.start()

root.after(1000, update_gui)
root.mainloop()
