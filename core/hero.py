from core.stats import stats
from ui.logs import logEvent

def levelUp():
    while stats["hero_xp"] >= stats["xp_threshold"]:
        stats["hero_xp"] -= stats["xp_threshold"]
        stats["hero_level"] += 1
        stats["xp_threshold"] = int(stats["xp_threshold"] * 1.5)
        logEvent(f"Level Up! Hero is now level {stats['hero_level']}")