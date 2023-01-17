import configparser
import json
import os
import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import tool_table_parser as ttp

class OffsetUtilities(ttk.Frame):
    def __init__(self, parent, statusvar, sbar):
        super().__init__(parent)
        self.statusvar = statusvar
        self.sbar = sbar
        self.pack()

        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        self.tooldott_path = self.config['PATHS']['tool_t_path']
        self.json_path = self.config['PATHS']['json_path']

        self.data = self.load_json_data()
        self.create_widgets()

    def load_json_data(self):
        with open(os.path.join(self.tooldott_path, self.json_path)) as f:
            data = json.load(f)
        return data

    def create_widgets(self):
        tk.Label(self, text="Select a machine:").grid(row=0, column=0)

        self.selected_machine = tk.StringVar()
        machine_list = list(self.data.keys())
        machine_dropdown = tk.OptionMenu(self, self.selected_machine, *machine_list)
        machine_dropdown.grid(row=1, column=0)

        tk.Button(self, text="Create Chart", command=self.create_chart).grid(row=2, column=0)
        tk.Button(self, text="Parse Tool.t files", command=self.tool_dot_t).grid(row=3, column=0, padx=10, pady=10)
        
        
    def tool_dot_t(self):
        self.statusvar.set("Busy..")
        self.sbar.update()
        ttp.process_files(self.tooldott_path)
        self.statusvar.set("Ready...")

    def create_chart(self):
        self.chart_window = tk.Toplevel(self)
        self.chart_window.title(f"{self.selected_machine.get()} DL and DR Offsets")
        machine = self.data[self.selected_machine.get()]

        dl_data = []
        dr_data = []

        for id_num, measurements in machine.items():
            dl = 0
            dr = 0
            for measurement in measurements:
                dl += measurement['DL']
                dr += measurement['DR']
            dl_data.append(dl)
            dr_data.append(dr)

        fig, axs = plt.subplots(1, 2, tight_layout=True)
        fig.set_size_inches(15, 7)
        axs[0].set_title('DL Measurements')
        axs[0].set_xlabel('Tool Number')
        axs[0].set_ylabel('Offset')
        axs[0].stem(list(machine.keys()), dl_data, markerfmt='D', label='DL')
        axs[0].legend()

        axs[1].set_title('DR Measurements')
        axs[1].set_xlabel('Tool Number')
        axs[1].set_ylabel('Offset')
        axs[1].stem(list(machine.keys()), dr_data, markerfmt='*', label='DR')
        axs[1].legend()

        canvas = FigureCanvasTkAgg(fig, master=self.chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

class ToolOrder(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack()

        # create a label
        label = tk.Label(self, text="different but the same")
        label.grid(row=0,column=0, padx=5,pady=5)

        # create a button that will raise the Main frame when clicked
        button = tk.Button(self, text="Go to Main", command=self.pack_forget)
        button.grid(row=0,column=1,padx=5,pady=5)

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