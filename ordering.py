
import datetime
import json
import sqlite3
import tkinter as tk
import traceback
from tkinter import ttk
import configparser
from tkinter import messagebox
config = configparser.ConfigParser()
config.read('config.ini')

tool_items = config['PATHS']['tool_items']
db_path = config['PATHS']['tool_order_db']

class ToolOrder(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.row_count = 0
        self.cf_vars = []
        self.ct_vars = []
        self.metric_vars = []
        self.tool_order = []
        self.file_name = tool_items
        self.items = self.read_data_from_json()
        self.order_frame()
        self.create_widgets()
        self.set_default_values()
        self.tool_listbox = tk.Listbox(self.orderframe, height=20)
        self.populate_listbox()
        self.tool_listbox.grid(row=2,column=5, rowspan=6, padx=5, pady=5)
        self.position_widgets()
        self.create_search_bar()
        self.order_detail_frame()
        self.bind_listbox_double_click()
        self.submit_button = ttk.Button(self, text="Submit", command=self.submit)
        self.submit_button.grid(row=10, column=0, padx=5, pady=5, sticky="E")
        self.reset_button = ttk.Button(self, text="Reset", command=self.reset)
        self.reset_button.grid(row=10, column=1, padx=5, pady=5, sticky="W")

        self.pack()

    def submit(self):
        name = self.name_entry.get().strip()
        part = self.part_entry.get().strip()
        if not name or not part:
            messagebox.showerror("Error", "Required fields are empty")
            return

        date_str = self.needed_by_date.get()
        if date_str == "Today":
            date = datetime.datetime.now().date()
        elif date_str == "Tomorrow":
            date = (datetime.datetime.now() + datetime.timedelta(days=1)).date()
        elif date_str == "Day after tomorrow":
            date = (datetime.datetime.now() + datetime.timedelta(days=2)).date()
        else:
            date = None
        time = f"{date} {self.needed_by_hour.get()}:{self.needed_by_minute.get()} {self.needed_by_am_pm.get()}"
        comments = self.comments_text.get("1.0", tk.END).strip()
        complete = 0

        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS orders
                        (name text, machine text, part text, time text, comments text, complete integer)''')
            c.execute("INSERT INTO orders VALUES (?,?,?,?,?,?)", (name, self.machine_combo.get(), part, time, comments, complete))
            order_id = c.lastrowid

            c.execute('''CREATE TABLE IF NOT EXISTS order_detail
                        (order_id text, tool_name text,item_qty text, cf text,ct text, metric text)''')
            for item in self.tool_order:
                tool_name = item['tool_name'].strip()
                item_qty = item['item_qty'].strip()
                cf = item['cf']
                ct = item['ct']
                metric = item['metric']
                c.execute("INSERT INTO order_detail (order_id, tool_name, item_qty, cf, ct, metric) VALUES (?,?,?,?,?,?)", (order_id, tool_name, item_qty, cf, ct, metric))
        self.reset()
        self.tool_order = []

        
    def reset(self):
        # reset the name field
        self.name_entry.delete(0, tk.END)
        # reset the machine combo box
        self.machine_combo.set("Select Machine")
        # reset the part number field
        self.part_entry.delete(0, tk.END)
        # reset the time to the default
        self.set_default_values()
        # clear the comments
        self.comments_text.delete("1.0", tk.END)
        self.search_entry.delete(0, tk.END)
        self.asap_var.set(0)
        # remove anything thats been added to the order_details_frame
        for child in self.order_detail.winfo_children():
            child.destroy()

    def order_detail_frame(self):
        self.order_detail = ttk.LabelFrame(self, text='Order Details')
        self.order_detail.grid(row=0, column=2, sticky="N",padx=5,pady=5)
        tool_name = ttk.Label(self.order_detail, text='Tool Name')
        tool_name.grid(row=0, column=0,padx=5,pady=5)
        qty_lbl = ttk.Label(self.order_detail, text='QTY:')
        qty_lbl.grid(row=0, column=1, padx=5,pady=5)

    def order_frame(self):
        self.orderframe = ttk.Frame(self)
        self.orderframe.grid(row=0,column=0,padx=5,pady=5)

    def bind_listbox_double_click(self):
        self.tool_listbox.bind("<Double-Button-1>", self.add_item_to_quantity_frame)

    def add_item_to_quantity_frame(self, event):
        selected_item = self.tool_listbox.get(self.tool_listbox.curselection())
        item_label = ttk.Label(self.order_detail, text=selected_item)
        item_qty = tk.Spinbox(self.order_detail, from_=1, to=20,width=3, wrap=True)
        remove_btn = ttk.Button(self.order_detail, text="Remove", 
                                command=lambda: self.remove_item(item_label, item_qty, remove_btn, cf_checkbox, ct_checkbox, metric_checkbox))
        cf_var = tk.IntVar()
        ct_var = tk.IntVar()
        metric_var = tk.IntVar()
        cf_checkbox = ttk.Checkbutton(self.order_detail, text="Coolant Flush (CF)", variable=cf_var)
        ct_checkbox = ttk.Checkbutton(self.order_detail, text="Coolant Thru (CT)", variable=ct_var)
        metric_checkbox = ttk.Checkbutton(self.order_detail, text="Metric", variable=metric_var)

        self.row_count += 2
        item_label.grid(row=self.row_count - 1, column=0, padx=5, pady=5)
        item_qty.grid(row=self.row_count - 1, column=1, padx=5, pady=5)
        remove_btn.grid(row=self.row_count - 1, column=2, padx=5, pady=5)
        cf_checkbox.grid(row=self.row_count, column=0, padx=5, pady=5, sticky="W")
        ct_checkbox.grid(row=self.row_count, column=1, padx=5, pady=5, sticky="W")
        metric_checkbox.grid(row=self.row_count, column=2, padx=5, pady=5, sticky="W")

        item_qty.config(command=lambda: self.update_tool_order(selected_item, item_qty.get(), cf_var.get(), ct_var.get(), metric_var.get()))
        cf_checkbox.config(command=lambda: self.update_tool_order(selected_item, item_qty.get(), cf_var.get(), ct_var.get(), metric_var.get()))
        ct_checkbox.config(command=lambda: self.update_tool_order(selected_item, item_qty.get(), cf_var.get(), ct_var.get(), metric_var.get()))
        metric_checkbox.config(command=lambda: self.update_tool_order(selected_item, item_qty.get(), cf_var.get(), ct_var.get(), metric_var.get()))

        tool_order = {
        'tool_name': selected_item,
        'item_qty': item_qty.get(),
        'cf': cf_var.get(),
        'ct': ct_var.get(),
        'metric': metric_var.get()
        }
        self.tool_order.append(tool_order)
    
    def update_tool_order(self, tool_name, item_qty, cf, ct, metric):
        for tool in self.tool_order:
            if tool['tool_name'] == tool_name:
                tool['item_qty'] = item_qty
                tool['cf'] = cf
                tool['ct'] = ct
                tool['metric'] = metric

    def remove_item(self, label, entry, button,chbx1,chbx2,chbx3):
        label.destroy()
        entry.destroy()
        button.destroy()
        chbx1.destroy()
        chbx2.destroy()
        chbx3.destroy()
    
    def read_data_from_json(self):
        items = []
        try:
            with open(self.file_name, 'r') as jsonfile:
                data = json.load(jsonfile)
                items.extend(item['sToolName'] for item in data['ToolItems'])
        except FileNotFoundError:
            print("File not found")
        except Exception as e:
            print("An error occurred while reading the file:")
            print(traceback.print_exc())
        return items

    def populate_listbox(self):
        for i in range(1, len(self.items)):
            self.tool_listbox.insert(tk.END, self.items[i])

    def lower_case(self):
        if name := self.name_entry.get().strip():
            name_parts = [part.capitalize() for part in name.lower().split(" ")]
            formatted_name = ".".join(name_parts)
            self.name_entry.delete(0, 'end')
            self.name_entry.insert(0, formatted_name)
        else:
            messagebox.showerror("Error", "Name cannot be empty.")
            self.name_entry.focus()
            
    def create_widgets(self):
        self.name_label = ttk.Label(self.orderframe, text="Name: (first.last)*")
        self.name_entry = ttk.Entry(self.orderframe)
        self.name_entry.bind('<FocusOut>', lambda e: self.lower_case())
        self.machine_label = ttk.Label(self.orderframe, text="Machine:*")
        self.machine_combo = ttk.Combobox(self.orderframe, values=[f"HC-{i:02d}" for i in range(1,31)])
        self.machine_combo['state']='readonly'
        self.part_label = ttk.Label(self.orderframe, text='Part Number*')
        self.part_entry =ttk.Entry(self.orderframe)
        self.needed_by_label = ttk.Label(self.orderframe, text="Needed by:")
        self.needed_by_date = ttk.Combobox(self.orderframe, values=["Today", "Tomorrow", "Day after tomorrow"])
        self.needed_by_hour = tk.Spinbox(self.orderframe, from_=1, to=12,width=3, format="%02.0f", wrap=True)
        self.needed_by_minute = tk.Spinbox(self.orderframe, from_=0, to=59, width=3, format="%02.0f", wrap=True)
        self.needed_by_am_pm = ttk.Combobox(self.orderframe, values=["AM", "PM"], width=3)
        self.asap_var = tk.BooleanVar() # Create a variable to hold the checkbox's state
        self.asap_checkbox = ttk.Checkbutton(self.orderframe, text="ASAP", variable=self.asap_var)
        self.asap_checkbox.bind("<ButtonRelease-1>", self.set_asap) # Bind the checkbox to the 'set_asap' function
        self.comments_label = ttk.Label(self.orderframe, text="Comments:")
        self.comments_text = tk.Text(self.orderframe, height=10)

    def set_default_values(self):
        self.update_time()
        self.master.after(300000, self.set_default_values)

    def update_time(self):
        now = datetime.datetime.now()
        hour = ((now.hour % 12) + 1)
        minute = now.minute
        am_pm = "AM" if now.hour < 12 else "PM"

        self.needed_by_date.set("Today")
        self.needed_by_hour.delete(0, "end")
        self.needed_by_hour.insert(0, f"{hour:02}")
        self.needed_by_minute.delete(0, "end")
        self.needed_by_minute.insert(0, f"{minute:02}")
        self.needed_by_am_pm.set(am_pm)

    def set_asap(self, event):
        if self.asap_var.get():
            self.update_time()
        else:
            # Set the needed_by_date to today
            self.needed_by_date.set("Today")
            # Set the needed_by_hour and needed_by_minute to the current time
            now = datetime.datetime.now()
            self.needed_by_hour.delete(0, "end")
            self.needed_by_hour.insert(0, (now.hour % 12))
            self.needed_by_minute.delete(0, "end")
            self.needed_by_minute.insert(0, now.minute)


    def position_widgets(self):
        self.name_label.grid(row=0,column=0,sticky="E")
        self.name_entry.grid(row=0,column=1,sticky="W")
        self.machine_label.grid(row=1, column=0,sticky="E")
        self.machine_combo.grid(row=1,column=1,sticky="W")
        self.part_label.grid(row=2, column=0,sticky="E")
        self.part_entry.grid(row=2,column=1, sticky="W")
        self.needed_by_label.grid(row=3,columnspan=4)
        self.needed_by_date.grid(row=4,column=0,sticky="E")
        self.needed_by_hour.grid(row=4,column=1,sticky="E")
        self.needed_by_minute.grid(row=4,column=2,sticky="W")
        self.needed_by_am_pm.grid(row=4,column=3,sticky="W")
        self.asap_checkbox.grid(row=5)
        self.comments_label.grid(row=6,column=0,sticky="W")
        self.comments_text.grid(row=7,columnspan=4,sticky="W",padx=5)

    def create_search_bar(self):
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.orderframe, textvariable=self.search_var)
        self.search_entry.grid(row=1, column=5, pady=5, sticky="W")
        self.search_var.trace("w", self.update_listbox)
        self.search_label =ttk.Label(self.orderframe, text='Tool Search')
        self.search_label.grid(row=0,column=5,pady=5)
    
    def update_listbox(self, *args):
        search_term = self.search_var.get()
        self.tool_listbox.delete(0, tk.END)
        if search_term:
            for item in self.items:
                if search_term in item:
                    self.tool_listbox.insert(tk.END, item)
        else:
            for item in self.items:
                self.tool_listbox.insert(tk.END, item)


if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap("toolbox.ico")
    root.title("Tool Ordering App")
    app = ToolOrder(root)
    app.mainloop()