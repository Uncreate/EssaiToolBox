import tkinter as tk
from tkinter import ttk
import configparser
from rename_module import rename_files
import tool_table_parser as ttp
#Load Configuration File
config = configparser.ConfigParser()
config.read('config.ini')

tooldott_path = config['PATHS']['tool_t_path']
ecp_path = config['PATHS']['ecp']

# Define Our Functions
def on_rename_clicked():
    statusvar.set("Executing Protocol: 1375")
    sbar.update()
    rename_files(tooldott_path)
    statusvar.set("Ready...")

def ecp_run():
    statusvar.set("Executing Protocol: Anthony Da Man")
    sbar.update()
    # Call EssaiControlPanel.exe using the path from the config file
    import subprocess
    subprocess.run([ecp_path])
    statusvar.set("Awaiting Your Command")

def tool_dot_t():
    statusvar.set("Busy..")
    sbar.update()
    ttp.main()
    statusvar.set("Awaiting Your Command")
def about():
    about = tk.Toplevel(root)
    about.geometry("250x250")
    text1= tk.Label(about, text="Essai Tool Box")
    text2= tk.Label(about, text="Created by 3v3r 0dd")
    text3=tk.Label(about, text="Copyright 2023")
    text1.pack(pady=(20,5))
    text2.pack(pady=(20,0))
    text3.pack(pady=(0,10))

root=tk.Tk()
root.geometry("400x400")
root.title("Essai Tool Box")

# Create a menu bar
menu_bar = tk.Menu(root)

# Create a Utilities menu and add it to the menu bar
utility_menu = tk.Menu(menu_bar, tearoff=0)
utility_menu.add_command(label="Rename Tool.T Files", command=on_rename_clicked)
utility_menu.add_command(label="Graph DL and DR values ", command=tool_dot_t)
utility_menu.add_command(label="Run Essai Control Panel", command=ecp_run)
menu_bar.add_cascade(label="Utilities", menu=utility_menu)
# Add an EXIT command
menu_bar.add_command(label="About", command=about)
menu_bar.add_command(label="Exit", command=root.destroy)
# Set the menu bar as the root window's menu bar
root.config(menu=menu_bar)



# Create a status bar at the bottom of the window.
statusvar = tk.StringVar()
statusvar.set("Awaiting Your Command")
sbar = tk.Label(root, textvariable=statusvar, relief=tk.SUNKEN, anchor="e")
sbar.pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()