from core.stats import stats
from ui.logs import logEvent

achievements = [
    {"name": "Key Master (100 key presses)", "condition": lambda: stats["key_press_count"], "target": 100, "completed": False},
    {"name": "Clicker Pro (50 clicks)", "condition": lambda: stats["Button.left"], "target": 50, "completed": False},
    {"name": "Traveler (5000 pixels moved)", "condition": lambda: stats["mouse_distance"], "target": 5000, "completed": False},
]

def updateAchievements():
    for achievement in achievements:
        if not achievement["completed"] and achievement["condition"]() >= achievement["target"]:
            achievement["completed"] = True
            logEvent(f"Achievement Unlocked: {achievement['name']}")
