from curses import window
from User.user import User
from tkinter import *
from tkinter import messagebox
from Util import sql
from tkinter import StringVar, ttk, OptionMenu
from PIL import Image, ImageTk
import pyodbc
import tkinter as tk
import re

class Employee(User):
    pos = ''
    hire_date = ''
    branch_id = False

    def __init__(self,sql,name,login,password,type,pos,hire_date,id,branch_id):
        super().__init__(sql,name,login,password,type,id)
        self.hire_date = hire_date
        self.pos = pos
        self.branch_id = branch_id


    
    def add_customer(self):
        # Create a new window for adding a customer
        customer_window = Toplevel()
        customer_window.title("Add Customer")
        customer_window.geometry("400x400")
        customer_window.configure(bg="#d6e2e0")



        lbl_email = Label(customer_window, text="Email:", bg="#d7e3e1",fg="#152238")
        lbl_email.grid(row=0, column=0, padx=(90, 0), pady=(70, 0))

        entry_email = Entry(customer_window)
        entry_email.grid(row=0, column=1, padx=10, pady=(70, 0))

        lbl_ssn = Label(customer_window, text="ssn:", bg="#d7e3e1",fg="#152238")
        lbl_ssn.grid(row=1, column=0, padx=(75, 0), pady=(20, 0))

        entry_ssn = Entry(customer_window)
        entry_ssn.grid(row=1, column=1, padx=10, pady=(20, 0))

        lbl_street = Label(customer_window, text="Street:", bg="#d7e3e1",fg="#152238")
        lbl_street.grid(row=2, column=0, padx=(90, 0), pady=(20, 0))

        entry_street = Entry(customer_window)
        entry_street.grid(row=2, column=1, padx=10, pady=(20, 0))

        lbl_city = Label(customer_window, text="City:", bg="#d7e3e1",fg="#152238")
        lbl_city.grid(row=3, column=0, padx=(90, 0), pady=(20, 0))

        entry_city = Entry(customer_window)
        entry_city.grid(row=3, column=1, padx=10, pady=(20, 0))

        lbl_zone = Label(customer_window, text="Zone:", bg="#d7e3e1",fg="#152238")
        lbl_zone.grid(row=4, column=0, padx=(90, 0), pady=(20, 0))

        entry_zone = Entry(customer_window)
        entry_zone.grid(row=4, column=1, padx=10, pady=(20, 0))
        lbl_name = Label(customer_window, text="Name:",bg="#d6e2e0",fg="#152238")
        lbl_name.grid(row=5, column=0, padx=(90, 0), pady=(70, 0))

        entry_name = Entry(customer_window)
        entry_name.grid(row=5, column=1, padx=10, pady=(70, 0))
        # Create a button to submit the customer information
        btn_submit = Button(customer_window, text="Submit", command=lambda: self.submit_customer_info(
            entry_name.get(),entry_email.get(), entry_ssn.get(), entry_street.get(), entry_city.get(), entry_zone.get(), customer_window),
                            bg="#152238", fg="white", height=1, width=16)
        btn_submit.grid(row=6, column=0, columnspan=2, padx=(140, 0), pady=10)
    def submit_customer_info(self, name,email, ssn, street, city, zone, customer_window):
     try:
            self.sql.create_customer(name,email,city,street,zone,ssn,self.branch_id)
            messagebox.showinfo("Success", "Customer  created successfully!")

            customer_window.destroy()
     except Exception as e:
        messagebox.showerror("Error", f"An error occurred while adding the customer:\n{str(e)}")


    def get_customers(self):
        # Create a new window for displaying loan types
        loan_types_window = Toplevel()
        loan_types_window.title("Show Customers")
        loan_types_window.configure(bg="#d6e2e0")

        # Create a treeview widget to display the loan types in a table
        tree = ttk.Treeview(loan_types_window, columns=("Name", "SSN", "City", "Zone",), show="headings")
        tree.heading("Name", text="Name")
        tree.heading("SSN", text="SSN")
        tree.heading("City", text="City")
        tree.heading("Zone", text="Zone")

        tree.grid(row=0, column=0, padx=10, pady=10)

        # Fetch all customers from the database
        customers = self.sql.get_customers()

        # Insert customers into the treeview
        for customer in customers:
            tree.insert("", "end", values=(customer.name, re.sub(r'\d(?=\d{4})', '#', customer.ssn), customer.city, customer.zone,))



    def view_loans(self):
        
        loans = self.sql.get_loans("", "", "", self.branch_id)
        self.view_loans_table(loans)


    def view_loans_table(self, loans):
        loans = self.sql.get_loans(employee_id=self.id,branch_id=self.branch_id)
        branch_window,tree = self.view_loans_gui(loans)
        branch_window.title("Loans")
        branch_window.configure(bg="#d6e2e0")
        branch_window.resizable(False, False)
        # branch_window.geometry("400x350")
        def get_index():
            selected = tree.focus()
            index = int(tree.index(selected))
            return index
        container = ttk.Frame(branch_window)
        container.grid(row=1, column=0, padx=10, pady=10)
        btn_1 = Button(container, text="Accept", command=lambda: self.accept(loans[get_index()].id,loans[get_index()].state), bg="#152238", fg="white", height=2, width=10)
        btn_1.grid(row=0, column=0, padx=10, pady=10)
        btn_2 = Button(container, text="Reject", command=lambda: self.reject(loans[get_index()].id,loans[get_index()].state), bg="#152238", fg="white", height=2, width=10)
        btn_2.grid(row=0, column=1, padx=10, pady=10)
        btn_3 = Button(container, text="Pay", command=lambda: self.pay(loans[get_index()].id,loans[get_index()].state), bg="#152238", fg="white", height=2, width=10)
        btn_3.grid(row=0, column=2, padx=10, pady=10)
    def accept(self,loan_id,loan_state):
        try:   
            if loan_state != 'opened':
                return 
            self.sql.change_loan_state(loan_id,'accepted')
            self.sql.set_employee_id(loan_id,self.id)
            messagebox.showinfo("Success", "Accepted !!!")
        except pyodbc.Error as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")    
    def reject(self,loan_id,loan_state):
        try:   
            if loan_state != 'opened':
                return 
            self.sql.change_loan_state(loan_id,'rejected')
            self.sql.set_employee_id(loan_id,self.id)
            messagebox.showinfo("Success", "Rejected !!!")
        except pyodbc.Error as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")    
    def pay(self,loan_id,loan_state):
        try:   
            if loan_state != 'accepted':
                return 
            self.sql.change_loan_state(loan_id,'paid')
            self.sql.set_employee_id(loan_id,self.id)
            messagebox.showinfo("Success", "Paid !!!")
        except pyodbc.Error as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")   

    def add_account(self):
        # Create a new window for adding a customer
        customer_window = Toplevel()
        customer_window.title("Add account")
        customer_window.geometry("400x300")
        customer_window.configure(bg="#d6e2e0")

        lbl_name = Label(customer_window, text="Type :", bg="#d7e3e1",fg="#152238")
        lbl_name.grid(row=0, column=0, padx=(90, 0), pady=(70, 0))

        entry_name = Entry(customer_window)
        entry_name.grid(row=0, column=1, padx=10, pady=(70, 0))

        lbl_ssn = Label(customer_window, text="Balance:", bg="#d7e3e1",fg="#152238")
        lbl_ssn.grid(row=1, column=0, padx=(75, 0), pady=(20, 0))

        entry_ssn = Entry(customer_window)
        entry_ssn.grid(row=1, column=1, padx=10, pady=(20, 0))
        customers = self.sql.get_customers(self.branch_id)
        customer_dict = {f" {customer.name}" : customer.id for customer in customers}
        customer_dict[''] = 0
        lbl_customer = Label(customer_window, text="Customer :", bg="#d6e2e0",fg="#152238")
        lbl_customer.grid(row=2, column=0, padx=(90, 0), pady=(20, 0))
        customer_name = tk.StringVar(customer_window)
        selection_combo = ttk.Combobox(customer_window, textvariable=customer_name, values=list(customer_dict.keys()))
        selection_combo.grid(row=2, column=1, padx=10, pady=(20, 0))
        # Create a button to submit the customer information
        btn_submit = Button(customer_window, text="Submit", command=lambda: self.create_account(
            entry_name.get(), entry_ssn.get(),customer_dict[selection_combo.get()], customer_window),
                            bg="#152238", fg="white", height=1, width=16)
        btn_submit.grid(row=3, column=0, columnspan=2, padx=(130, 0), pady=10)

    def create_account(self, type, balance,customer_id, customer_window):
        try:    
            self.sql.create_account(customer_id,type,balance)
            messagebox.showinfo("Success", "Customer account created successfully!")
            customer_window.destroy()
        except pyodbc.Error as e:
            messagebox.showerror("Error", f"An error occurred while adding the account:\n{str(e)}")


   

    def update_name(self):
        # Create a new window for adding a customer
        customer_window = Toplevel()
        customer_window.title("update customer name")
        customer_window.geometry("400x300")
        customer_window.configure(bg="#d6e2e0")
        customers = self.sql.get_customers(self.branch_id)
        customer_dict = {f" {customer.name}" : customer.id for customer in customers}
        customer_dict[''] = 0
        lbl_customer = Label(customer_window, text="Customer :", bg="#d6e2e0",fg="#152238")
        lbl_customer.grid(row=0, column=0, padx=(90, 0), pady=(20, 0))
        customer_name = tk.StringVar(customer_window)
        selection_combo = ttk.Combobox(customer_window, textvariable=customer_name, values=list(customer_dict.keys()))
        selection_combo.grid(row=0, column=1, padx=10, pady=(20, 0))
        lbl_ssn = Label(customer_window, text="New Name:", bg="#d7e3e1",fg="#152238")
        lbl_ssn.grid(row=1, column=0, padx=(75, 0), pady=(20, 0))

        entry_ssn = Entry(customer_window)
        entry_ssn.grid(row=1, column=1, padx=10, pady=(20, 0))

        # Create a button to submit the customer information
        btn_submit = Button(customer_window, text="Submit", command=lambda: self.update_namee(
            entry_ssn.get(), customer_dict[selection_combo.get()], customer_window),
                            bg="#152238", fg="white", height=1, width=16)
        btn_submit.grid(row=5, column=0, columnspan=2, padx=(160, 0), pady=10) 
    def update_namee(self, new_name, customer_id, customer_window):
        try:
            self.sql.update_customer_name(customer_id,new_name)
            messagebox.showinfo("Success", "Customer name updated successfully!")
            customer_window.destroy()
        except pyodbc.Error as e:
            messagebox.showerror("Error", f"An error occurred while updating the customer name:\n{str(e)}")    
    def update_email(self):
        # Create a new window for adding a customer
        customer_window = Toplevel()
        customer_window.title("update customer username")
        customer_window.geometry("400x300")
        customer_window.configure(bg="#d6e2e0")
        customers = self.sql.get_customers(self.branch_id)
        customer_dict = {f" {customer.login}" : customer.id for customer in customers}
        customer_dict[''] = 0
        lbl_customer = Label(customer_window, text="Customer :", bg="#d6e2e0",fg="#152238")
        lbl_customer.grid(row=0, column=0, padx=(90, 0), pady=(20, 0))
        customer_name = tk.StringVar(customer_window)
        selection_combo = ttk.Combobox(customer_window, textvariable=customer_name, values=list(customer_dict.keys()))
        selection_combo.grid(row=0, column=1, padx=10, pady=(20, 0))
        lbl_ssn = Label(customer_window, text="New username:", bg="#d7e3e1",fg="#152238")
        lbl_ssn.grid(row=1, column=0, padx=(75, 0), pady=(20, 0))
        entry_ssn = Entry(customer_window)
        entry_ssn.grid(row=1, column=1, padx=10, pady=(20, 0))
        # Create a button to submit the customer information
        btn_submit = Button(customer_window, text="Submit", command=lambda: self.update_email_action(
            entry_ssn.get(), customer_dict[selection_combo.get()], customer_window),
                            bg="#152238", fg="white", height=1, width=16)
        btn_submit.grid(row=5, column=0, columnspan=2, padx=(160, 0), pady=10)   
    def update_email_action(self, new_name, customer_id, customer_window):
        try:
            self.sql.update_customer_login(customer_id,new_name)
            messagebox.showinfo("Success", "Customer name updated successfully!")
            customer_window.destroy()
        except pyodbc.Error as e:
            messagebox.showerror("Error", f"An error occurred while updating the customer name:\n{str(e)}")   

    def page(self):
        
        window = Tk()
        window.title("Employee Page")
        window.configure(bg="#d6e2e0")
        window.geometry("950x700")
        window.resizable(False, False)

        lbl_emloyee = Label(window, text="Welcome, Employee", font=("Helvetica", 40), fg="#152238", bg="#d6e2e0")
        lbl_emloyee.config(highlightthickness=0)
        lbl_emloyee.pack(pady=50)

        # Create an instance of the Employee class
        employee = self


        frame1 = Frame(window, bg="#d6e2e0")
        frame1.pack(pady=50)

        btn_add_customer = Button(frame1, text="Add Customer", command=employee.add_customer, bg="#152238", fg="white",
                                height=4, width=50)
        btn_add_customer.pack(side="left", padx=(30,0))

        btn_view_customers = Button(frame1, text="View All Customers", command=employee.get_customers, bg="#152238",
                                    fg="white", height=4, width=50)
        btn_view_customers.pack(side="left", padx=(30,0))


        frame2 = Frame(window, bg="#d6e2e0")
        frame2.pack(pady=50)

        btn_view_loans = Button(frame2, text="View Loans", command=employee.view_loans, bg="#152238", fg="white",
                                height=4, width=50)
        btn_view_loans.pack(side="left", padx=(30, 0))
        btn_add_acc = Button(frame2, text="Add Account", command=employee.add_account, bg="#152238", fg="white",
                                height=4, width=50)
        btn_add_acc.pack(side="left", padx=(30, 0))

        frame3 = Frame(window, bg="#d6e2e0")
        frame3.pack(pady=50)

        btn_view_loans = Button(frame3, text="Update Customer Name", command=employee.update_name, bg="#152238", fg="white",
                                height=4, width=50)
        btn_view_loans.pack(side="left", padx=(30, 0))
        btn_add_acc = Button(frame3, text="Update Customer E-mail", command=employee.update_email, bg="#152238", fg="white",
                                height=4, width=50)
        btn_add_acc.pack(side="left", padx=(30, 0))

        return window