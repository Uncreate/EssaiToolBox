import tkinter as tk
from tkinter import ttk
import configparser

# Import modules

import tool_table_parser as ttp
from graph_display import MyFrame

# Load Configuration File
config = configparser.ConfigParser()
config.read('config.ini')

tooldott_path = config['PATHS']['tool_t_path']
ecp_path = config['PATHS']['ecp']

# Define Functions
def ecp_run():
    statusvar.set("Busy...")
    sbar.update()
    import subprocess
    subprocess.run([ecp_path])
    statusvar.set("Ready...")

def tool_dot_t():
    statusvar.set("Busy..")
    sbar.update()
    ttp.main()
    statusvar.set("Ready...")

def about():
    about = tk.Toplevel(root)
    about.geometry("250x250")
    tk.Label(about, text="Essai Tool Box").pack(pady=(20,5))
    tk.Label(about, text="Created by 3v3r 0dd").pack(pady=(20,0))
    tk.Label(about, text="Copyright© 2023").pack(pady=(0,10))

def raise_frame():
    frame = MyFrame(root)
    frame.tkraise()

# Create Root Window
root = tk.Tk()
root.geometry("1200x800")
root.title("Essai Tool Box")

# Create Menu Bar
menu_bar = tk.Menu(root)
utility_menu = tk.Menu(menu_bar, tearoff=0)
utility_menu.add_command(label="Graph DL and DR values ", command=tool_dot_t)
utility_menu.add_command(label="Run Essai Control Panel", command=ecp_run)
menu_bar.add_cascade(label="Utilities", menu=utility_menu)
menu_bar.add_command(label="About", command=about)
menu_bar.add_command(label="Exit", command=root.destroy)
root.config(menu=menu_bar)

# Create Button
button = tk.Button(root, text="Raise MyFrame", command=raise_frame)
button.pack()

# Create Status Bar
statusvar = tk.StringVar()
statusvar.set("Awaiting Your Command")
sbar = tk.Label(root, textvariable=statusvar, relief=tk.SUNKEN, anchor="e")
sbar.pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()