import tkinter as tk
from tkinter import ttk, StringVar
import os

from core.stats import stats, saveStats
from core.hero import levelUp
from core.quests import updateQuests, quests, getCurrentQuests, getCompletedQuests
from core.achievements import updateAchievements,achievements

from ui.logs import setupLog
from ui.config import importSave,exportSave,resetSave

mainGui = None
notebook = None
header_frame = None  # Add global header_frame
safe_for_work_var = None  # Add global safe_for_work_var

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
most_used_key_var = None  # Add most_used_key_var to globals

# Initialize quest tracking variables
quest_progress = {}
quest_labels = {}

# GUI Setup
def initGUI(): 
    global mainGui, notebook, header_frame
    mainGui = tk.Tk()
    try:
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "icon.ico")
        mainGui.iconbitmap(icon_path)
    except Exception as e:
        print(f"Could not load icon: {e}")
    mainGui.title("Bullshitjob Quest")
    mainGui.option_add("*Font", ("Fixedsys", 14))
    style = ttk.Style()
    style.configure("TNotebook.Tab", font=("Fixedsys", 14))

    # Create main container frame
    main_container = ttk.Frame(mainGui)
    main_container.pack(fill="both", expand=True)

    # Create header frame
    header_frame = tk.Frame(main_container, bg="lightgray")
    
    # Create notebook frame
    notebook_frame = ttk.Frame(main_container)
    notebook_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Initialize header
    initHeader(header_frame)
    
    # Initialize notebook
    notebook = ttk.Notebook(notebook_frame)
    notebook.pack(fill="both", expand=True)

    initTabs()
    updateTabs()

    # Apply initial SafeForWork state
    if stats["safe_for_work"]:
        toggleSafeForWork()
    else:
        header_frame.pack(fill="x", pady=5)

    return mainGui

def initHeader(header_frame):
    global level_var, xp_var, hero_level_progress

    level_var = StringVar(value=f"Level: {stats['hero_level']}")
    tk.Label(header_frame, textvariable=level_var).pack(pady=5)
    xp_var = StringVar(value=f"XP: {stats['hero_xp']}/{stats['xp_threshold']}")
    xp_label = tk.Label(header_frame, textvariable=xp_var, bg="lightgray")
    xp_label.pack(pady=5)
    hero_level_progress = tk.DoubleVar()
    ttk.Progressbar(header_frame, variable=hero_level_progress, maximum=100).pack(fill="x", padx=10, pady=5)

