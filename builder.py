import sqlite3
import tkinter as tk 
from tkinter import ttk
from datetime import datetime
import win32api
import win32con
import winreg as winreg
import configparser
from win32printing import Printer

config = configparser.ConfigParser()

config.read('config.ini')

printer_name = config['SETTINGS']['Printer']
db_path = config['PATHS']['tool_order_db']
class ViewOrders(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.create_widgets()
        self.populate_treeview()
        self.tree.bind("<<TreeviewSelect>>", self.show_order_details)
        # self.details_tree.bind("<<TreeviewSelect>>", self.send_to_ecp)
        self.complete_button = ttk.Button(self, text="Complete Order", command=self.complete_order)
        self.complete_button.grid(row=10, column=0, padx=5, pady=5)
        self.complete_button = ttk.Button(self, text="Reload Orders", command=self.reset_treeview)
        self.complete_button.grid(row=10, column=1, padx=5, pady=5)
        self.position_widgets()
        self.pack()

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=("name", "machine", "part", "time", "comments"))#, "complete"))
        self.tree["columns"] = ("name", "machine", "part", "time", "comments")#, "complete")
        for col in self.tree["columns"]:
            self.tree.column(col, anchor="center")
        self.tree.heading("#0", text="Order ID")
        self.tree.column("#0", width=55,stretch=False)
        self.tree.heading("name", text="Name")
        self.tree.column("name", width=85, stretch=False)
        self.tree.heading("machine", text="Machine")
        self.tree.column("machine", width=65, stretch=False)
        self.tree.heading("part", text="Part Number")
        self.tree.column("part", width=95, stretch=False)
        self.tree.heading("time", text="Needed by")
        self.tree.column("time", width=120, stretch=False)
        self.tree.heading("comments", text="Comments")
        # self.tree.heading("complete", text="Complete")
        self.details_tree = ttk.Treeview(self, columns=("tool_name", "item_qty", "cf", "ct", "metric"))
        self.details_tree["columns"] = ("tool_name", "item_qty", "cf", "ct", "metric")
        for col in self.details_tree["columns"]:
            self.details_tree.column(col, anchor="center")
        self.details_tree.heading("#0", text="Order ID")
        self.details_tree.column("#0", width=55,stretch=False)
        self.details_tree.heading("tool_name", text="Tool Name")
        self.details_tree.column("tool_name", width=85, stretch=False)
        self.details_tree.heading("item_qty", text="Quantity")
        self.details_tree.column("item_qty", width=85, stretch=False)
        self.separator = ttk.Separator(self,orient="horizontal")
        self.details_tree.heading("cf", text="CF")
        self.details_tree.column("cf", width=50, stretch=False)
        self.details_tree.heading("ct", text="CT")
        self.details_tree.column("ct", width=50, stretch=False)
        self.details_tree.heading("metric", text="Metric")
        self.details_tree.column("metric", width=50, stretch=False)
        
    def reset_treeview(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for i in self.details_tree.get_children():
            self.details_tree.delete(i)
        self.populate_treeview()

    def connect_to_db(self):
        try:
            conn = sqlite3.connect(db_path)
            return conn
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            return None

    def sort_treeview(self):
        items = [(self.tree.set(child, '#4'), child) for child in self.tree.get_children()]
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
                orders = sorted(orders, key=lambda x: datetime.strptime(x[4], '%Y-%m-%d %I:%M %p'))
                existing_ids = [self.tree.item(item)['text'] for item in self.tree.get_children()]
                for order in orders:
                    if order[0] not in existing_ids:
                        self.tree.insert("", tk.END, text=order[0], values=(order[1], order[2], order[3], order[4], order[5]))
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
                order_details = c.fetchall()
                return order_details
            except Exception as e:
                print(f"An error occurred while fetching order details: {e}")
            finally:
                conn.close()

    def _insert_order_details_into_tree(self, order_details):
            for order in order_details:
                self.details_tree.insert("", tk.END, text=order[0], values=(order[1], order[2], order[3], order[4], order[5]))
            for i, item in enumerate(self.details_tree.get_children()):
                if i % 2 == 0:
                    self.details_tree.item(item, tags=("odd",))

            self.details_tree.tag_configure("odd", background="light blue")


    def position_widgets(self):
        self.tree.grid(row=0, column=0, columnspan=2,padx=15, pady=15, sticky='W')
        self.separator.grid(row=1,columnspan=2, sticky='EW')
        self.details_tree.grid(row=2, column=0, padx=15, pady=15,sticky='W')
        
    def send_to_ecp(self, e):
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\MyApp')
        value, _ = winreg.QueryValueEx(key, 'MyValue')
        print(value)
        winreg.CloseKey(key)
        selected_item = self.details_tree.selection()[0]
        tool_name = self.details_tree.item(selected_item)['values'][0]
        tool_name_bytes = tool_name.encode('utf-8')
        win32api.PostMessage(value, win32con.WM_COPYDATA, 0, tool_name_bytes)


    def complete_order(self):
        self.print_ticket()
        if selected_item := self.tree.focus():
            order_id = self.tree.item(selected_item)['text']
            with sqlite3.connect(db_path) as conn:
                c = conn.cursor()
                c.execute("UPDATE orders SET complete = 1 WHERE rowid = ?", (order_id,))
            self.tree.delete(*self.tree.get_children())
            self.populate_treeview()
            
    def print_ticket(self):
        font = {"height": 18}
        name = self.tree.item(self.tree.focus())['values'][0]
        machine = self.tree.item(self.tree.focus())['values'][1]
        partnum = self.tree.item(self.tree.focus())['values'][2]
        time = datetime.now()
        time = time.strftime("%m/%d/%y, %H:%M")
        details = []
        for child in self.details_tree.get_children():
            tool_name = self.details_tree.item(child)['values'][0]
            qty = self.details_tree.item(child)['values'][1]
            details.append((tool_name, qty))
        with Printer(linegap=2, printer_name=printer_name) as printer:
            printer.text(f"Name: {str(name)}",align="center", font_config=font)
            printer.text(f"Machine Number: {str(machine)}", font_config=font)
            printer.text(f"Part Number: {str(partnum)}",font_config=font)
            for tool_name, qty in details:
                printer.text(f"{str(tool_name)} - QTY={str(qty)}", font_config=font)
            printer.text(time, align="center")
        
if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap("toolbox.ico")
    root.title("Tool Builder App")
    view_orders = ViewOrders(root)
    view_orders.grid(row=0, column=0)
    root.mainloop()
