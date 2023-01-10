import subprocess
import time
import tkinter as tk
import tkinter.ttk as ttk

program_path = "C:\\Program Files (x86)\\HEIDENHAIN\\TNCremo\\TNCcmdPlus.exe"

procs = []
for i in range(1, 26):
    filename = f"./Data/tnccmd/HP-{i:02}.tnccmd"
    window_title = f"HP-{i:02}"
    proc = subprocess.Popen([program_path, filename], creationflags=subprocess.CREATE_NEW_CONSOLE)
    procs.append(proc)

root = tk.Tk()

class ProcessFrame(tk.Frame):
    def __init__(self, parent, procs, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.procs = procs
        self.labels = []
        self.create_widgets()

    def create_widgets(self):
        self.dropdown = ttk.Combobox(self, values=["All"] + [f"HP-{i:02}" for i in range(1, 26)], state='readonly') #, command=self.terminate_processes)
        self.dropdown.grid(row=0,column=0)
        for i in range(1, 26):
            label = tk.Label(self, text=f"HP-{i:02}")
            label.grid(row=i+1, column=0)
            self.labels.append(label)
        self.update_status()
        self.after(5000,self.update_status)
    
    def update_status(self):
        for i, p in enumerate(self.procs):
            label = self.labels[i]
            if p.poll() is None:
                label.config(text=f"HP-{i+1:02} (running)", background="green")
            else:
                label.config(text=f"HP-{i+1:02} (stopped)", background="red")

    def terminate_processes(self):
        selected = self.dropdown.get()
        if selected == "All":
            for p in self.procs:
                if p.poll() is None:
                    p.terminate()
        else:
            for i, p in enumerate(self.procs):
                if f"HP-{i+1:02}" == selected:
                    p.terminate()

process_frame = ProcessFrame(root, procs)
process_frame.pack()
root.mainloop()
