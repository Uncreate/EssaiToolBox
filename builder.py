import sqlite3
import tkinter as tk 
from tkinter import ttk
from datetime import datetime
import win32api
import win32con
import winreg as winreg
import configparser
config = configparser.ConfigParser()
config.read('config.ini')


db_path = config['PATHS']['tool_order_db']
class ViewOrders(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.create_widgets()
        self.populate_treeview()
        self.tree.bind("<<TreeviewSelect>>", self.show_order_details)
        # self.details_tree.bind("<<TreeviewSelect>>", self.send_to_ecp)
        self.complete_button = ttk.Button(self, text="Complete Order", command=self.complete_order)
        self.complete_button.grid(row=10, column=0,columnspan=2, padx=5, pady=5)
        self.position_widgets()
        self.pack()

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=("name", "machine", "part", "time", "comments", "complete"))
        self.tree["columns"] = ("name", "machine", "part", "time", "comments", "complete")
        for col in self.tree["columns"]:
            self.tree.column(col, anchor="center")
        self.tree.heading("#0", text="Order ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("machine", text="Machine")
        self.tree.heading("part", text="Part Number")
        self.tree.heading("time", text="Needed by")
        self.tree.heading("comments", text="Comments")
        self.tree.heading("complete", text="Complete")
        self.details_tree = ttk.Treeview(self, columns=("tool_name", "item_qty", "cf", "ct", "metric"))
        self.details_tree["columns"] = ("tool_name", "item_qty", "cf", "ct", "metric")
        for col in self.details_tree["columns"]:
            self.details_tree.column(col, anchor="center")
        self.details_tree.heading("#0", text="Order ID")
        self.details_tree.heading("tool_name", text="Tool Name")
        self.details_tree.heading("item_qty", text="Quantity")
        self.separator = ttk.Separator(self,orient="horizontal")
        self.details_tree.heading("cf", text="CF")
        self.details_tree.heading("ct", text="CT")
        self.details_tree.heading("metric", text="Metric")
        

    def populate_treeview(self):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("SELECT rowid, * FROM orders WHERE complete = 0")
        orders = c.fetchall()
        orders = sorted(orders, key=lambda x: datetime.strptime(x[4], '%Y-%m-%d %I:%M %p'))
        existing_ids = [self.tree.item(item)['text'] for item in self.tree.get_children()]
        for order in orders:
            if order[0] not in existing_ids:
                self.tree.insert("", tk.END, text=order[0], values=(order[1], order[2], order[3], order[4], order[5], order[6]))
        conn.close()
        items = [(self.tree.set(child, '#4'), child) for child in self.tree.get_children()]
        items.sort()
        for index, (val, item) in enumerate(items):
            self.tree.move(item, '', index)
        self.master.after(30000, self.populate_treeview)
    
    def show_order_details(self, event):
        # clear the details_tree
        for i in self.details_tree.get_children():
            self.details_tree.delete(i)
        # get the selected order id
        selected_order = self.tree.focus()
        order_id = self.tree.item(selected_order)['text']
        # fetch the details of the order from the order_detail table
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("SELECT * FROM order_detail WHERE order_id=?", (order_id,))
        order_details = c.fetchall()
        for order in order_details:
            self.details_tree.insert("", tk.END, text=order[0], values=(order[1], order[2], order[3], order[4], order[5]))
        conn.close()

    def position_widgets(self):
        self.tree.grid(row=0, column=0, columnspan=2,padx=15, pady=15)
        self.separator.grid(row=1,columnspan=2, sticky='EW')
        self.details_tree.grid(row=2, column=0, padx=15, pady=15,sticky='NW')
        
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
        if selected_items := self.tree.focus():
            order_id = self.tree.item(self.tree.focus())['text']
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("UPDATE orders SET complete = 1 WHERE rowid = ?", (order_id,))
            conn.commit()
            conn.close()
            self.tree.delete(*self.tree.get_children())
            self.populate_treeview()


if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap("toolbox.ico")
    root.title("Tool Builder App")
    view_orders = ViewOrders(root)
    view_orders.grid(row=0, column=0)
    root.mainloop()