def initTabs():
    global quest_progress, achievement_progress, always_on_top_var, updateQuestDisplay, stats_tab, config_tab, visible_tabs, safe_for_work_var

    # Store references to all tabs
    visible_tabs = {}

    # Logs Tab
    logs_tab = ttk.Frame(notebook)
    visible_tabs["logs"] = logs_tab
    notebook.add(logs_tab, text="📜Logs", padding=10)
    setupLog(logs_tab)

    # Quest Tab
    quest_tab = ttk.Frame(notebook)
    visible_tabs["quest"] = quest_tab
    notebook.add(quest_tab, text="🎯Quests", padding=10)

    # Create sub-notebook for quests
    quest_notebook = ttk.Notebook(quest_tab)
    quest_notebook.pack(fill="both", expand=True, padx=10, pady=5)

    # Current Quests Tab
    current_quests_frame = create_scrollable_tab("Current Quests", lambda frame: None)
    quest_notebook.add(current_quests_frame, text="Current Quests")

    # Completed Quests Tab
    completed_quests_frame = create_scrollable_tab("Completed Quests", lambda frame: None)
    quest_notebook.add(completed_quests_frame, text="Completed Quests")

    def updateQuestDisplay():
        # Get the content frames from the scrollable tabs
        current_content = current_quests_frame.winfo_children()[0].winfo_children()[0]
        completed_content = completed_quests_frame.winfo_children()[0].winfo_children()[0]

        # Clear existing widgets
        for widget in current_content.winfo_children():
            widget.destroy()
        for widget in completed_content.winfo_children():
            widget.destroy()

        # Update current quests
        for quest in getCurrentQuests():
            quest_id = quest["name"]
            if quest_id not in quest_progress:
                quest_progress[quest_id] = tk.DoubleVar()
                quest_labels[quest_id] = StringVar()
            
            ttk.Label(current_content, textvariable=quest_labels[quest_id]).pack(anchor="w", padx=10)
            ttk.Progressbar(current_content, variable=quest_progress[quest_id], maximum=100).pack(fill="x", padx=10, pady=5)
            ttk.Label(current_content, text=f"Reward: {quest['xp_reward']} XP").pack(anchor="w", padx=10)

        # Update completed quests
        for quest in getCompletedQuests():
            quest_id = quest["name"]
            if quest_id not in quest_labels:
                quest_labels[quest_id] = StringVar()
            
            ttk.Label(completed_content, textvariable=quest_labels[quest_id]).pack(anchor="w", padx=10)
            ttk.Label(completed_content, text="✓ Completed").pack(anchor="w", padx=10)
            ttk.Label(completed_content, text=f"Reward: {quest['xp_reward']} XP").pack(anchor="w", padx=10, pady=5)

        # Update scroll regions
        current_quests_frame.winfo_children()[0].config(scrollregion=current_quests_frame.winfo_children()[0].bbox("all"))
        completed_quests_frame.winfo_children()[0].config(scrollregion=completed_quests_frame.winfo_children()[0].bbox("all"))

    # Initial quest display setup
    updateQuestDisplay()

    # Achievements Tab
    achievement_tab = ttk.Frame(notebook)
    visible_tabs["achievement"] = achievement_tab
    notebook.add(achievement_tab, text="🏆Achievements", padding=10)

    achievement_progress = [tk.DoubleVar() for _ in achievements]
    for i, achievement in enumerate(achievements):
        ttk.Label(achievement_tab, text=achievement["name"]).pack(anchor="w", padx=10)
        ttk.Progressbar(achievement_tab, variable=achievement_progress[i], maximum=100).pack(fill="x", padx=10, pady=5)

    # Stats Tab
    stats_tab = create_scrollable_tab("📊Stats", initStatsTab)
    visible_tabs["stats"] = stats_tab
    notebook.add(stats_tab, text="📊Stats", padding=10)

    # Inventory Tab
    inventory_tab = ttk.Frame(notebook)
    visible_tabs["inventory"] = inventory_tab
    notebook.add(inventory_tab, text="💰Inventory", padding=10)

    inventory_var = StringVar(value="No items yet.")
    tk.Label(inventory_tab, textvariable=inventory_var, justify="left").pack(pady=5)

    # Config Tab
    config_tab = ttk.Frame(notebook)
    visible_tabs["config"] = config_tab
    notebook.add(config_tab, text="⚙️Config", padding=10)

    tk.Button(config_tab, text="⬇️Import", command=importSave).pack(pady=5)
    tk.Button(config_tab, text="⬆️Export", command=exportSave).pack(pady=5)
    tk.Button(config_tab, text="Reset datas", command=resetSave).pack(pady=5)

    # Boolean variables for checkboxes
    always_on_top_var = tk.BooleanVar(value=False)
    safe_for_work_var = tk.BooleanVar(value=stats["safe_for_work"])  # Initialize from stats

    # Add Checkbuttons
    tk.Checkbutton(config_tab, text="Always on Top", variable=always_on_top_var, command=toggle_always_on_top).pack(pady=5)
    tk.Checkbutton(config_tab, text="Safe For Work Mode", variable=safe_for_work_var, command=toggleSafeForWork).pack(pady=5)

def get_key_sort_order(key):
    # Convert key to string if it's a tuple
    if isinstance(key, tuple):
        key_str = key[0]
    else:
        key_str = str(key)
    
    # Handle special cases for number pad keys
    if key_str == 'Key.numlock':
        return (1, 'NumLock')  # Put NumLock with numbers
    elif key_str.startswith('Key.numpad'):
        # Extract the number from numpad key
        num = key_str.replace('Key.numpad', '')
        return (1, f'NumPad{num}')  # Put numpad numbers with numbers
    elif key_str.startswith('Key.'):
        return (3, key_str)  # Special keys last
    
    # Define the order of different key types
    if key_str.isalpha():
        return (0, key_str.lower())  # Alphabetical keys first, case-insensitive
    elif key_str.isdigit():
        return (1, key_str)  # Numerical keys second
    elif key_str in "!@#$%^&*()_+-=[]{}|;:,.<>?/~`":
        return (2, key_str)  # Punctuation third
    else:
        return (3, key_str)  # Special keys last

