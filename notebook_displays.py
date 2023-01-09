import tkinter as tk
from tkinter import ttk
import tool_table_parser as ttp

class OffsetUtilities(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack()

        # create a label
        label = tk.Label(self, text="This is MyFrame")
        label.pack()

        # create a button that will raise the Main frame when clicked
        button = tk.Button(self, text="Parse Tool.t files", command=self.tool_dot_t)
        button.pack()

    def tool_dot_t(self, statusvar, sbar):
        statusvar.set("Busy..")
        sbar.update()
        ttp.main()
        statusvar.set("Ready...")

class ToolOrder(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack()

        # create a label
        label = tk.Label(self, text="different but the same")
        label.pack()

        # create a button that will raise the Main frame when clicked
        button = tk.Button(self, text="Go to Main", command=self.pack_forget)
        button.pack()

    def tool_dot_t(self, statusvar, sbar):
        statusvar.set("Busy..")
        sbar.update()
        ttp.main()
        statusvar.set("Ready...")

class Home(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack()

        