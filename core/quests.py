from core.stats import stats
from ui.logs import logEvent

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

def updateQuestsAndAchievements():
    for quest in quests:
        if not quest["completed"] and quest["condition"]() >= quest["target"]:
            quest["completed"] = True
            logEvent(f"Quest Completed: {quest['name']}")
    
    for achievement in achievements:
        if not achievement["completed"] and achievement["condition"]() >= achievement["target"]:
            achievement["completed"] = True
            logEvent(f"Achievement Unlocked: {achievement['name']}")
