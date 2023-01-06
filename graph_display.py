import tkinter as tk
from tkinter import ttk

class MyFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.pack()

        # create a label
        label = tk.Label(self, text="This is MyFrame")
        label.pack()

        # create a button that will raise the Main frame when clicked
        button = tk.Button(self, text="Go to Main", command=lambda: self.pack_forget())
        button.pack()

