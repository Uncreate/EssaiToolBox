import tkinter as tk
from tkinter import ttk
import configparser
import threading
# Import modules
import notebook_displays

# Load Configuration File
config = configparser.ConfigParser()
config.read('config.ini')

tooldott_path = config['PATHS']['tool_t_path']
ecp_path = config['PATHS']['ecp']

# Define Functions
def ecp_run():
    # Create a new thread
    thread = threading.Thread(target=ecp_run_thread)
    # Start the thread
    thread.start()

def ecp_run_thread():
    import subprocess
    subprocess.run([ecp_path])
    
def about():
    about = tk.Toplevel(root)
    about.geometry("250x250")
    tk.Label(about, text="Essai Tool Box").pack(pady=(20,5))
    tk.Label(about, text="Created by 3v3r 0dd").pack(pady=(20,0))
    tk.Label(about, text="Copyright© 2023").pack(pady=(0,10))

# Create Root Window
root = tk.Tk()
root.geometry("1200x800")
root.title("Essai Tool Box")

# Create Menu Bar
menu_bar = tk.Menu(root)
utility_menu = tk.Menu(menu_bar, tearoff=0)

utility_menu.add_command(label="Run Essai Control Panel", command=ecp_run)
menu_bar.add_cascade(label="Utilities", menu=utility_menu)

menu_bar.add_command(label="About", command=about)
menu_bar.add_command(label="Exit", command=root.destroy)
root.config(menu=menu_bar)

display = ttk.Notebook(root)
display.pack(padx=10,pady=10,fill="both",expand=True)
frame1 = notebook_displays.OffsetUtilities(display)
frame2 = notebook_displays.ToolOrder(display)
frame1.pack()
frame2.pack()
display.add(frame1, text="Tool.t Utilies")
display.add(frame2, text="Tool Order")
# Create Status Bar
statusvar = tk.StringVar()
statusvar.set("Ready...")
sbar = tk.Label(root, textvariable=statusvar, relief=tk.SUNKEN, anchor="e")
sbar.pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()