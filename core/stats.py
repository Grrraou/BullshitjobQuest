import json
import os

# File to store statistics
log_file = "data/stats.json"

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