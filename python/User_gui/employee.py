from curses import window
from User.user import User
from tkinter import *
from tkinter import messagebox
from Util import sql
from tkinter import StringVar, ttk, OptionMenu
from PIL import Image, ImageTk
import pyodbc
import tkinter as tk

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

        lbl_name = Label(customer_window, text="Name:",bg="#d6e2e0",fg="#152238")
        lbl_name.grid(row=0, column=0, padx=(90, 0), pady=(70, 0))

        entry_name = Entry(customer_window)
        entry_name.grid(row=0, column=1, padx=10, pady=(70, 0))

        lbl_email = Label(customer_window, text="Email:", bg="#d7e3e1",fg="#152238")
        lbl_email.grid(row=0, column=0, padx=(90, 0), pady=(70, 0))

        entry_email = Entry(customer_window)
        entry_email.grid(row=0, column=1, padx=10, pady=(70, 0))

        lbl_ssn = Label(customer_window, text="ssn:", bg="#d7e3e1",fg="#152238")
        lbl_ssn.grid(row=1, column=0, padx=(75, 0), pady=(20, 0))

        entry_ssn = Entry(customer_window)
        entry_ssn.grid(row=1, column=1, padx=10, pady=(20, 0))

        lbl_branch_id = Label(customer_window, text="branch id:", bg="#d7e3e1",fg="#152238")
        lbl_ssn.grid(row=1, column=0, padx=(75, 0), pady=(20, 0))

        entry_branch_id = Entry(customer_window)
        entry_branch_id.grid(row=1, column=1, padx=10, pady=(20, 0))

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

        # Create a button to submit the customer information
        btn_submit = Button(customer_window, text="Submit", command=lambda: self.submit_customer_info(
            entry_name.get(),entry_email.get(), entry_ssn.get(),entry_branch_id.get(), entry_street.get(), entry_city.get(), entry_zone.get(), customer_window),
                            bg="#152238", fg="white", height=1, width=16)
        btn_submit.grid(row=5, column=0, columnspan=2, padx=(140, 0), pady=10)
    def submit_customer_info(self, name,email, ssn, branch_id, street, city, zone, customer_window):
     try:
            # Establish a connection to the database
            server = '34.123.49.27'
            database = 'BankSystem'
            username = 'sqlserver'
            password = '123456'
            driver = '{ODBC Driver 17 for SQL Server}'

            connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            insert_user_query = "INSERT INTO [User] (Name, Email, Password, UserType) VALUES (?, ?, ?, ?)"
            user_values = (name, email,None, "employee")
            cursor.execute(insert_user_query, user_values)
            connection.commit()

            # Retrieve the generated UserID for the new user
            select_user_query = "SELECT UserID FROM [User] WHERE Email = ?"
            cursor.execute(select_user_query, (email,))
            user_row = cursor.fetchone()
            user_id = user_row.UserID

            # Insert a record into the Customer table
            insert_customer_query = "INSERT INTO Customer (SSN, Street, City, CustomerID, Zone, BranchID) VALUES (?, ?, ?, ?, ?, ?)"
            customer_values = (ssn, street, city, user_id, zone, branch_id)
            cursor.execute(insert_customer_query, customer_values)
            connection.commit()

            messagebox.showinfo("Success", "Customer added successfully!")
            customer_window.destroy()
     except Exception as e:
        messagebox.showerror("Error", f"An error occurred while adding the customer:\n{str(e)}")


    def get_customers(self):
        # Create a new window for displaying loan types
        loan_types_window = Toplevel()
        loan_types_window.title("Show Customers")
        loan_types_window.configure(bg="#d6e2e0")

        # Create a treeview widget to display the loan types in a table
        tree = ttk.Treeview(loan_types_window, columns=("Name", "SSN", "City", "Zone", "Branch ID"), show="headings")
        tree.heading("Name", text="Name")
        tree.heading("SSN", text="SSN")
        tree.heading("City", text="City")
        tree.heading("Zone", text="Zone")
        tree.heading("Branch ID", text="Branch ID")

        tree.grid(row=0, column=0, padx=10, pady=10)

        # Fetch all customers from the database
        customers = self.sql.get_customers()

        # Insert customers into the treeview
        for customer in customers:
            tree.insert("", "end", values=(customer.name, customer.SSN, customer.city, customer.zone, customer.branch_id))



    def view_loans(self):
        
        loans = self.sql.get_loans("", "", "", self.branch_id)
        self.view_loans_table(loans)


    def view_loans_table(self, loans):
        # Create a new window for displaying loans
        loan_types_window = Toplevel()
        loan_types_window.title("Loans")
        loan_types_window.configure(bg="#d6e2e0")
 
        # Create a treeview widget to display the loan types in a table
        tree = ttk.Treeview(loan_types_window, columns=("loan_id", "state", "branchNO", "amount", "customer_id", "employee_id", "loan_type_id"), show="headings")
        tree.heading("loan_id", text="Loan ID")
        tree.heading("state", text="State")
        tree.heading("branchNO", text="Branch Number")
        tree.heading("amount", text="Amount")
        tree.heading("customer_id", text="Customer ID")
        tree.heading("employee_id", text="Employee ID")
        tree.heading("loan_type_id", text="Loan Type ID")
        tree.grid(row=0, column=0, padx=10, pady=10)

        types = self.sql.get_loans()

        # Create a dictionary to map loan states to their corresponding option values
        state_options = {
            "accept": "Accept",
            "reject": "Reject"
        }

        # Update the loan state in the treeview
        def change_loan_state(self, loan_id, state_var):
               new_state = state_var.get()
   
               self.sql.change_loan_state(loan_id, new_state)


        # Insert loans into the treeview
        for i, loan in enumerate(loans, start=1):
            state_var = StringVar()
            state_var.set(loan.state)  # Set the initial state value

            # Create a dropdown menu for selecting the state
            state_option_menu = OptionMenu(loan_types_window, state_var, *state_options.values(), command=lambda event, loan_id=loan.id, state_var=state_var: change_loan_state(self,loan_id, state_var))
            state_option_menu.grid(row=i, column=1, padx=10)

            tree.insert("", "end", values=(loan.id, loan.state, loan.branch_id, loan.amount, loan.customer_id, loan.employee_id, loan.loan_type_name))

    

    def add_account(self):
        # Create a new window for adding a customer
        customer_window = Toplevel()
        customer_window.title("Add account")
        customer_window.geometry("400x300")
        customer_window.configure(bg="#d6e2e0")

        lbl_name = Label(customer_window, text="Name:", bg="#d7e3e1",fg="#152238")
        lbl_name.grid(row=0, column=0, padx=(90, 0), pady=(70, 0))

        entry_name = Entry(customer_window)
        entry_name.grid(row=0, column=1, padx=10, pady=(70, 0))

        lbl_ssn = Label(customer_window, text="Balance:", bg="#d7e3e1",fg="#152238")
        lbl_ssn.grid(row=1, column=0, padx=(75, 0), pady=(20, 0))

        entry_ssn = Entry(customer_window)
        entry_ssn.grid(row=1, column=1, padx=10, pady=(20, 0))

        # Create a button to submit the customer information
        btn_submit = Button(customer_window, text="Submit", command=lambda: self.create_account(
            entry_name.get(), entry_ssn.get(), customer_window),
                            bg="#152238", fg="white", height=1, width=16)
        btn_submit.grid(row=5, column=0, columnspan=2, padx=(130, 0), pady=10)

    def create_account(self, customer_name, balance, customer_window):
        try:
            server = '34.123.49.27'
            database = 'BankSystem'
            username = 'sqlserver'
            password = '123456'
            driver = '{ODBC Driver 17 for SQL Server}'

            connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            # Retrieve the CustomerID based on the provided name
            select_customer_query = "SELECT UserID FROM [User] WHERE Name = ? AND UserType = 'customer'"
            cursor.execute(select_customer_query, (customer_name,))
            customer_row = cursor.fetchone()

            if customer_row is None:
                messagebox.showerror("Error", "Customer not found.")
                return

            customer_id = customer_row.UserID

            # Insert a new record into the Account table
            insert_account_query = "INSERT INTO Account (AccountType, Balance, CustomerID) VALUES (?, ?, ?)"
            account_values = ('account_type', balance, customer_id)
            cursor.execute(insert_account_query, account_values)
            connection.commit()

            messagebox.showinfo("Success", "Customer account created successfully!")
            customer_window.destroy()
        except pyodbc.Error as e:
            messagebox.showerror("Error", f"An error occurred while adding the account:\n{str(e)}")
        finally:
            cursor.close()
            connection.close()



   

    def update_name(self):
        # Create a new window for adding a customer
        customer_window = Toplevel()
        customer_window.title("update customer name")
        customer_window.geometry("400x300")
        customer_window.configure(bg="#d6e2e0")
    
        lbl_name = Label(customer_window, text="Customer ID:", bg="#d7e3e1",fg="#152238")
        lbl_name.grid(row=0, column=0, padx=(90, 0), pady=(70, 0))

        entry_name = Entry(customer_window)
        entry_name.grid(row=0, column=1, padx=10, pady=(70, 0))

        lbl_ssn = Label(customer_window, text="New Name:", bg="#d7e3e1",fg="#152238")
        lbl_ssn.grid(row=1, column=0, padx=(75, 0), pady=(20, 0))

        entry_ssn = Entry(customer_window)
        entry_ssn.grid(row=1, column=1, padx=10, pady=(20, 0))

        # Create a button to submit the customer information
        btn_submit = Button(customer_window, text="Submit", command=lambda: self.update_namee(
            entry_name.get(), entry_ssn.get(), customer_window),
                            bg="#152238", fg="white", height=1, width=16)
        btn_submit.grid(row=5, column=0, columnspan=2, padx=(160, 0), pady=10) 
    def update_namee(self, customer_id, new_name, customer_window):
        try:
            server = '34.123.49.27'
            database = 'BankSystem'
            username = 'sqlserver'
            password = '123456'
            driver = '{ODBC Driver 17 for SQL Server}'

            connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            # Check if the customer exists
            select_customer_query = "SELECT * FROM [User] WHERE UserID = ? AND UserType = 'customer'"
            cursor.execute(select_customer_query, (customer_id,))
            customer_row = cursor.fetchone()

            if customer_row is None:
                messagebox.showerror("Error", "Customer not found.")
                return

            # Update the customer's name
            update_name_query = "UPDATE [User] SET Name = ? WHERE UserID = ?"
            cursor.execute(update_name_query, (new_name, customer_id))
            connection.commit()

            messagebox.showinfo("Success", "Customer name updated successfully!")
            customer_window.destroy()
        except pyodbc.Error as e:
            messagebox.showerror("Error", f"An error occurred while updating the customer name:\n{str(e)}")
        finally:
            cursor.close()
            connection.close()
       
         
    
    def update_email(self):
        # Create a new window for adding a customer
        customer_window = Toplevel()
        customer_window.title("update customer Email")
        customer_window.geometry("400x300")
        customer_window.configure(bg="#d6e2e0")

        lbl_name = Label(customer_window, text="Customer ID:", bg="#d7e3e1",fg="#152238")
        lbl_name.grid(row=0, column=0, padx=(90, 0), pady=(70, 0))

        entry_name = Entry(customer_window)
        entry_name.grid(row=0, column=1, padx=10, pady=(70, 0))

        lbl_ssn = Label(customer_window, text="New E-mail:", bg="#d7e3e1",fg="#152238")
        lbl_ssn.grid(row=1, column=0, padx=(75, 0), pady=(20, 0))

        entry_ssn = Entry(customer_window)
        entry_ssn.grid(row=1, column=1, padx=10, pady=(20, 0))

        # Create a button to submit the customer information
        btn_submit = Button(customer_window, text="Submit", command=lambda: self.update_email(
            entry_name.get(), entry_ssn.get(), customer_window),
                            bg="#152238", fg="white", height=1, width=16)
        btn_submit.grid(row=5, column=0, columnspan=2, padx=(160, 0), pady=10)    


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