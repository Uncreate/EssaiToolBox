import tkinter as tk
import sqlite3
from tkinter import ttk

class UserApp(ttk.Frame):
    def __init__(self, parent, app_type):
        super().__init__(parent)
        self.app_type = app_type
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.login_label = ttk.Label(self, text="Login:")
        self.login_label.grid(row=0, column=0, sticky=tk.W)
        self.login_entry = ttk.Entry(self)
        self.login_entry.grid(row=0, column=1, sticky=tk.W)
        self.password_label = ttk.Label(self, text="Password:")
        self.password_label.grid(row=1, column=0, sticky=tk.W)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1, sticky=tk.W)

        if self.app_type == "login":
            self.login_button = ttk.Button(self, text='Login', command=self.login)
            self.login_button.grid(row=2, column=0, sticky=tk.W)
            self.register_button = ttk.Button(self, text='Register', command=self.register)
            self.register_button.grid(row=2, column=1, sticky=tk.W)
        elif self.app_type == "register":
            self.password_confirm_label = ttk.Label(self, text="Confirm password:")
            self.password_confirm_label.grid(row=2, column=0, sticky=tk.W)
            self.password_confirm_entry = ttk.Entry(self, show="*")
            self.password_confirm_entry.grid(row=2, column=1, sticky=tk.W)
            self.register_button = ttk.Button(self, text='Register', command=self.register)
            self.register_button.grid(row=3, column=0, sticky=tk.W)

        self.quit_button = ttk.Button(self, text='Quit', command=self.quit)
        self.quit_button.grid(row=4, column=0, sticky=tk.W)

    def login(self):
        # Get the values from the login_entry and password_entry widgets
        login = self.login_entry.get()
        password = self.password_entry.get()
        # Check if the login and password match the ones in the database
        # Code to connect to the database and check the credentials goes here

    def register(self):
        # Get the values from the login_entry, password_entry and password_confirm_entry widgets
        login = self.login_entry.get()
        password = self.password_entry.get()
        confirm_password = self.password_confirm_entry.get()
        # Check if the password and confirm_password match and if the login is not already taken
    # Code to connect to the database and insert the new user goes here

class MainApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack()
        self.create_widgets()
    def create_widgets(self):
        self.login_button = ttk.Button(self, text='Login', command=self.login)
        self.login_button.pack()
        self.register_button = ttk.Button(self, text='Register', command=self.register)
        self.register_button.pack()

    def login(self):
        self.login_app = UserApp(self, "login")

    def register(self):
        self.register_app = UserApp(self, "register")
if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    app.mainloop()