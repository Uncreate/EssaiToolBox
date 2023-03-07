import tkinter as tk
from tkinter import ttk

import pandas as pd

# Load the CSV file into a pandas dataframe
df = pd.read_csv('matching_tools.csv')

# Define a function to populate the treeview with the dataframe data


def populate_treeview(treeview, df):
    # Remove any existing items from the treeview
    treeview.delete(*treeview.get_children())

    # Add the column headings to the treeview
    treeview['columns'] = list(df.columns)
    for column in df.columns:
        treeview.heading(column, text=column)

    # Add the data rows to the treeview
    df = df.reset_index(drop=True)  # Remove the index column
    for i, row in df.iterrows():
        treeview.insert(parent='', index='end', values=list(row))


def search_legacy_tool(df):
    # Get the search term from the search bar
    search_term = legacy_tool_search_var.get()

    # Remove any existing items from the treeview
    treeview.delete(*treeview.get_children())

    # Add the column headings to the treeview
    treeview['columns'] = list(df.columns)
    for column in df.columns:
        treeview.heading(column, text=column)

    # Convert all columns to string data type
    df = df.astype(str)

    # Filter the dataframe based on the search term
    filtered_df = df[df['Legacy Tool'] == search_term]

    # Add the filtered data rows to the treeview
    filtered_df = filtered_df.reset_index(drop=True)  # Remove the index column
    for i, row in filtered_df.iterrows():
        treeview.insert(parent='', index='end', values=list(row))


def search_new_tool_name(df):
    # Get the search term from the search bar
    search_term = new_tool_name_search_var.get()

    # Remove any existing items from the treeview
    treeview.delete(*treeview.get_children())

    # Add the column headings to the treeview
    treeview['columns'] = list(df.columns)
    for column in df.columns:
        treeview.heading(column, text=column)

    # Convert all columns to string data type
    df = df.astype(str)

    # Filter the dataframe based on the search term
    filtered_df = df[df['New Tool Name'].str.contains(search_term, case=False, na=False)]

    # Add the filtered data rows to the treeview
    filtered_df = filtered_df.reset_index(drop=True)  # Remove the index column
    for i, row in filtered_df.iterrows():
        treeview.insert(parent='', index='end', values=list(row))



# Create a tkinter window and treeview
root = tk.Tk()
treeview = ttk.Treeview(root, show='headings', height=25)

# Populate the treeview with the CSV data
populate_treeview(treeview, df)

# Create a search bar for the "Legacy Tool" column
legacy_tool_search_var = tk.StringVar()
legacy_tool_search_entry = tk.Entry(root, textvariable=legacy_tool_search_var)
legacy_label = ttk.Label(root, text='Search Legacy Tool Number')
legacy_label.grid(column=0, row=0)
legacy_tool_search_entry.grid(row=0, column=1)
legacy_tool_search_button = ttk.Button(
    root, text="Search", command=lambda: search_legacy_tool(df))
legacy_tool_search_button.grid(row=0, column=2)


# Create a search bar for the "New Tool Name" column
new_tool_name_search_var = tk.StringVar()
new_tool_name_search_entry = tk.Entry(
    root, textvariable=new_tool_name_search_var)
ntt_label = ttk.Label(root, text='Search New Tool Number')
ntt_label.grid(row=1, column=0)
new_tool_name_search_entry.grid(row=1, column=1)
new_tool_name_search_button = ttk.Button(
    root, text="Search", command=lambda: search_new_tool_name(df))
new_tool_name_search_button.grid(row=1, column=2)

reset_button = ttk.Button(
    root, text="Reset", command=lambda: populate_treeview(treeview, df))
reset_button.grid(row=2, column=1)
# Pack the treeview and start the tkinter event loop
treeview.grid(row=3, columnspan=3, padx=10, pady=10)
root.mainloop()
