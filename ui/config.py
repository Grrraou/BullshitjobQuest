import tkinter as tk
from tkinter import filedialog, messagebox
from core.stats import loadStats, saveStats, resetStats

def importSave():
    filepath = filedialog.askopenfilename(title="Import Save File", filetypes=[("JSON Files", "*.json")])
    if filepath:
        loadStats(filepath)
        messagebox.showinfo("Import Successful", "Save file imported successfully!")

def exportSave():
    filepath = filedialog.asksaveasfilename(title="Export Save File", defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if filepath:
        saveStats(filepath)
        messagebox.showinfo("Export Successful", "Save file exported successfully!")

def resetSave():
    root = tk.Tk()
    root.withdraw()
    if (messagebox.askyesno("Reset datas", "Are you sure ?")):
        if (messagebox.askyesno("Backup", "Want a backup first ?")):
            exportSave()
        resetStats()
    