def format_key_display(key):
    if isinstance(key, tuple):
        key_str = key[0]
    else:
        key_str = str(key)
    
    # Handle special cases for number pad keys
    if key_str == 'Key.numlock':
        return 'NumLock'
    elif key_str.startswith('Key.numpad'):
        num = key_str.replace('Key.numpad', '')
        return f'NumPad{num}'
    elif key_str.startswith('Key.'):
        return key_str.replace('Key.', '')
    else:
        return key_str

def create_scrollable_tab(tab_name, content_func):
    # Create main frame
    main_frame = ttk.Frame(notebook)
    
    # Create canvas and scrollbar
    canvas = tk.Canvas(main_frame)
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    
    # Create content frame
    content_frame = ttk.Frame(canvas)
    
    # Configure canvas
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Pack scrollbar and canvas
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    
    # Create window in canvas
    canvas_frame = canvas.create_window((0, 0), window=content_frame, anchor="nw")
    
    # Configure content frame to expand with canvas
    def configure_frame(event):
        canvas.itemconfig(canvas_frame, width=event.width)
    canvas.bind('<Configure>', configure_frame)
    
    # Initialize content
    content_func(content_frame)
    
    # Update scroll region
    def update_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    content_frame.bind('<Configure>', update_scroll_region)
    
    # Bind mouse wheel
    def on_mousewheel(event):
        canvas.yview_scroll(-1 * int(event.delta / 120), "units")
    canvas.bind_all("<MouseWheel>", on_mousewheel)
    
    return main_frame

def initStatsTab(content_frame):
    global distance_var, key_var, left_click_var, right_click_var, middle_click_var, other_click_var, most_used_key_var, key_stats_vars, key_stats_frame

    # Create a container frame for centering
    container = ttk.Frame(content_frame)
    container.pack(fill="both", expand=True, padx=20)

    # Basic stats
    key_var = StringVar(value=f"Total Keys Pressed: {stats['key_press_count']}")
    left_click_var = StringVar(value=f"Left Clicks: {stats['Button.left']}")
    right_click_var = StringVar(value=f"Right Clicks: {stats['Button.right']}")
    middle_click_var = StringVar(value=f"Middle Clicks: {stats['Button.middle']}")
    other_click_var = StringVar(value=f"Other Clicks: {stats['Button.other']}")
    distance_var = StringVar(value=f"Mouse Distance: {stats['mouse_distance']:.2f} pixels")
    most_used_key_var = StringVar(value=f"Key: {stats['most_used_key']['key']} ({stats['most_used_key']['count']} times)")

    # Basic stats section
    ttk.Label(container, text="Basic Statistics", font=("Fixedsys", 14, "bold")).pack(pady=5)
    ttk.Label(container, textvariable=key_var).pack(pady=2)
    ttk.Label(container, textvariable=left_click_var).pack(pady=2)
    ttk.Label(container, textvariable=right_click_var).pack(pady=2)
    ttk.Label(container, textvariable=middle_click_var).pack(pady=2)
    ttk.Label(container, textvariable=other_click_var).pack(pady=2)
    ttk.Label(container, textvariable=distance_var).pack(pady=2)

    # Separator
    ttk.Separator(container, orient="horizontal").pack(fill="x", pady=10)

    # Most used key section
    ttk.Label(container, text="Most Used Key", font=("Fixedsys", 14, "bold")).pack(pady=5)
    ttk.Label(container, textvariable=most_used_key_var).pack(pady=2)

    # Separator
    ttk.Separator(container, orient="horizontal").pack(fill="x", pady=10)

    # Detailed key statistics section
    ttk.Label(container, text="Detailed Key Statistics", font=("Fixedsys", 14, "bold")).pack(pady=5)
    
    # Create a frame for key stats
    key_stats_frame = ttk.Frame(container)
    key_stats_frame.pack(fill="both", expand=True)
    
    # Add key stats labels
    key_stats_vars = {}
    for key, count in sorted(stats["key_stats"].items(), key=get_key_sort_order):
        key_str = format_key_display(key)
        key_stats_vars[key_str] = StringVar(value=f"{key_str}: {count} times")
        ttk.Label(key_stats_frame, textvariable=key_stats_vars[key_str]).pack(anchor="w", pady=1)

