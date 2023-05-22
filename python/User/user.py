import pandas as pd
from curses import window
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import Tk, Label, Button, Frame
class User():
    name = ''
    login = ''
    password = ''
    type = '' #'customer' or 'admin' or 'employee'
    id = 0
    sql = ''
    def view_loans_gui(self,loans):
        # Create a new window for displaying loans
      # Create a new window for displaying loan types
        loan_types_window = Toplevel()
        loan_types_window.title("Loans")
        loan_types_window.configure(bg="#d6e2e0")
        loan_types_window.resizable(False, False)


        # Create a treeview widget to display the loan types in a table
        tree = ttk.Treeview(loan_types_window, columns=('loan_id',"loan_type", "amount", "customer", "Employee", "Branch", "state"), show="headings",selectmode='browse')
        tree.heading("loan_id", text="Loan ID")
        tree.heading("loan_type", text="Loan Type")
        tree.heading("amount", text="Amount")
        tree.heading("customer", text="Customer")
        tree.heading("Employee", text="Employee")
        tree.heading("Branch", text="Branch")
        tree.heading("state", text="State")
        tree.grid(row=0, column=0, padx=10, pady=10)
        # Fetch all loan types from the database
        # Insert loans into the treeview
        for i, loan in enumerate(loans, start=1):
             tree.insert("", "end", values=(loan.id,loan.loan_type_name, loan.amount, loan.get_customer_name(), loan.get_employee_name(), loan.get_branch_name(), loan.state))
        return loan_types_window,tree
    def view_loans_table(self,loans):
        if len(loans) == 0:
            print('Nothing to show')
            return False
        loan_data = {
        'Loan Type': [loan.loan_type_name for loan in loans],
        'Amount': [loan.amount for loan in loans],
        'Customer': [loan.get_customer_name() for loan in loans],
        'Employee': [loan.get_employee_name() for loan in loans],
        'Branch': [loan.get_branch_name() for loan in loans],
        'State': [loan.state for loan in loans]
        }
        df = pd.DataFrame(loan_data)
        print(df)
        return True
    def app(self):
        pass
    def __init__(self,sql,name,login,password,type,id):
        self.id = id
        self.name = name
        self.login = login
        self.password = password
        self.type = type
        self.sql = sql