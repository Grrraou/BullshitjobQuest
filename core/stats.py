import json
import os
import sys


# File to store statistics
log_file = "data/stats.json"

# Stats
defaultStats = {
    "key_press_count": 0,
    "Button.left": 0,
    "Button.right": 0,
    "Button.middle": 0,
    "Button.other": 0,
    "mouse_distance": 0.0,
    "hero_level": 1,
    "hero_xp": 0,
    "xp_threshold": 100,
    "inventory": [],
}
stats = defaultStats.copy()

# Load stats from file
def loadStats(filepath=log_file):
    global stats
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            stats.update(json.load(f))

# Save stats to file
def saveStats(filepath=log_file):
    with open(filepath, "w") as f:
        json.dump(stats, f, indent=4)

def resetStats():
    global stats, defaultStats
    stats = defaultStats.copy()     # Reset stats
    saveStats()  
    restartApp()

def restartApp():
    print("Restarting the application...")
    os.execv(sys.executable, ['python'] + sys.argv)