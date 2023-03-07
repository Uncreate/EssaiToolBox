import tkinter as tk
from tkinter import ttk
import json



class TapToolsGUI(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack()

        # Load the JSON file
        with open("C:\\Users\\adam.riggs\\OneDrive - Advantest\\EssaiControlPanel\\MasterToolDatabase.txt") as f:
            data = json.load(f)

        # Find all objects in the list where `NAME` contains 36 or 37 in the 4th and 5th position
        self.tap_tools = []
        for item in data['tools']:
            name = item.get('tool_name')
            if name is not None and len(name) >= 5 and name[3:5] in ['36', '37']:
                sc_pitch = item.get('drilling_tool', {}).get('Pitch')
                doc = item.get('Solfex', {}).get('DOC')
                if doc is not None:
                    doc = doc[3:-4]  # Remove the first 3 and last 4 characters
                self.tap_tools.append(
                    {'name': name, 'sc_pitch': sc_pitch, 'doc': doc})

        # Create a Frame for the search box
        self.search_frame = ttk.Frame(self)
        self.search_frame.pack(side='top', fill='x')

        # Create an Entry widget for the search string
        self.search_entry = ttk.Entry(self.search_frame)
        self.search_entry.pack(side='left', padx=10, pady=10)

        # Create a Button to trigger the search
        self.search_button = ttk.Button(
            self.search_frame, text='Search', command=self.search)
        self.search_button.pack(side='left', padx=10, pady=10)

        # Create a Frame for the Treeview and scrollbar
        self.frame = ttk.Frame(self)
        self.frame.pack(padx=10, pady=10)

        # Create a Treeview widget
        self.tree = ttk.Treeview(self.frame, columns=(
            'rfid_pitch', 'sc_pitch', 'pitch', 'doc'), height=30)
        self.tree.heading('#0', text='Tool Name')
        self.tree.heading('rfid_pitch', text='RFID Pitch')
        self.tree.heading('sc_pitch', text='SolidCam Pitch')
        self.tree.heading('pitch', text='Program Pitch')
        self.tree.heading('doc', text='Tap Type')
        self.tree.column('rfid_pitch', width=100, anchor='center')
        self.tree.column('sc_pitch', width=100, anchor='center')
        self.tree.column('doc', width=100, anchor='center')
        self.tree.column('pitch', width=100, anchor='center')

        # Define tags to highlight rows that meet the condition and alternate row colors
        self.tree.tag_configure('red', background='#ADD8E6')
        self.tree.tag_configure('odd', background='#f0f0f0')
        self.tree.tag_configure('even', background='#ffffff')

        # Add the tool information to the Treeview
        for tool in self.tap_tools:
            fSolidcam_pitch = '{:.7f}'.format(tool['sc_pitch'])
            fRfid_pitch = '{:.4f}'.format(tool['sc_pitch'])
            fProgram_pitch = '{:.6f}'.format(tool['sc_pitch'])
            item = self.tree.insert('', 'end', text=tool['name'], values=(
                fRfid_pitch, fSolidcam_pitch, fProgram_pitch, tool['doc']))

        # Create a vertical scrollbar and attach it
        self.vsb = ttk.Scrollbar(
            self.frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side='right', fill='y')

        # Pack the Treeview widget
        self.tree.pack(side='left', fill='both', expand=True)

    def search(self):
        search_string = self.search_entry.get().lower()
        found_row = None
        for i, tool in enumerate(self.tap_tools):
            if search_string in tool['name'].lower():
                self.tree.item(self.tree.get_children()[i], tags=(
                    'red', 'odd' if i % 2 == 0 else 'even'))
                if found_row is None:
                    found_row = self.tree.get_children()[i]
        if found_row is not None:
            self.tree.see(found_row)
            self.tree.selection_set(found_row)
        else:
            self.tree.selection_clear()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Solfex TAP')
    gui = TapToolsGUI(root)
    root.mainloop()
    