def updateTabs():
    levelUp()
    updateQuests()
    updateAchievements()

    # XP and level
    level_var.set(f"Level: {stats['hero_level']}")
    xp_var.set(f"XP: {stats['hero_xp']}/{stats['xp_threshold']}")
    hero_level_progress.set(stats['hero_xp'] / stats['xp_threshold'] * 100)

    # Basic stats
    key_var.set(f"Total Keys Pressed: {stats['key_press_count']}")
    left_click_var.set(f"Left Clicks: {stats['Button.left']}")
    right_click_var.set(f"Right Clicks: {stats['Button.right']}")
    middle_click_var.set(f"Middle Clicks: {stats['Button.middle']}")
    other_click_var.set(f"Other Clicks: {stats['Button.other']}")
    distance_var.set(f"Mouse Distance: {stats['mouse_distance']:.2f} pixels")

    # Most used key
    most_used_key_var.set(f"Key: {stats['most_used_key']['key']} ({stats['most_used_key']['count']} times)")

    # Update key stats
    if 'key_stats_vars' in globals() and 'key_stats_frame' in globals():
        # Clear existing labels
        for widget in key_stats_frame.winfo_children():
            widget.destroy()
        
        # Recreate labels in sorted order
        for key, count in sorted(stats["key_stats"].items(), key=get_key_sort_order):
            key_str = format_key_display(key)
            if key_str in key_stats_vars:
                key_stats_vars[key_str].set(f"{key_str}: {count} times")
            else:
                key_stats_vars[key_str] = StringVar(value=f"{key_str}: {count} times")
            ttk.Label(key_stats_frame, textvariable=key_stats_vars[key_str]).pack(anchor="w", pady=1)

    # Quest Tab
    for quest in quests:
        quest_id = quest["name"]
        if quest_id in quest_progress and not quest["completed"]:
            progress = quest["condition"]() / quest["target"] * 100
            quest_progress[quest_id].set(min(progress, 100))
            quest_labels[quest_id].set(f"{quest['name']} ({quest['condition']():.0f}/{quest['target']})")
        elif quest_id in quest_labels and quest["completed"]:
            quest_labels[quest_id].set(f"{quest['name']} ({quest['target']}/{quest['target']})")

    # Update quest display to move completed quests
    updateQuestDisplay()

    # Logs Tab
    for i, achievement in enumerate(achievements):
        achievement_progress[i].set(achievement["condition"]() / achievement["target"] * 100)

    saveStats()
    mainGui.after(100, updateTabs)

def toggle_always_on_top():
    mainGui.wm_attributes("-topmost", always_on_top_var.get())

def toggleSafeForWork():
    global notebook, header_frame, safe_for_work_var
    stats["safe_for_work"] = safe_for_work_var.get()  # Get state from checkbox
    saveStats()
    
    # Hide/show appropriate elements
    if stats["safe_for_work"]:
        # Hide header
        header_frame.pack_forget()
        # Hide all tabs except Stats and Config
        for tab_name, tab in visible_tabs.items():
            if tab_name not in ["stats", "config"]:
                notebook.forget(tab)
    else:
        # Show header
        header_frame.pack(fill="x", pady=5)
        # Show all tabs
        for tab_name, tab in visible_tabs.items():
            if tab_name not in ["stats", "config"]:
                # Get the original tab text
                tab_text = {
                    "logs": "📜Logs",
                    "quest": "🎯Quests",
                    "achievement": "🏆Achievements",
                    "inventory": "💰Inventory"
                }.get(tab_name, "")
                notebook.add(tab, text=tab_text)