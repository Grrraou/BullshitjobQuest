import threading

from core.stats import load_stats
from core.event_handlers import start_listeners

from ui.gui import initGUI,updateTabs

# Load stats on startup
load_stats()

# GUI Setup
mainGui = initGUI()

# Start listeners and GUI loop
listener_thread = threading.Thread(target=start_listeners, daemon=True)
listener_thread.start()

mainGui.after(100, updateTabs)
mainGui.mainloop()