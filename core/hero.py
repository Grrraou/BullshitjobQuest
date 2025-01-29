from core.stats import stats
from ui.logs import log_event

def level_up():
    while stats["hero_xp"] >= stats["xp_threshold"]:
        stats["hero_xp"] -= stats["xp_threshold"]
        stats["hero_level"] += 1
        stats["xp_threshold"] = int(stats["xp_threshold"] * 1.5)
        log_event(f"Level Up! Hero is now level {stats['hero_level']}")