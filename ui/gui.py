import tkinter as tk
from tkinter import ttk, StringVar

from core.stats import stats, saveStats
from core.hero import levelUp
from core.quests import updateQuestsAndAchievements
from core.quests import quests,achievements

from ui.logs import setupLog
from ui.config import importSave,exportSave,resetSave

mainGui = None
notebook = None

key_var = None
click_var = None
distance_var = None
level_var = None
xp_var = None

# GUI Setup
def initGUI(): 
    global mainGui,notebook
    mainGui = tk.Tk()
    mainGui.iconbitmap("icon.ico")
    mainGui.title("Bullshitjob Quest")

    # Tabs
    notebook = ttk.Notebook(mainGui)
    notebook.pack(padx=10, pady=10, expand=True)

    initTabs()
    updateTabs()

    return mainGui

def initTabs():
    global key_var,click_var,distance_var,level_var,xp_var, quest_progress, achievement_progress, always_on_top_var, hero_level_progress

    # Adventure Tab
    adventure_tab = ttk.Frame(notebook)
    notebook.add(adventure_tab, text="Adventure")
    setupLog(adventure_tab)

    # Quest Tab
    quest_tab = ttk.Frame(notebook)
    notebook.add(quest_tab, text="Quests")

    quest_progress = [tk.DoubleVar() for _ in quests]
    for i, quest in enumerate(quests):
        ttk.Label(quest_tab, text=quest["name"]).pack(anchor="w", padx=10)
        ttk.Progressbar(quest_tab, variable=quest_progress[i], maximum=100).pack(fill="x", padx=10, pady=5)

    # Achievements Tab
    achievement_tab = ttk.Frame(notebook)
    notebook.add(achievement_tab, text="Achievements")

    achievement_progress = [tk.DoubleVar() for _ in achievements]
    for i, achievement in enumerate(achievements):
        ttk.Label(achievement_tab, text=achievement["name"]).pack(anchor="w", padx=10)
        ttk.Progressbar(achievement_tab, variable=achievement_progress[i], maximum=100).pack(fill="x", padx=10, pady=5)

    # Hero Tab
    hero_tab = ttk.Frame(notebook)
    notebook.add(hero_tab, text="Hero")

    key_var = StringVar(value=f"Keys Pressed: {stats['key_press_count']}")
    click_var = StringVar(value=f"Mouse Clicks: {stats['mouse_click_count']}")
    distance_var = StringVar(value=f"Mouse Distance: {stats['mouse_distance']:.2f} pixels")
    level_var = StringVar(value=f"Level: {stats['hero_level']}")
    xp_var = StringVar(value=f"XP: {stats['hero_xp']}/{stats['xp_threshold']}")

    tk.Label(hero_tab, textvariable=key_var, font=("Helvetica", 14)).pack(pady=5)
    tk.Label(hero_tab, textvariable=click_var, font=("Helvetica", 14)).pack(pady=5)
    tk.Label(hero_tab, textvariable=distance_var, font=("Helvetica", 14)).pack(pady=5)
    tk.Label(hero_tab, textvariable=level_var, font=("Helvetica", 14)).pack(pady=5)
    tk.Label(hero_tab, textvariable=xp_var, font=("Helvetica", 14)).pack(pady=5)
    hero_level_progress = tk.DoubleVar()
    ttk.Progressbar(hero_tab, variable=hero_level_progress, maximum=100).pack(fill="x", padx=10, pady=5)

    # Inventory Tab
    inventory_tab = ttk.Frame(notebook)
    notebook.add(inventory_tab, text="Inventory")

    inventory_var = StringVar(value="No items yet.")
    tk.Label(inventory_tab, textvariable=inventory_var, font=("Helvetica", 14), justify="left").pack(pady=5)

    # Config Tab
    config_tab = ttk.Frame(notebook)
    notebook.add(config_tab, text="Config")

    tk.Button(config_tab, text="Import Save", command=importSave).pack(pady=5)
    tk.Button(config_tab, text="Export Save", command=exportSave).pack(pady=5)
    tk.Button(config_tab, text="Reset datas", command=resetSave).pack(pady=5)

    # Boolean variable for Always on Top
    always_on_top_var = tk.BooleanVar(value=False)

    # Add Checkbutton for Always on Top
    tk.Checkbutton(config_tab, text="Always on Top", variable=always_on_top_var, command=toggle_always_on_top).pack(pady=5)

# Update GUI
def updateTabs():
    #stats["hero_xp"] += stats["key_press_count"] + stats["mouse_click_count"] + int(stats["mouse_distance"] // 100)
    levelUp()
    updateQuestsAndAchievements()

    # Hero Tab
    key_var.set(f"Keys Pressed: {stats['key_press_count']}")
    click_var.set(f"Mouse Clicks: {stats['mouse_click_count']}")
    distance_var.set(f"Mouse Distance: {stats['mouse_distance']:.2f} pixels")
    level_var.set(f"Level: {stats['hero_level']}")
    xp_var.set(f"XP: {stats['hero_xp']}/{stats['xp_threshold']}")
    hero_level_progress.set(stats['hero_xp'] / stats['xp_threshold'] * 100)

     # Quest Tab
    for i, quest in enumerate(quests):
        quest_progress[i].set(quest["condition"]() / quest["target"] * 100)

    # Achievements Tab
    for i, achievement in enumerate(achievements):
        achievement_progress[i].set(achievement["condition"]() / achievement["target"] * 100)

    saveStats()
    mainGui.after(100, updateTabs)

def toggle_always_on_top():
    mainGui.wm_attributes("-topmost", always_on_top_var.get())