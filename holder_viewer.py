import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import os
import json
import re


class ToolHolderViewer(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.pack()

        self.create_layout()
        self.create_widgets()

    def create_layout(self):
        self.machine_select_frame = ttk.Frame(self)
        self.machine_select_frame.grid(
            row=0, column=0, padx=5, pady=5, columnspan=3, sticky="EW")
        self.machine_holders_frame = ttk.LabelFrame(self, text="Holders")
        self.machine_holders_frame.grid(
            row=1, column=0, padx=5, pady=5, sticky="NS")
        self.machine_tools_frame = ttk.LabelFrame(
            self, text="Tools in Machine")
        self.machine_tools_frame.grid(
            row=1, column=1, padx=5, pady=5, sticky="NS")
        self.tool_details_frame = ttk.LabelFrame(
            self, text="Selected Tool Details")
        self.tool_details_frame.grid(
            row=1, column=2, padx=5, pady=5, sticky="NS")
        self.program_frame = ttk.LabelFrame(self, text="Program Compatibility")
        self.program_frame.grid(row=2, column=0, padx=5,
                                pady=5, columnspan=3, sticky="EW")

    def create_widgets(self):
        self.select_label = ttk.Label(
            self.machine_select_frame, text="Select Machine")
        self.select_label.pack(side="left", padx=5, pady=5)
        self.machine_combo = ttk.Combobox(self.machine_select_frame, values=[
                                          f"HC-{i:02d}" for i in range(1, 31)])
        self.machine_combo['state'] = 'readonly'
        self.machine_combo.pack(side="left", padx=5, pady=5)
        self.machine_combo.bind("<<ComboboxSelected>>", self.on_machine_select)
        self.machine = self.machine_combo.get()
        self.show_data_button = ttk.Button(
            self.machine_select_frame, text="Show Data", command=lambda: self.get_tools(self.machine))
        self.show_data_button.pack(side="left", padx=5, pady=5)
        self.columns = ("qty", "tool_name", "holder_name")
        self.tree = ttk.Treeview(
            self.machine_tools_frame, columns=self.columns, show="headings")
        for col in self.tree["columns"]:
            self.tree.column(col, anchor="center")
        self.tree.heading("qty", text="QTY")
        self.tree.heading("tool_name", text="Tool Name")
        self.tree.heading("holder_name", text="Holder")
        self.tree.bind('<<TreeviewSelect>>', self.selected_tool)
        self.tree.pack(padx=5, pady=5, fill="both", expand=True)
        self.holder_list = tk.Listbox(self.machine_holders_frame)
        self.holder_list.pack(padx=5, pady=5)
        self.program_button = ttk.Button(
            self.program_frame, text="Select Program", command=self.program_reader)
        self.program_button.pack()

    def on_machine_select(self, event):
        self.machine = self.machine_combo.get()

    def get_tools(self, machine):
        folder_path = f'D:/Holders/{machine[3:]}'
        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                if filename.endswith('.t'):
                    file_path = os.path.join(root, filename)
                    # output_file_path = os.path.join(root, f"{filename}.json")
                    data = {}
                    with open(file_path, 'r') as f:
                        lines = f.readlines()
                        for line in lines[2:]:
                            line_data = line.split()
                            if re.match(r"^\d+$", line_data[0]) and re.match(r"^[A-Za-z]{2}\d{6}[A-Za-z]$", line_data[1]):
                                if line_data[1] in data:
                                    data[line_data[1]] += 1
                                else:
                                    data[line_data[1]] = 1
                    self.get_holder_count(data)
                    self.clear_tree()
                    self.get_tool_count(data)

    def get_holder_count(self, data):
        with open('A:/EssaiControlPanel/excel/ToolDbEditorlog_ToolItems.json', 'r') as f:
            tool_items_data = json.load(f)
        tool_item_counts = {}
        for key in data.keys():
            for item in tool_items_data["ToolItems"]:
                if item["sToolName"] == key:
                    holder_name = item["sHolderName"]
                    break
            else:
                continue
            count = data[key]
            if holder_name not in tool_item_counts:
                tool_item_counts[holder_name] = count
            else:
                tool_item_counts[holder_name] += count
        self.holder_list.delete(0, tk.END)
        for holder_name, count in tool_item_counts.items():
            item_text = f"{holder_name}: {count}"
            self.holder_list.insert(tk.END, item_text)

    def get_tool_count(self, data):
        with open('A:/EssaiControlPanel/excel/ToolDbEditorlog_ToolItems.json', 'r') as f:
            tool_items_data = json.load(f)
        items = []
        for key in data.keys():
            for item in tool_items_data["ToolItems"]:
                if item["sToolName"] == key:
                    qty = data[key]
                    tool_name = key
                    holder_name = item["sHolderName"]
                    items.append((qty, tool_name, holder_name))
        items.sort(key=lambda x: x[1])
        for i, item in enumerate(items):
            tags = ("odd", ) if i % 2 == 0 else ()
            self.tree.insert("", "end", values=item, tags=tags)


        self.tree.tag_configure("odd", background="light blue")

    def clear_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def selected_tool(self, event):
        for widget in self.tool_details_frame.winfo_children():
            widget.destroy()
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            self.record = item['values'][1]
            with open('A:/EssaiControlPanel/excel/ToolDbEditorlog_ToolItems.json', 'r') as f:
                tool_items_data = json.load(f)
            for item in tool_items_data["ToolItems"]:
                if item["sToolName"] == self.record:
                    tool_name = item["sToolName"]
                    essai_num = item["sEssaiPartNum"]
                    holder_name = item["sHolderName"]
                    tool_type = item["sToolGroupName"]
                    ohl = item["dOHL"]
                    gage_length = item["dGageLength"]
                    manufacturer = item["sToolManufacturer"]
                    edp = item["sToolEdp"]
                    diameter = item["dDia"]
                    details = {
                        "Tool Name": tool_name,
                        "Essai Part Number": essai_num,
                        "Holder Name": holder_name,
                        "Tool Type": tool_type,
                        "OHL": ohl,
                        "Gage Length": gage_length,
                        "Manufacturer": manufacturer,
                        "EDP": edp,
                        "Diameter": diameter
                    }
                    for i, (key, value) in enumerate(details.items()):
                        label = tk.Label(self.tool_details_frame,
                                         text=f"{key}: {value}")
                        label.grid(row=i, column=0, sticky="w")

    def program_reader(self):
        filename = fd.askopenfilename(
            filetypes=[('Program Files', '*.h'), ('Tool List', '*.txt')])
        with open(filename) as f:
            lines = f.readlines()
        templist = []
        for line in lines:
            myStr = line.strip()
            if results := re.findall(
                '\* - T"(.*)" =(.*) R=(.*) -- LONG= (.*)"min. #(.*) -- Angle= (.*)',
                myStr,
            ):
                matches = [match[0] for match in results]
                filtered_matches = [match for match in matches if all(str(num) not in match for num in [31, 32, 33, 34])]
                templist.extend(filtered_matches)
        self.templist = templist
        
        self.compare_files()

    def compare_files(self):
        print(self.templist)
        folder_path = 'E:/Holders/'
        folders_tool_names = {}
        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                if filename.endswith('.t'):
                    file_path = os.path.join(root, filename)
                    with open(file_path) as f:
                        content = f.readlines()
                        tool_names = []
                        for line in content[2:]:
                            line_data = line.split()
                            if len(line_data) < 2:
                                break
                            if match := re.match(r"^[A-Za-z]{2}\d{6}[A-Za-z]$", line_data[1]):
                                tool_names.append(match[0])
                if all(t in tool_names for t in self.templist):
                    folder_name = os.path.basename(root)
                    if folder_name not in folders_tool_names:
                        folders_tool_names[folder_name] = []
                    folders_tool_names[folder_name].extend(tool_names)

        for folder in folders_tool_names:
            label_text = f'HC-{folder}'
            label = tk.Label(self.program_frame, text=label_text, fg='green')
            label.pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = ToolHolderViewer(root)
    app.mainloop()
