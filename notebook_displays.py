import json
import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
class GraphFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        with open("./Data/tooldott/offsets.json", "r") as f:
            data = json.load(f)

        x = []
        DL_y = []
        DR_y = []

        for key in data["HP-02"]:
            x.append(int(key))
            DL_y.append(data["HP-02"][key][0]["DL"])
            DR_y.append(data["HP-02"][key][0]["DR"])

        fig = plt.figure()
        plt.plot(x, DL_y, label="DL")
        plt.plot(x, DR_y, label="DR")
        plt.legend()

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0)