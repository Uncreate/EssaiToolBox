import configparser
import ctypes
import ctypes.wintypes
import json
import sqlite3
import tkinter as tk
import winreg as winreg
from datetime import datetime
from tkinter import messagebox, ttk

import win32con
from win32printing import Printer

config = configparser.ConfigParser()

config.read('config.ini')
tool_items = config['PATHS']['tool_items']
printer_name = config['SETTINGS']['Printer']
db_path = config['PATHS']['tool_order_db']
inv_path = config['PATHS']['inventory_db']


class InventoryManager(tk.Toplevel):
    def __init__(self, master=None, inv_path="inventory.db"):
        super().__init__(master)

        self.geometry("400x500")
        self.title("Inventory Manager")
        self.focus
        self.search_frame = ttk.Frame(self)
        self.epn_label = ttk.Label(
            self.search_frame, text="Essai Part Number:")
        self.epn_entry = ttk.Entry(self.search_frame)
        self.epn_search = ttk.Button(
            self.search_frame, text="Search Inventory", command=self.search_inventory)
        self.inventory = ttk.Frame(self)
        self.button_frame = ttk.Frame(self)
        self.update_button = ttk.Button(
            self.button_frame, text="Update Inventory", command=self.update_inventory)
        self.entries = {}
        self.create_ui()
        

        # Bind the <Return> event to the epn_entry widget
        self.epn_entry.bind("<Return>", self.handle_search)

    def handle_search(self, event):
        # Call the search_inventory() method when the <Return> key is pressed
        self.search_inventory()

    def create_ui(self):
        self.search_frame.grid(row=0, column=0)
        self.epn_label.pack(side="left", padx=10)
        self.epn_entry.pack(side="left", padx=10)
        self.epn_search.pack(side="left", padx=10)
        self.inventory.grid(row=1, column=0,)
        self.button_frame.grid(row=2)
        self.update_button.pack()

    def update_inventory(self):
        if not messagebox.askyesno(
            "Inventory Update",
            "This will update the values assigned to this item. \n\n Are you sure everything is correct?",
        ):
            return

        inventory_values = {}
        for label in self.entries:
            value = self.entries[label].get()
            if label != "Essai Part Number:":
                inventory_values[label] = value

        # Update the database
        conn = sqlite3.connect(inv_path)
        with conn:
            c = conn.cursor()
            c.execute(
                "UPDATE inventory SET sToolManufacturer=?, sToolEdp=?, iMin=?, iMax=?, iQty=?, sLocation=? WHERE sEssaiPartNum=?",
                (inventory_values["Tool Manufacturer:"], inventory_values["EDP Number:"], inventory_values["Min"], inventory_values["Max"],
                 inventory_values["Quantity on Hand:"], inventory_values["Tool Crib Location:"], self.entries["Essai Part Number:"].get())
            )
            conn.commit()
            messagebox.showinfo("Inventory Update",
                                "The inventory has been updated successfully!")

    def search_inventory(self):
        epn = self.epn_entry.get()

        conn = sqlite3.connect(inv_path)
        with conn:
            c = conn.cursor()
            c.execute("SELECT * FROM inventory WHERE sEssaiPartNum=?", (epn,))
            inventory_row = c.fetchone()

        if inventory_row is None:
            return

        labels = ["Essai Part Number:", "Tool Manufacturer:", "EDP Number:",
                  "Quantity on Hand:", "Tool Crib Location:", "Min", "Max"]
        values = [inventory_row[0], inventory_row[1], inventory_row[2],
                  inventory_row[5], inventory_row[6], inventory_row[3], inventory_row[4]]

        for i, label in enumerate(labels):
            ttk.Label(self.inventory, text=label).grid(
                row=i, column=0, padx=5, pady=5)
            self.entries[label] = ttk.Entry(self.inventory)
            self.entries[label].grid(row=i, column=1, padx=5, pady=5)
            self.entries[label].insert(0, values[i])
            self.entries["Essai Part Number:"].configure(state="readonly")


