import threading

from core.stats import loadStats
from core.inputs import startListeners

from ui.gui import initGUI,updateTabs

# Load stats on startup
loadStats()

# GUI Setup
mainGui = initGUI()

# Start listeners and GUI loop
listener_thread = threading.Thread(target=startListeners, daemon=True)
listener_thread.start()

mainGui.after(100, updateTabs)
mainGui.mainloop()