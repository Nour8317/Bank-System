from tkinter import *
from PIL import Image, ImageTk
import os
from tkinter import Tk, Label, Button, Frame
from tkinter import messagebox
import pyodbc
import sys
from User_gui import customer
from User_gui import admin as admin_file
from User_gui import employee
from Util.sql import SQL
file_path = os.path.abspath(sys.argv[0])

# Get the parent directory of the file
parent_directory = os.path.dirname(file_path)
sql = SQL()
class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Page")
        # background_image = Image.open(os.path.join(parent_directory,'/Bank-System/python/back.jpg'))
        # background_image = background_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.ANTIALIAS)
        # self.background_photo = ImageTk.PhotoImage(background_image)
        # background_label = Label(root, image=self.background_photo)
        # background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # login_image = Image.open(os.path.join(parent_directory,'/Bank-System/python/log.png'))
        # login_image = login_image.resize((180, 160), Image.ANTIALIAS)
        # self.login_photo = ImageTk.PhotoImage(login_image)
        # login_label = Label(root, image=self.login_photo,bg="#d8e4e2")
        # login_label.grid(row=0, column=0, columnspan=2, pady=(80,0))

        
        lbl_username = Label(root, text="Username ", font=("Helvetica", 20), fg="#152238", bg="#d6e2e0")
        lbl_username.config(highlightthickness=0)
        lbl_username.grid(row=1, column=0, padx=10, sticky=E,pady=(60, 0))

        self.entry_username = Entry(root, width=30)  
        self.entry_username.grid(row=1, column=1, padx=10,sticky=W,pady=(60, 0))

       
        lbl_password = Label(root, text="Password ", font=("Helvetica", 20), fg="#152238", bg="#d6e2e0")
        lbl_password.config(highlightthickness=0)
        lbl_password.grid(row=2, column=0, padx=15, pady=(30,0), sticky=E)

        self.entry_password = Entry(root, show="*", width=30)  
        self.entry_password.grid(row=2, column=1, padx=10, pady=(30,0), sticky=W)

        btn_login = Button(root, text="Login", command=self.login, bg="#152238", fg="white", height=3, width=25)
        btn_login.grid(row=3, column=0, columnspan=2, pady=100)

        for i in range(root.grid_size()[0]):
            root.grid_columnconfigure(i, weight=1)

        for i in range(root.grid_size()[1]):
            root.grid_rowconfigure(i, weight=1)

    def login(self):
        user = self.entry_username.get()
        passw = self.entry_password.get()
        current_user = sql.login(user,passw)
        if not current_user:
            messagebox.showerror("Error", "Invalid Credintials")
        current_user.page()



        
root = Tk()
root.config(bg="#d8e4e2")
login_page = LoginPage(root)
root.geometry("500x600")
root.resizable(False, False)
root.mainloop()