class ViewOrders(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.last_order_data = None
        self.create_widgets()
        self.populate_treeview()
        self.tree.bind("<<TreeviewSelect>>", self.show_order_details)
        self.details_tree.bind("<<TreeviewSelect>>", self.invetory_viewer)
        # self.details_tree.bind("<Double-Button-1>", self.send_to_ecp)
        self.position_widgets()
        self.pack()

    def create_widgets(self):
        self.separator = ttk.Separator(self, orient="horizontal")
        self.inventory_frame = tk.LabelFrame(self, text="Inventory Details")
        self.button_frame = ttk.Frame(self)
        self.complete_button = ttk.Button(
            self.button_frame, text="Complete Order", command=self.complete_order)
        self.reset_button = ttk.Button(
            self.button_frame, text="Reload Orders", command=self.reset_treeview)
        self.delete_button = ttk.Button(
            self.button_frame, text="Delete Order", command=self.delete_order)
        self.delete_tool = ttk.Button(
            self.button_frame, text="Remove Tool", command=self.delete_tool_from_order)
        self.tree = ttk.Treeview(self, columns=(
            "name", "machine", "part", "time", "comments"))  # , "complete"))
        self.tree["columns"] = ("name", "machine", "part",
                                "time", "comments")  # , "complete")
        for col in self.tree["columns"]:
            self.tree.column(col, anchor="center")
        self.tree.heading("#0", text="Order ID")
        self.tree.column("#0", width=55, stretch=False)
        self.tree.heading("name", text="Name")
        self.tree.column("name", width=85, stretch=False)
        self.tree.heading("machine", text="Machine")
        self.tree.column("machine", width=65, stretch=False)
        self.tree.heading("part", text="Part Number")
        self.tree.column("part", width=95, stretch=False)
        self.tree.heading("time", text="Needed by")
        self.tree.column("time", width=120, stretch=False)
        self.tree.heading("comments", text="Comments")
        self.details_tree = ttk.Treeview(self, columns=(
            "tool_name", "item_qty", "cf", "ct", "metric"))
        self.details_tree["columns"] = (
            "tool_name", "item_qty", "cf", "ct", "metric")
        for col in self.details_tree["columns"]:
            self.details_tree.column(col, anchor="center")
        self.details_tree.heading("#0", text="Item")
        self.details_tree.column("#0", width=55, stretch=False)
        self.details_tree.heading("tool_name", text="Tool Name")
        self.details_tree.column("tool_name", width=85, stretch=False)
        self.details_tree.heading("item_qty", text="Quantity")
        self.details_tree.column("item_qty", width=85, stretch=False)
        self.details_tree.heading("cf", text="CF")
        self.details_tree.column("cf", width=50, stretch=False)
        self.details_tree.heading("ct", text="CT")
        self.details_tree.column("ct", width=50, stretch=False)
        self.details_tree.heading("metric", text="Metric")
        self.details_tree.column("metric", width=50, stretch=False)
        self.test_button = ttk.Button(
            self.button_frame, text="Inventory Management", command=InventoryManager)
        self.reprint_ticket = ttk.Button(
            self.button_frame, text="Reprint Last Order", command=self.reprint_last_order)
        self.spacer = ttk.Label(self.button_frame, text='')

    def reset_treeview(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for i in self.details_tree.get_children():
            self.details_tree.delete(i)
        self.existing_ids = []
        self.populate_treeview()

    def connect_to_db(self):
        try:
            return sqlite3.connect(db_path)
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            return None

    def sort_treeview(self):
        items = [(self.tree.set(child, '#4'), child)
                 for child in self.tree.get_children()]
        items.sort()
        for index, (val, item) in enumerate(items):
            self.tree.move(item, '', index)
        for i, item in enumerate(self.tree.get_children()):
            if i % 2 == 0:
                self.tree.item(item, tags=("odd",))
        self.tree.tag_configure("odd", background="light blue")

    def populate_treeview(self):
        if conn := self.connect_to_db():
            with conn:
                c = conn.cursor()
                c.execute("SELECT rowid, * FROM orders WHERE complete = 0")
                orders = c.fetchall()
                orders = sorted(orders, key=lambda x: (
                    datetime.strptime(x[4], '%Y-%m-%d %H:%M')))
                self.existing_ids = [self.tree.item(
                    item)['text'] for item in self.tree.get_children()]
                for order_data in orders:
                    order_id = order_data[0]
                for order in orders:
                    if order[0] not in self.existing_ids:
                        self.tree.insert("", tk.END, text=order[0], values=(
                            order[1], order[2], order[3], order[4], order[5]))
                        if self.last_order_data is None:
                            self.last_order_data = order_id
                self.sort_treeview()
        self.master.after(30000, self.populate_treeview)

    def show_order_details(self, event):
        # clear the details_tree
        for i in self.details_tree.get_children():
            self.details_tree.delete(i)
        # get the selected order id
        selected_order = self.tree.focus()
        order_id = self.tree.item(selected_order)['text']
        # fetch the details of the order from the order_detail table
        order_details = self._get_order_details(order_id)
        self._insert_order_details_into_tree(order_details)

    def _get_order_details(self, order_id):
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("SELECT * FROM order_detail WHERE order_id=?", (order_id,))
            return c.fetchall()
        except Exception as e:
            print(f"An error occurred while fetching order details: {e}")
        finally:
            conn.close()

    def _insert_order_details_into_tree(self, order_details):
        for counter, order in enumerate(order_details, start=1):
            self.details_tree.insert("", tk.END, text=counter, values=(
                order[1], order[2], order[3], order[4], order[5]))
        for i, item in enumerate(self.details_tree.get_children()):
            if i % 2 == 0:
                self.details_tree.item(item, tags=("odd",))

        self.details_tree.tag_configure("odd", background="light blue")

    '''def _insert_order_details_into_tree(self, order_details):
            for order in order_details:
                self.details_tree.insert("", tk.END, text=order[0], values=(order[1], order[2], order[3], order[4], order[5]))
            for i, item in enumerate(self.details_tree.get_children()):
                if i % 2 == 0:
                    self.details_tree.item(item, tags=("odd",))

            self.details_tree.tag_configure("odd", background="light blue")'''

    def position_widgets(self):
        self.tree.grid(row=0, column=0, columnspan=2,
                       padx=15, pady=15, sticky='W')
        self.separator.grid(row=1, columnspan=2, sticky='EW')
        self.details_tree.grid(row=2, column=0, padx=15, pady=15, sticky='W')
        self.inventory_frame.grid(row=2, column=1, sticky='NESW')
        self.button_frame.grid(
            row=10, column=0, columnspan=2, padx=5, pady=5, stick='EW')

        self.complete_button.grid(row=2, column=2, padx=5, pady=5, sticky='N')
        self.reset_button.grid(row=0, column=0, padx=5, pady=5)
        self.delete_button.grid(row=1, column=3, padx=5, pady=5)
        self.delete_tool.grid(row=0, column=3, padx=5, pady=5, sticky='E')
        self.test_button.grid(row=0, column=5, columnspan=2,
                              padx=5, pady=5, sticky='E')
        self.reprint_ticket.grid(row=1, column=0, padx=5, pady=5)
        self.spacer.grid(row=0, column=4)

    def complete_order(self):
        self.print_ticket()
        self.inventory_update()
        if selected_item := self.tree.focus():
            order_id = self.tree.item(selected_item)['text']
            with sqlite3.connect(db_path) as conn:
                c = conn.cursor()
                c.execute(
                    "UPDATE orders SET complete = 1 WHERE rowid = ?", (order_id,))
            self.tree.delete(*self.tree.get_children())
            self.populate_treeview()

    def inventory_update(self):
        with open(tool_items, "r") as file:
            data = json.load(file)
        conn = sqlite3.connect(inv_path)
        cursor = conn.cursor()
        for child in self.details_tree.get_children():

            tool_name = self.details_tree.item(child)['values'][0]
            order_qty = self.details_tree.item(child)['values'][1]
            print(tool_name)
            print(order_qty)
            essai_partNum = [item["sEssaiPartNum"] for item in data["ToolItems"]
                             if item["sToolName"] == self.details_tree.item(child)['values'][0]]
            essai_partNum = essai_partNum[0]
            cursor.execute(
                "UPDATE inventory SET iQty = iQty - ? WHERE sEssaiPartNum = ?", (order_qty, essai_partNum))
        conn.commit()
        conn.close()

    def invetory_viewer(self, e):
        with open(tool_items, "r") as file:
            data = json.load(file)
        selection = self.details_tree.selection()
        if not selection:
            return
        child = selection[0]
        essai_partNum = [item["sEssaiPartNum"] for item in data["ToolItems"]
                         if item["sToolName"] == self.details_tree.item(child)['values'][0]]
        if not essai_partNum:
            return

        sEssaiPartNum = essai_partNum[0]
        tool_group_name = [item["sToolGroupName"]
                           for item in data["ToolItems"] if item["sEssaiPartNum"] == sEssaiPartNum][0]

        tool_group_names = {
            "EM": "Endmill", "BA": "Ballmill", "BU": "Bullmill", "FM": "Facemill",
            "LP": "Lollipop mill", "DO": "Dovetail mill", "CM": "Chamfer mill",
            "CR": "Corner Round mill", "DA": "Double Angle Shank Cutter",
            "KC": "Key Cutter", "SS": "Slitter Saw", "SD": "Spot Drill",
            "CS": "Countersink", "DS": "Drill Stub", "DJ": "Drill Jobber",
            "DT": "Drill Taper", "CD": "Circuitboard Drill", "RM": "Reamer",
            "CT": "Cut Tap", "RT": "Roll Form Tap", "TM": "Thread Mill Straight",
            "DC": "Coolant Thru Drill", "TE": "Tapered Endmill"
        }
        full_name = tool_group_names.get(tool_group_name, "Unknown")

        conn = sqlite3.connect(inv_path)
        with conn:
            c = conn.cursor()
            c.execute("SELECT * FROM inventory WHERE sEssaiPartNum=?",
                      (sEssaiPartNum,))
            inventory_row = c.fetchone()
            if not inventory_row:
                return

            labels = ["Essai Part Number:", "Tool Manufacturer:", "EDP Number:",
                      "Quantity on Hand:", "Tool Crib Location:", "Tool Group Name:"]
            values = [inventory_row[0], inventory_row[1], inventory_row[2],
                      inventory_row[5], inventory_row[6], full_name]

            for widget in self.inventory_frame.winfo_children():
                widget.destroy()

            for i, label in enumerate(labels):
                ttk.Label(self.inventory_frame, text=label).grid(
                    row=i, column=0, padx=5, pady=5)
                ttk.Label(self.inventory_frame, text=values[i]).grid(
                    row=i, column=1, padx=5, pady=5)
        self.send_to_ecp()

    def delete_order(self):
        if selected_item := self.tree.selection():
            if result := messagebox.askokcancel(
                "Delete Order", "Are you sure you want to delete this order?"
            ):
                order_id = self.tree.item(selected_item)['text']
                print(order_id)
                if conn := self.connect_to_db():
                    c = conn.cursor()
                    c.execute("DELETE FROM orders WHERE rowid=?", (order_id,))
                    conn.commit()
                    self.reset_treeview()
                    messagebox.showinfo("Info", "Order Deleted Successfully")
                else:
                    messagebox.showerror(
                        "Error", "Error connecting to the database")
        else:
            messagebox.showerror("Error", "No order selected")

    def delete_tool_from_order(self):
        if selected_item := self.details_tree.selection():
            if result := messagebox.askyesno(
                "Delete Tool", "Are you sure you want to delete this tool from the order?"
            ):
                order_id = self.details_tree.item(selected_item)['text']
                tool_id = self.details_tree.item(selected_item)["values"][0]
                print(order_id)
                print(tool_id)
                if conn := self.connect_to_db():
                    c = conn.cursor()
                    c.execute(
                        "DELETE FROM order_detail WHERE order_id = ? AND tool_name = ?", (order_id, tool_id))
                    conn.commit()
                    self.reset_treeview()
                    messagebox.showinfo("Info", "Tool Deleted Successfully")
                else:
                    messagebox.showerror(
                        "Error", "Error connecting to the database")
        else:
            messagebox.showerror("Error", "No tool selected")

    def print_ticket(self):
        font = {"height": 18}
        name = self.tree.item(self.tree.focus())['values'][0]
        machine = self.tree.item(self.tree.focus())['values'][1]
        partnum = self.tree.item(self.tree.focus())['values'][2]
        time = datetime.now()
        time = time.strftime("%m/%d/%y, %H:%M")
        details = []
        self.reprint = [(name, machine, partnum, time, details)]
        for child in self.details_tree.get_children():
            tool_name = self.details_tree.item(child)['values'][0]
            qty = self.details_tree.item(child)['values'][1]
            details.append((tool_name, qty))
        with Printer(linegap=2, printer_name=printer_name) as printer:
            printer.text(f"Name: {str(name)}",
                         align="center", font_config=font)
            printer.text(f"Machine Number: {str(machine)}", font_config=font)
            printer.text(f"Part Number: {str(partnum)}", font_config=font)
            for tool_name, qty in details:
                printer.text(
                    f"{str(tool_name)} - QTY={str(qty)}", font_config=font)
            printer.text(time, align="center")

    def reprint_last_order(self):
        font = {"height": 18}
        name, machine, partnum, time, details = self.reprint[-1]
        with Printer(linegap=2, printer_name=printer_name) as printer:
            printer.text(f"Name: {str(name)}",
                         align="center", font_config=font)
            printer.text(f"Machine Number: {str(machine)}", font_config=font)
            printer.text(f"Part Number: {str(partnum)}", font_config=font)
            for tool_name, qty in details:
                printer.text(
                    f"{str(tool_name)} - QTY={str(qty)}", font_config=font)
            printer.text(time, align="center")

    def send_to_ecp(self):
        SendMessage = ctypes.windll.user32.SendMessageW

        class COPYDATASTRUCT(ctypes.Structure):
            _fields_ = [
                ('dwData', ctypes.wintypes.LPARAM),
                ('cbData', ctypes.wintypes.DWORD),
                ('lpData', ctypes.c_char_p)  # ('lpData', ctypes.c_wchar_p)
            ]

        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             'Software\EssaiControlPanel')
        hwnd, _ = winreg.QueryValueEx(key, 'HWND')
        winreg.CloseKey(key)

        selected_item = self.details_tree.selection()[0]
        tool_name = self.details_tree.item(selected_item)['values'][0]
        # print(tool_name)
        tool_name_utf16 = tool_name.encode()  # ('utf-16')
        # print(tool_name_utf16)
        cds = COPYDATASTRUCT()
        cds.dwData = 55
        # cds.cbData = len(tool_name_utf16)
        # cds.lpData = tool_name_utf16.decode('utf-16')
        cds.cbData = ctypes.sizeof(
            ctypes.create_string_buffer(tool_name_utf16))
        cds.lpData = ctypes.c_char_p(tool_name_utf16)

        SendMessage(hwnd, win32con.WM_COPYDATA, 0, ctypes.byref(cds))


if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap("toolbox.ico")
    root.title("Tool Builder App")
    view_orders = ViewOrders(root)
    view_orders.grid(row=0, column=0)
    root.mainloop()
