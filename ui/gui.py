import tkinter as tk
from tkinter import ttk, StringVar

from core.stats import stats, saveStats
from core.hero import levelUp
from core.quests import updateQuests,quests
from core.achievements import updateAchievements,achievements

from ui.logs import setupLog
from ui.config import importSave,exportSave,resetSave

mainGui = None
notebook = None

key_var = None
left_click_var = None
right_click_var = None
middle_click_var = None
other_click_var = None
left_click_var = None
right_click_var = None
middle_click_var = None
other_click_var = None
distance_var = None
level_var = None
xp_var = None

# GUI Setup
def initGUI(): 
    global mainGui,notebook
    mainGui = tk.Tk()
    mainGui.iconbitmap("icon.ico")
    mainGui.title("Bullshitjob Quest")
    mainGui.option_add("*Font", ("Fixedsys", 14))

    initHeader()
    # Tabs
    notebook = ttk.Notebook(mainGui)
    notebook.pack(padx=10, pady=10, expand=True)

    initTabs()
    updateTabs()

    return mainGui

def initHeader():
    global level_var, xp_var, hero_level_progress

    # XP and level
    header_frame = tk.Frame(mainGui, bg="lightgray")
    header_frame.pack(fill="x", pady=5)
    level_var = StringVar(value=f"Level: {stats['hero_level']}")
    tk.Label(header_frame, textvariable=level_var).pack(pady=5)
    xp_var = StringVar(value=f"XP: {stats['hero_xp']}/{stats['xp_threshold']}")
    xp_label = tk.Label(header_frame, textvariable=xp_var, bg="lightgray")
    xp_label.pack(pady=5)
    hero_level_progress = tk.DoubleVar()
    ttk.Progressbar(header_frame, variable=hero_level_progress, maximum=100).pack(fill="x", padx=10, pady=5)

def initTabs():
    global key_var,left_click_var,right_click_var,middle_click_var,other_click_var
    global distance_var, quest_progress, achievement_progress, always_on_top_var

    # Logs Tab
    logs_tab = ttk.Frame(notebook)
    notebook.add(logs_tab, text="📜Logs")
    setupLog(logs_tab)

    # Quest Tab
    quest_tab = ttk.Frame(notebook)
    notebook.add(quest_tab, text="🎯Quests")

    quest_progress = [tk.DoubleVar() for _ in quests]
    for i, quest in enumerate(quests):
        ttk.Label(quest_tab, text=quest["name"]).pack(anchor="w", padx=10)
        ttk.Progressbar(quest_tab, variable=quest_progress[i], maximum=100).pack(fill="x", padx=10, pady=5)

    # Achievements Tab
    achievement_tab = ttk.Frame(notebook)
    notebook.add(achievement_tab, text="🏆Achievements")

    achievement_progress = [tk.DoubleVar() for _ in achievements]
    for i, achievement in enumerate(achievements):
        ttk.Label(achievement_tab, text=achievement["name"]).pack(anchor="w", padx=10)
        ttk.Progressbar(achievement_tab, variable=achievement_progress[i], maximum=100).pack(fill="x", padx=10, pady=5)

    # Stats Tab
    stats_tab = ttk.Frame(notebook)
    notebook.add(stats_tab, text="📊Stats")

    key_var = StringVar(value=f"Keys Pressed: {stats['key_press_count']}")
    left_click_var = StringVar(value=f"Left Clicks: {stats['Button.left']}")
    right_click_var = StringVar(value=f"Right Clicks: {stats['Button.right']}")
    middle_click_var = StringVar(value=f"Right Clicks: {stats['Button.middle']}")
    other_click_var = StringVar(value=f"Right Clicks: {stats['Button.other']}")
    left_click_var = StringVar(value=f"Left Clicks: {stats['Button.left']}")
    right_click_var = StringVar(value=f"Right Clicks: {stats['Button.right']}")
    middle_click_var = StringVar(value=f"Right Clicks: {stats['Button.middle']}")
    other_click_var = StringVar(value=f"Right Clicks: {stats['Button.other']}")
    distance_var = StringVar(value=f"Mouse Distance: {stats['mouse_distance']:.2f} pixels")

    tk.Label(stats_tab, textvariable=key_var).pack(pady=5)
    tk.Label(stats_tab, textvariable=left_click_var).pack(pady=5)
    tk.Label(stats_tab, textvariable=right_click_var).pack(pady=5)
    tk.Label(stats_tab, textvariable=middle_click_var).pack(pady=5)
    tk.Label(stats_tab, textvariable=other_click_var).pack(pady=5)
    tk.Label(stats_tab, textvariable=distance_var).pack(pady=5)

    # Inventory Tab
    inventory_tab = ttk.Frame(notebook)
    notebook.add(inventory_tab, text="💰Inventory")

    inventory_var = StringVar(value="No items yet.")
    tk.Label(inventory_tab, textvariable=inventory_var, justify="left").pack(pady=5)

    # Config Tab
    config_tab = ttk.Frame(notebook)
    notebook.add(config_tab, text="⚙️Config")

    tk.Button(config_tab, text="⬇️Import", command=importSave).pack(pady=5)
    tk.Button(config_tab, text="⬆️Export", command=exportSave).pack(pady=5)
    tk.Button(config_tab, text="Reset datas", command=resetSave).pack(pady=5)

    # Boolean variable for Always on Top
    always_on_top_var = tk.BooleanVar(value=False)

    # Add Checkbutton for Always on Top
    tk.Checkbutton(config_tab, text="Always on Top", variable=always_on_top_var, command=toggle_always_on_top).pack(pady=5)

# Update GUI
def updateTabs():
    levelUp()
    updateQuests()
    updateAchievements()

    # XP and level
    level_var.set(f"Level: {stats['hero_level']}")
    xp_var.set(f"XP: {stats['hero_xp']}/{stats['xp_threshold']}")
    hero_level_progress.set(stats['hero_xp'] / stats['xp_threshold'] * 100)

    # Hero Tab
    key_var.set(f"Keys Pressed: {stats['key_press_count']}")
    left_click_var.set(f"Left Clicks: {stats['Button.left']}")
    right_click_var.set(f"Right Clicks: {stats['Button.right']}")
    middle_click_var.set(f"Middle Clicks: {stats['Button.middle']}")
    other_click_var.set(f"Other Clicks: {stats['Button.other']}")
    distance_var.set(f"Mouse Distance: {stats['mouse_distance']:.2f} pixels")
    

     # Quest Tab
    for i, quest in enumerate(quests):
        quest_progress[i].set(quest["condition"]() / quest["target"] * 100)

    # Logs Tab
    for i, achievement in enumerate(achievements):
        achievement_progress[i].set(achievement["condition"]() / achievement["target"] * 100)

    saveStats()
    mainGui.after(100, updateTabs)

def toggle_always_on_top():
    mainGui.wm_attributes("-topmost", always_on_top_var.get())