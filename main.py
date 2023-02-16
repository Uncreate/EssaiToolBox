import configparser
import threading
import tkinter as tk
from tkinter import ttk
import subprocess
import os
# Import modules
import notebook_displays
import builder, ordering, holder_viewer
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
    subprocess.run([ecp_path])

def batch_run():
    thread1 = threading.Thread(target=batch_run_thread)
    thread1.start()

def batch_run_thread():
    os.system("tooltest.bat")

def about():
    about = tk.Toplevel(root)
    about.geometry("250x250")
    tk.Label(about, text="Essai Tool Box").pack(pady=(20,5))
    tk.Label(about, text="Created by 3v3r 0dd").pack(pady=(20,0))
    tk.Label(about, text="Copyright© 2023").pack(pady=(0,10))

# Create Root Window
root = tk.Tk()
root.title("Essai Tool Box")
root.geometry("1400x800")
root.iconbitmap("toolbox.ico")
# Create Menu Bar
menu_bar = tk.Menu(root)
utility_menu = tk.Menu(menu_bar, tearoff=0)
utility_menu.add_command(label="Run Tool.t Gatherer", command=batch_run)
utility_menu.add_command(label="Run Essai Control Panel", command=ecp_run)
menu_bar.add_cascade(label="External Programs", menu=utility_menu)

menu_bar.add_command(label="About", command=about)
menu_bar.add_command(label="Exit", command=root.destroy)
root.config(menu=menu_bar)
# Create Status Bar
statusvar = tk.StringVar()
statusvar.set("Ready...")
sbar = tk.Label(root, textvariable=statusvar, relief=tk.SUNKEN, anchor="e")
sbar.pack(side=tk.BOTTOM, fill=tk.X)
display = ttk.Notebook(root)
display.pack(padx=10,pady=10,fill="both",expand=True)
frame1 = notebook_displays.OffsetUtilities(display, statusvar, sbar)
frame2 = ordering.ToolOrder(display)
frame3 = notebook_displays.Home(display)
frame4 = builder.ViewOrders(display)
frame5 = holder_viewer.ToolHolderViewer(display)
frame1.pack()   
frame2.pack()
frame3.pack()
frame4.pack(expand=True)
frame5.pack()

display.add(frame3, text="Home")
display.add(frame1, text="Tool.t Utilies")
display.add(frame4, text="Tool Builder")
display.add(frame2, text="Tool Order")
display.add(frame5, text="Tool Holder Viewer")


root.mainloop()