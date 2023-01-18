import configparser
import json
import os
import tkinter as tk
from tkinter import ttk
import subprocess
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
        
        self.include_history = tk.IntVar()
        tk.Checkbutton(self, text="Include history data", variable=self.include_history).grid(row=4, column=0)

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
        tool_num = []
        for id_num, measurements in machine.items():
            dl = 0
            dr = 0
            for measurement in measurements:
                dl += measurement['DL']
                dr += measurement['DR']
            if len(measurements) > 1 and self.include_history.get() == 1:
                for history_measurement in measurements[1:]:
                    dl += history_measurement['DL']
                    dr += history_measurement['DR']
            dl_data.append(dl)
            dr_data.append(dr)
            tool_num.append(id_num)
        fig, axs = plt.subplots(1, 2, tight_layout=True)
        fig.set_size_inches(15, 7)
        axs[0].set_title('DL Measurements')
        axs[0].set_xlabel('Tool Number')
        axs[0].set_ylabel('Offset')
        dl_colors = []
        for dl in dl_data:
            if dl > 0.01:
                dl_colors.append('red')
            elif dl > 0.005:
                dl_colors.append('orange')
            elif dl > 0:
                dl_colors.append('green')
            else:
                dl_colors.append('blue')
        axs[0].bar(tool_num, dl_data, color=dl_colors)
        axs[0].legend()
        axs[0].set_xticklabels(tool_num, rotation=45)
        axs[0].grid(True, axis='y', linestyle='-.', linewidth=0.5)

        axs[1].set_title('DR Measurements')
        axs[1].set_xlabel('Tool Number')
        axs[1].set_ylabel('Offset')
        axs[1].scatter(tool_num, dr_data, marker='*', label='DR')
        for i, txt in enumerate(dl_data):
            if txt != 0:
                axs[1].annotate(txt, (tool_num[i], dr_data[i]))
        axs[1].legend()
        axs[1].set_xticklabels(tool_num, rotation=45)

        canvas = FigureCanvasTkAgg(fig, master=self.chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

class ToolOrder(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack()

       
    

class Home(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack()
        
