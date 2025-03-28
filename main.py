import threading

from core.stats import initStats, loadStats
from core.quests import initQuests
from ui.gui import initGUI, updateTabs
from core.inputs import startListeners

def main():
    # Initialize everything in the correct order
    loadStats()  # Load existing stats first
    initStats()  # Then initialize any missing stats
    initQuests()
    
    # GUI Setup
    mainGui = initGUI()
    
    # Start listeners and GUI loop
    listener_thread = threading.Thread(target=startListeners, daemon=True)
    listener_thread.start()
    
    mainGui.after(100, updateTabs)
    mainGui.mainloop()

if __name__ == "__main__":
    main()