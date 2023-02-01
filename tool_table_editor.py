import tkinter as tk
from tkinter import ttk
import pandas as pd
class ToolTableEditor(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # create 3 frames in the main frame
        self.tree_frame = ttk.Frame(self)
        self.details_frame = ttk.Frame(self)
        self.control_frame = ttk.Frame(self)
        self.tree_frame.pack(fill='x', expand=True)
        self.details_frame.pack(fill='x', expand=True)
        self.control_frame.pack(fill='x', expand=True)
        self.tree = ttk.Treeview(self.tree_frame)
        self.tree.pack(fill='both', expand=True)
        self.df = pd.read_excel('./Data/BOM.xlsx', sheet_name='Tools', keep_default_na=False)
        print(self.df)
        # insert data from the dataframe into the treeview
        #for i, row in self.df.iterrows():
        #    self.tree.insert('', 'end', text=row['Part Name'], values=(row['Part Number'], row['Quantity']))


if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap("toolbox.ico")
    root.title("Tool Ordering App")
    app = ToolTableEditor(root)
    app.pack(fill='both', expand=True)
    app.mainloop()
