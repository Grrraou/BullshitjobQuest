from core.stats import stats
from ui.logs import logEvent

quests = [
    {"name": "Complete 10 key presses", "condition": lambda: stats["key_press_count"], "target": 10, "completed": False},
    {"name": "Click 5 times", "condition": lambda: stats["mouse_click_count"], "target": 5, "completed": False},
    {"name": "Move mouse 500 pixels", "condition": lambda: stats["mouse_distance"], "target": 500, "completed": False},
]

def updateQuests():
    for quest in quests:
        if not quest["completed"] and quest["condition"]() >= quest["target"]:
            quest["completed"] = True
            logEvent(f"Quest Completed: {quest['name']}")