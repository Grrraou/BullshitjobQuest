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
    "safe_for_work": False,  # New setting for SafeForWork mode
    "key_stats": {},  # Dictionary to store individual key press counts
    "most_used_key": {"key": "", "count": 0},  # Track the most used key
    "key_combo_stats": {},  # Dictionary to store key combination counts
    "most_used_combo": {"combo": "", "count": 0},  # Track the most used combination
    "quests_completed": 0,
    "track_detailed_keys": True,  # New option for detailed key tracking
    "key_combo_count": 0  # Track total number of key combinations
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
    # Create data directory if it doesn't exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
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

def updateKeyStats(key):
    # Convert tuple keys to strings
    if isinstance(key, tuple):
        key_str = key[0]
    else:
        key_str = str(key)
    
    if key_str not in stats["key_stats"]:
        stats["key_stats"][key_str] = 0
    stats["key_stats"][key_str] += 1
    
    # Update most used key
    if stats["key_stats"][key_str] > stats["most_used_key"]["count"]:
        stats["most_used_key"] = {"key": key_str, "count": stats["key_stats"][key_str]}

def initStats():
    """Initialize all stats to their default values"""
    global stats
    stats = {
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
        "safe_for_work": False,
        "key_stats": {},
        "most_used_key": {"key": "", "count": 0},
        "key_combo_stats": {},
        "most_used_combo": {"combo": "", "count": 0},
        "quests_completed": 0,
        "track_detailed_keys": True,
        "key_combo_count": 0
    }
    saveStats()