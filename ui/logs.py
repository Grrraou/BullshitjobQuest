import tkinter as tk

logs = None

def setupLog(tab):
    global logs
    logs = tk.Listbox(tab, height=15, font=("Courier", 10))
    logs.pack(fill="both", expand=True, padx=5, pady=5)

def logEvent(message):
    logs.insert(tk.END, message)
    logs.see(tk.END)