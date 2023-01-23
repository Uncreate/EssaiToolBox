import configparser
import json
import os
import tkinter as tk
from tkinter import ttk
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from datetime import timedelta
import tool_table_parser as ttp
from test import MainApp
import csv
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
        self.fig, self.ax = plt.subplots()

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
        #tk.Checkbutton(self, text="Include history data", variable=self.include_history).grid(row=4, column=0)
        
        

    def tool_dot_t(self):
        self.statusvar.set("Busy..")
        self.sbar.update()
        ttp.process_files(self.tooldott_path)
        self.statusvar.set("Ready...")

    def create_chart(self):
        if hasattr(self, 'chart_window'):
            self.chart_window.destroy()
        self.chart_window = tk.LabelFrame(self, text=(f"{self.selected_machine.get()} DL and DR Offsets"))
        # self.chart_window.text=(f"{self.selected_machine.get()} DL and DR Offsets")
        self.chart_window.grid()
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
        dr_colors = []
        for dr in dr_data:
            if dr > 0.01:
                dr_colors.append('red')
            elif dr > 0.005:
                dr_colors.append('orange')
            elif dr > 0:
                dr_colors.append('green')
            else:
                dr_colors.append('blue')
        axs[1].bar(tool_num, dr_data, color=dr_colors)
        axs[1].legend()
        axs[1].set_xticklabels(tool_num, rotation=45)
        axs[1].grid(True, axis='y', linestyle='-.', linewidth=0.5)
        tk.Label(self.chart_window, text="Display Tool History").pack()
        self.tool_combo = ttk.Combobox(self.chart_window, values=tool_num, state="readonly")
        self.tool_combo.pack()
        self.tool_combo.bind("<<ComboboxSelected>>", self.generate_tool_chart)
        canvas = FigureCanvasTkAgg(fig, master=self.chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack()
    def generate_tool_chart(self, event):
        selected_tool = self.tool_combo.get()
        tool_data = self.data[self.selected_machine.get()][selected_tool]

        # extract the DL, DR and timestamp data for the selected tool
        dl_data = [measurement['DL'] for measurement in tool_data]
        dr_data = [measurement['DR'] for measurement in tool_data]
        timestamp_data = [measurement['Timestamp'] for measurement in tool_data]
        # timestamp_data = [datetime.datetime.strptime(measurement['Timestamp'], '%Y-%m-%d %H:%M') for measurement in tool_data]
        print(dl_data)
        print(timestamp_data)
        # create a new figure
        fig, ax = plt.subplots()
        ax.set_title(f'{self.selected_machine.get()} Tool {selected_tool} Offset History')
        ax.set_xlabel('Timestamp')
        ax.set_ylabel('Offset')
        ax.grid(True, axis='y', linestyle='--', linewidth=0.5)
        #ax.xaxis_date()
        #ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %I:%M'))
        #ax.xaxis.set_major_locator(mdates.AutoDateLocator())

        # plot the DL and DR data
        ax.plot(timestamp_data, dl_data, '.-', label='DL')
        ax.plot(timestamp_data, dr_data, '.-', label='DR')
        ax.legend()
        plt.tight_layout()

        # check if a tool_window already exists, if so destroy it
        if hasattr(self, 'tool_window'):
            self.tool_window.destroy()

        # create a new Toplevel window for the selected tool
        self.tool_window = tk.Toplevel(self)
        self.tool_window.title(f"{selected_tool} Measurements")
        self.tool_window.iconbitmap("toolbox.ico")
        # add the new figure to the tool_window
        canvas = FigureCanvasTkAgg(fig, master=self.tool_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)




class ToolOrder(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.file_name = r"C:\\EssaiControlPanel\\excel\\ToolDbEditorlog_ToolItems.csv"
        self.items = self.read_data_from_csv()
        self.tool_listbox = tk.Listbox(self)
        self.populate_listbox()
        self.tool_listbox.grid()
        self.create_widgets()
        self.set_default_values()
        self.position_widgets()
        self.pack()

    def read_data_from_csv(self):
        items = []
        try:
            with open(self.file_name, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                items.extend(iter(reader))
        except FileNotFoundError:
            print("File not found")
        except Exception:
            print("An error occurred while reading the file")
        return items

    def populate_listbox(self):
        for i in range(1, len(self.items)):
            self.tool_listbox.insert(tk.END, self.items[i][1])

    def create_widgets(self):
        self.name_label = ttk.Label(self, text="Name:")
        self.name_entry = ttk.Entry(self)
        self.machine_label = ttk.Label(self, text="Machine:")
        self.machine_combo = ttk.Combobox(self, values=[f"HC-{i:02d}" for i in range(1,31)])
        self.needed_by_label = ttk.Label(self, text="Needed by:")
        self.needed_by_date = ttk.Combobox(self, values=["Today", "Tomorrow", "Day after tomorrow"])
        self.needed_by_hour = tk.Spinbox(self, from_=1, to=12)
        self.needed_by_minute = tk.Spinbox(self, from_=0, to=59)
        self.needed_by_am_pm = ttk.Combobox(self, values=["AM", "PM"])
        self.comments_label = ttk.Label(self, text="Comments:")
        self.comments_text = tk.Text(self)

    def set_default_values(self):
        now = datetime.datetime.now()
        self.needed_by_date.set("Today")
        self.needed_by_hour.delete(0, "end")
        self.needed_by_hour.insert(0, (now.hour % 12) + 1)
        self.needed_by_minute.delete(0, "end")
        self.needed_by_minute.insert(0, now.minute)
        self.needed_by_am_pm.set("AM" if now.hour < 12 else "PM")

    def position_widgets(self):
        self.name_label.grid(row=0, column=0, sticky="W")
        self.name_entry.grid(row=0, column=1)
        self.machine_label.grid(row=1, column=0, sticky="W")
        self.machine_combo.grid(row=1, column=1)
        self.needed_by_label.grid(row=2, column=0, sticky="W")
        self.needed_by_date.grid(row=2, column=1)
        self.needed_by_hour.grid(row=2, column=2)
        self.needed_by_minute.grid(row=2, column=3)
        self.needed_by_am_pm.grid(row=2, column=4)
        self.comments_label.grid(row=3, column=0, sticky="W")
        self.comments_text.grid(row=3, column=1)


class Home(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack()
        MainApp.pack(self)
