import json
import os
import tkinter as tk
from tkinter import messagebox, ttk

import pandas as pd


def build_json():
    # Read Excel file into a pandas dataframe
    df = pd.read_excel(
        "C:\\Users\\adam.riggs\\Desktop\\BOM.xlsx", sheet_name='Tools')

    # Convert int64 data to regular integers
    df = df.astype(object).where(pd.notnull(df), None)

    # Extract keys from the first row
    keys = list(df.columns)

    # Extract data from all other rows
    data = []
    for i in range(1, len(df)):
        row = {keys[j]: df.iloc[i, j] for j in range(len(keys))}
        data.append(row)

    # Convert data to JSON
    json_data = json.dumps(data)

    # Write JSON data to a file
    with open("C:\\Users\\adam.riggs\\Desktop\\BOM.json", 'w') as f:
        f.write(json_data)


def populate_treeview(treeview):
    # Check if the JSON file exists
    if not os.path.isfile('C:\\Users\\adam.riggs\\Desktop\\BOM.json'):
        # If the file does not exist, build it
        build_json()

    # Open the JSON file
    try:
        with open('C:\\Users\\adam.riggs\\Desktop\\BOM.json', 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        # If the file does not exist or does not contain valid JSON data, show an error message
        messagebox.showerror('Error', 'Failed to load JSON data from file.')
        return

    # Define columns for the treeview
    treeview['columns'] = ('EssaiPartNum', 'Type', 'EDPNum', 'Manufacturer')

    # Define column headings
    treeview.heading('#0', text='Index')
    treeview.heading('EssaiPartNum', text='Essai Part Num')
    treeview.heading('Type', text='Type')
    treeview.heading('EDPNum', text='EDP Num')
    treeview.heading('Manufacturer', text='Manufacturer')

    # Populate the treeview with data from the JSON file
    for i, row in enumerate(data):
        values = (row['EssaiPartNum'], row['Type'],
                  row['EDPNum'], row['Manufacturer'])
        treeview.insert(parent='', index=i, iid=i, text=str(i), values=values)

    treeview.bind('<<TreeviewSelect>>',
                  lambda event: show_details(treeview, data))

    # Create a search box
    search_frame = ttk.Frame(root)
    search_frame.pack(side='top', fill='x', padx=5, pady=5)
    search_label = ttk.Label(search_frame, text='Search Essai Part Num:')
    search_label.pack(side='left', padx=5)
    search_entry = ttk.Entry(search_frame)
    search_entry.pack(side='left', fill='x', expand=True, padx=5)
    search_entry.bind('<Return>', lambda event: search_by_essai_part_num(
        treeview, data, search_entry.get()))

    # Create a button to add new items
    add_button = ttk.Button(root, text='Add Item',
                            command=lambda: add_item(treeview, data))
    add_button.pack()


def search_by_essai_part_num(treeview, data, essai_part_num):
    # Loop through the items in the treeview and find the first match
    for item in treeview.get_children():
        values = treeview.item(item, 'values')
        if values[0] == essai_part_num:
            # Select the item and make it visible
            treeview.selection_set(item)
            treeview.see(item)
            break
    else:
        # If no match was found, show an error message
        messagebox.showwarning(
            'Warning', f'Essai Part Num "{essai_part_num}" not found.')


def add_item(treeview, data):
    # Create a new window for adding items
    add_window = tk.Toplevel(root)
    add_window.title('Add Item')

    # Create entry fields for each column in the treeview
    essai_part_num_label = ttk.Label(add_window, text='Essai Part Num:')
    essai_part_num_label.grid(row=0, column=0, padx=5, pady=5)
    essai_part_num_entry = ttk.Entry(add_window)
    essai_part_num_entry.grid(row=0, column=1, padx=5, pady=5)

    type_label = ttk.Label(add_window, text='Type:')
    type_label.grid(row=1, column=0, padx=5, pady=5)
    type_options = ['BA', 'BU', 'CD', 'CM', 'CR', 'CS', 'CT', 'DA', 'DC', 'DS', 'DJ', 'DT', 'DO', 'EM', 'FA', 'FM', 'KC', 'LA', 'LP', 'PR', 'RM', 'RT', 'SD', 'SS', 'TE', 'TM', 'DM']
    type_entry = ttk.Combobox(add_window, values=type_options)
    type_entry.grid(row=1, column=1, padx=5, pady=5)

    edp_num_label = ttk.Label(add_window, text='EDP Num:')
    edp_num_label.grid(row=2, column=0, padx=5, pady=5)
    edp_num_entry = ttk.Entry(add_window)
    edp_num_entry.grid(row=2, column=1, padx=5, pady=5)

    manufacturer_label = ttk.Label(add_window, text='Manufacturer:')
    manufacturer_label.grid(row=3, column=0, padx=5, pady=5)
    manufacturer_entry = ttk.Entry(add_window)
    manufacturer_entry.grid(row=3, column=1, padx=5, pady=5)

    if type_entry.get() == 'BA':
        size_label = ttk.Label(add_window, text='Size:')
        size_label.grid(row=4, column=0, padx=5, pady=5)
        size_entry = ttk.Entry(add_window)
        size_entry.grid(row=4, column=1, padx=5, pady=5)

        length_label = ttk.Label(add_window, text='Length:')
        length_label.grid(row=5, column=0, padx=5, pady=5)
        length_entry = ttk.Entry(add_window)
        length_entry.grid(row=5, column=1, padx=5, pady=5)

    elif type_entry.get() == 'BU':
        size_label = ttk.Label(add_window, text='Size:')
        size_label.grid(row=4, column=0, padx=5, pady=5)
        size_entry = ttk.Entry(add_window)
        size_entry.grid(row=4, column=1, padx=5, pady=5)

        style_label = ttk.Label(add_window, text='Style:')
        style_label.grid(row=5, column=0, padx=5, pady=5)
        style_entry = ttk.Entry(add_window)
        style_entry.grid(row=5, column=1, padx=5, pady=5)

    # Create a submit button that adds the new item to the treeview and updates the JSON file
    submit_button = ttk.Button(add_window, text='Submit', command=lambda: submit_new_item(
        treeview, data, add_window, essai_part_num_entry.get(), type_entry.get(), edp_num_entry.get(), manufacturer_entry.get()))
    submit_button.grid(row=4, column=1, padx=5, pady=5)


def submit_new_item(treeview, data, add_window, essai_part_num, type, edp_num, manufacturer):
    # Add the new item to the data list
    new_item = {'EssaiPartNum': essai_part_num, 'Type': type,
                'EDPNum': edp_num, 'Manufacturer': manufacturer}
    data.append(new_item)

    # Update the JSON file
    json_data = json.dumps(data)
    with open('C:\\Users\\adam.riggs\\Desktop\\output.json', 'w') as f:
        f.write(json_data)

    # Insert the new item into the treeview
    index = len(data) - 1
    values = (essai_part_num, type, edp_num, manufacturer)
    treeview.insert(parent='', index=index, iid=index,
                    text=str(index), values=values)

    # Close the add window
    add_window.destroy()


def show_details(treeview, data):
    # Get the selected item
    selection = treeview.selection()
    if not selection:
        return
    item_id = selection[0]
    item_data = data[int(item_id)]

    # Create a new window to show the details
    window = tk.Toplevel(treeview)
    window.title('Item Details')

    # Create a text widget to show the JSON data
    text_widget = tk.Text(window, wrap='word', height=20, width=80)
    text_widget.pack(fill='both', expand=True)

    # Convert the item data to JSON and display it in the text widget
    json_data = json.dumps(item_data, indent=4)
    text_widget.insert('1.0', json_data)


# Create the GUI
root = tk.Tk()

treeview = ttk.Treeview(root)
treeview.pack()

populate_treeview(treeview)

root.mainloop()
