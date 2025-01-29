import threading

from core.stats import loadStats
from core.event_handlers import start_listeners

from ui.gui import initGUI,updateTabs

# Load stats on startup
loadStats()

# GUI Setup
mainGui = initGUI()

# Start listeners and GUI loop
listener_thread = threading.Thread(target=start_listeners, daemon=True)
listener_thread.start()

mainGui.after(100, updateTabs)
mainGui.mainloop()