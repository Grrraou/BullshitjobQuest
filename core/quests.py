from core.stats import stats
from ui.logs import logEvent

quests = [
    # Early game quests
    {"name": "Complete 10 key presses", "condition": lambda: stats["key_press_count"], "target": 10, "completed": False, "xp_reward": 50},
    {"name": "Click 5 times", "condition": lambda: stats["Button.left"], "target": 5, "completed": False, "xp_reward": 50},
    {"name": "Move mouse 500 pixels", "condition": lambda: stats["mouse_distance"], "target": 500, "completed": False, "xp_reward": 50},
    
    # Early-Mid game quests
    {"name": "Type 25 characters", "condition": lambda: stats["key_press_count"], "target": 25, "completed": False, "xp_reward": 75},
    {"name": "Click 15 times", "condition": lambda: stats["Button.left"], "target": 15, "completed": False, "xp_reward": 75},
    {"name": "Move mouse 1000 pixels", "condition": lambda: stats["mouse_distance"], "target": 1000, "completed": False, "xp_reward": 75},
    {"name": "Right click 5 times", "condition": lambda: stats["Button.right"], "target": 5, "completed": False, "xp_reward": 75},
    
    # Mid game quests
    {"name": "Type 100 characters", "condition": lambda: stats["key_press_count"], "target": 100, "completed": False, "xp_reward": 200},
    {"name": "Click 50 times", "condition": lambda: stats["Button.left"], "target": 50, "completed": False, "xp_reward": 200},
    {"name": "Move mouse 2000 pixels", "condition": lambda: stats["mouse_distance"], "target": 2000, "completed": False, "xp_reward": 200},
    {"name": "Use all mouse buttons", "condition": lambda: min(stats["Button.left"], stats["Button.right"], stats["Button.middle"]), "target": 10, "completed": False, "xp_reward": 150},
    
    # Mid-Late game quests
    {"name": "Type 250 characters", "condition": lambda: stats["key_press_count"], "target": 250, "completed": False, "xp_reward": 300},
    {"name": "Click 100 times", "condition": lambda: stats["Button.left"], "target": 100, "completed": False, "xp_reward": 300},
    {"name": "Move mouse 5000 pixels", "condition": lambda: stats["mouse_distance"], "target": 5000, "completed": False, "xp_reward": 300},
    {"name": "Right click 25 times", "condition": lambda: stats["Button.right"], "target": 25, "completed": False, "xp_reward": 300},
    {"name": "Middle click 10 times", "condition": lambda: stats["Button.middle"], "target": 10, "completed": False, "xp_reward": 300},
    
    # Late game quests
    {"name": "Type 1000 characters", "condition": lambda: stats["key_press_count"], "target": 1000, "completed": False, "xp_reward": 500},
    {"name": "Click 200 times", "condition": lambda: stats["Button.left"], "target": 200, "completed": False, "xp_reward": 500},
    {"name": "Move mouse 10000 pixels", "condition": lambda: stats["mouse_distance"], "target": 10000, "completed": False, "xp_reward": 500},
    {"name": "Master of all inputs", "condition": lambda: min(stats["key_press_count"]//100, stats["Button.left"]//50, stats["mouse_distance"]//1000), "target": 5, "completed": False, "xp_reward": 1000},
    
    # End game quests
    {"name": "Type 5000 characters", "condition": lambda: stats["key_press_count"], "target": 5000, "completed": False, "xp_reward": 1000},
    {"name": "Click 1000 times", "condition": lambda: stats["Button.left"], "target": 1000, "completed": False, "xp_reward": 1000},
    {"name": "Move mouse 50000 pixels", "condition": lambda: stats["mouse_distance"], "target": 50000, "completed": False, "xp_reward": 1000},
    {"name": "Right click 200 times", "condition": lambda: stats["Button.right"], "target": 200, "completed": False, "xp_reward": 1000},
    {"name": "Middle click 100 times", "condition": lambda: stats["Button.middle"], "target": 100, "completed": False, "xp_reward": 1000},
    {"name": "Ultimate Master", "condition": lambda: min(stats["key_press_count"]//500, stats["Button.left"]//200, stats["Button.right"]//100, stats["Button.middle"]//50, stats["mouse_distance"]//5000), "target": 5, "completed": False, "xp_reward": 2000},
]

def getCurrentQuests():
    return [quest for quest in quests if not quest["completed"] and quest["condition"]() < quest["target"]]

def getCompletedQuests():
    return [quest for quest in quests if quest["completed"] or quest["condition"]() >= quest["target"]]

def updateQuests():
    for quest in quests:
        if not quest["completed"] and quest["condition"]() >= quest["target"]:
            quest["completed"] = True
            stats["hero_xp"] += quest["xp_reward"]
            logEvent(f"Quest Completed: {quest['name']} (+{quest['xp_reward']} XP)")