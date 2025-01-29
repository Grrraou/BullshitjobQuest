from tkinter import filedialog, messagebox
from core.stats import load_stats, save_stats

def import_save():
    filepath = filedialog.askopenfilename(title="Import Save File", filetypes=[("JSON Files", "*.json")])
    if filepath:
        load_stats(filepath)
        messagebox.showinfo("Import Successful", "Save file imported successfully!")

def export_save():
    filepath = filedialog.asksaveasfilename(title="Export Save File", defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if filepath:
        save_stats(filepath)
        messagebox.showinfo("Export Successful", "Save file exported successfully!")
