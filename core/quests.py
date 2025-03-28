from core.stats import stats
from ui.logs import logEvent

# Quest categories
CATEGORIES = {
    "left_click": "Left Click Quests",
    "right_click": "Right Click Quests",
    "key_press": "Key Press Quests",
    "mouse_distance": "Mouse Distance Quests",
    "key_combo": "Key Combination Quests"
}

# Quest definitions grouped by category
quests = [
    # Left Click Quests
    {"name": "Left Click Novice", "category": "left_click", "condition": "Button.left", "target": 5, "completed": False, "xp_reward": 10, "progress": 0, "start_value": 0},
    {"name": "Left Click Apprentice", "category": "left_click", "condition": "Button.left", "target": 50, "completed": False, "xp_reward": 50, "progress": 0, "start_value": 0},
    {"name": "Left Click Master", "category": "left_click", "condition": "Button.left", "target": 500, "completed": False, "xp_reward": 200, "progress": 0, "start_value": 0},
    {"name": "Left Click Legend", "category": "left_click", "condition": "Button.left", "target": 5000, "completed": False, "xp_reward": 1000, "progress": 0, "start_value": 0},
    
    # Right Click Quests
    {"name": "Right Click Novice", "category": "right_click", "condition": "Button.right", "target": 5, "completed": False, "xp_reward": 10, "progress": 0, "start_value": 0},
    {"name": "Right Click Apprentice", "category": "right_click", "condition": "Button.right", "target": 50, "completed": False, "xp_reward": 50, "progress": 0, "start_value": 0},
    {"name": "Right Click Master", "category": "right_click", "condition": "Button.right", "target": 500, "completed": False, "xp_reward": 200, "progress": 0, "start_value": 0},
    {"name": "Right Click Legend", "category": "right_click", "condition": "Button.right", "target": 5000, "completed": False, "xp_reward": 1000, "progress": 0, "start_value": 0},
    
    # Key Press Quests
    {"name": "Key Press Novice", "category": "key_press", "condition": "key_press_count", "target": 5, "completed": False, "xp_reward": 10, "progress": 0, "start_value": 0},
    {"name": "Key Press Apprentice", "category": "key_press", "condition": "key_press_count", "target": 50, "completed": False, "xp_reward": 50, "progress": 0, "start_value": 0},
    {"name": "Key Press Master", "category": "key_press", "condition": "key_press_count", "target": 500, "completed": False, "xp_reward": 200, "progress": 0, "start_value": 0},
    {"name": "Key Press Legend", "category": "key_press", "condition": "key_press_count", "target": 5000, "completed": False, "xp_reward": 1000, "progress": 0, "start_value": 0},
    
    # Mouse Distance Quests
    {"name": "Mouse Distance Novice", "category": "mouse_distance", "condition": "mouse_distance", "target": 1000, "completed": False, "xp_reward": 10, "progress": 0, "start_value": 0},
    {"name": "Mouse Distance Apprentice", "category": "mouse_distance", "condition": "mouse_distance", "target": 10000, "completed": False, "xp_reward": 50, "progress": 0, "start_value": 0},
    {"name": "Mouse Distance Master", "category": "mouse_distance", "condition": "mouse_distance", "target": 100000, "completed": False, "xp_reward": 200, "progress": 0, "start_value": 0},
    {"name": "Mouse Distance Legend", "category": "mouse_distance", "condition": "mouse_distance", "target": 1000000, "completed": False, "xp_reward": 1000, "progress": 0, "start_value": 0},
    
    # Key Combination Quests
    {"name": "Key Combo Novice", "category": "key_combo", "condition": "key_combo_count", "target": 5, "completed": False, "xp_reward": 10, "progress": 0, "start_value": 0},
    {"name": "Key Combo Apprentice", "category": "key_combo", "condition": "key_combo_count", "target": 50, "completed": False, "xp_reward": 50, "progress": 0, "start_value": 0},
    {"name": "Key Combo Master", "category": "key_combo", "condition": "key_combo_count", "target": 500, "completed": False, "xp_reward": 200, "progress": 0, "start_value": 0},
    {"name": "Key Combo Legend", "category": "key_combo", "condition": "key_combo_count", "target": 5000, "completed": False, "xp_reward": 1000, "progress": 0, "start_value": 0}
]

def initQuests():
    """Initialize quests and set their start values"""
    for quest in quests:
        quest["completed"] = False
        quest["progress"] = 0
        quest["start_value"] = stats[quest["condition"]]

def getCurrentQuests():
    """Get the current active quest for each category"""
    current_quests = {}
    for quest in quests:
        if not quest["completed"]:
            category = quest["category"]
            if category not in current_quests:
                current_quests[category] = quest
    return list(current_quests.values())

def getCompletedQuests():
    """Get all completed quests grouped by category"""
    completed_by_category = {}
    for quest in quests:
        if quest["completed"]:
            category = quest["category"]
            if category not in completed_by_category:
                completed_by_category[category] = []
            completed_by_category[category].append(quest)
    return completed_by_category

def updateQuests():
    """Update quest progress and check for completions"""
    for quest in quests:
        if not quest["completed"]:
            # Get current value from stats
            current_value = stats[quest["condition"]]
            
            # Calculate progress from start value
            progress = current_value - quest["start_value"]
            
            # Update quest progress
            quest["progress"] = progress
            
            # Check if quest is complete
            if progress >= quest["target"]:
                # Mark quest as completed
                quest["completed"] = True
                
                # Add XP reward
                stats["hero_xp"] += quest["xp_reward"]
                
                # Log completion
                logEvent(f"Quest completed: {quest['name']} (+{quest['xp_reward']} XP)")
                
                # Find next quest in category
                category = quest["category"]
                next_quest = None
                for q in quests:
                    if q["category"] == category and not q["completed"]:
                        next_quest = q
                        break
                
                if next_quest:
                    # Set start value for next quest
                    next_quest["start_value"] = stats[next_quest["condition"]]
                    next_quest["progress"] = 0