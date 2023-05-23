from asyncio import DatagramProtocol
from curses import window
import dataclasses
from datetime import date
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from User import user
from tkinter import Tk, Label, Button, Frame
import tkinter as tk
import pyodbc
class Admin(user.User):
    def __init__(self,sql,name,login,password,type,id):
        super().__init__(sql,name,login,password,type,id)
    def add_bank(self):
        # Create a new window for adding a bank
        bank_window = Toplevel()
        bank_window.title("Add Bank")
        bank_window.configure(bg="#d6e2e0")
        bank_window.geometry("400x350")  # Set the window size here
        bank_window.resizable(False, False)
    
        lbl_bank_name = Label(bank_window, text="Bank Name:", bg="#d6e2e0",fg="#152238")
        lbl_bank_name.grid(row=0, column=0,  padx=(75, 0), pady=(70, 0))

        entry_bank_name = Entry(bank_window)
        entry_bank_name.grid(row=0, column=1, padx=10,pady=(70, 0))

        lbl_bank_city = Label(bank_window, text="Bank City:", bg="#d6e2e0",fg="#152238")
        lbl_bank_city.grid(row=1, column=0, padx=(75, 0), pady=(20, 0))

        entry_bank_city = Entry(bank_window)
        entry_bank_city.grid(row=1, column=1, padx=10, pady=(20, 0))

        lbl_bank_zone = Label(bank_window, text="Bank Zone:", bg="#d6e2e0",fg="#152238")
        lbl_bank_zone.grid(row=2, column=0, padx=(90, 0), pady=(20, 0))

        entry_bank_zone = Entry(bank_window)
        entry_bank_zone.grid(row=2, column=1, padx=10, pady=(20, 0))

        lbl_bank_street = Label(bank_window, text="Bank Street:", bg="#d6e2e0",fg="#152238")
        lbl_bank_street.grid(row=3, column=0, padx=(90, 0), pady=(20, 0))

        entry_bank_street = Entry(bank_window)
        entry_bank_street.grid(row=3, column=1, padx=10, pady=(20, 0))

        # Create a button to submit the bank information
        btn_submit = Button(bank_window, text="Submit", command=lambda: self.submit_bank_info(
            entry_bank_name.get(), entry_bank_city.get(), entry_bank_zone.get(), entry_bank_street.get(), bank_window),
                            bg="#152238", fg="white", height=1, width=16)
        btn_submit.grid(row=4, column=0, columnspan=2, padx=(160, 0), pady=10)

    def submit_bank_info(self, bank_name, bank_city, bank_zone, bank_street, bank_window):
     try:
       if any(p == '' for p in (  bank_name, bank_city, bank_zone, bank_street, bank_window)):
            e = "Error Empty parameter is not allowed"
            messagebox.showerror("Error" , e)
            return
        # Establish a connection to the database
       server = '34.123.49.27'
       database = 'BankSystem'
       username = 'sqlserver'
       password = '123456'
       driver = '{ODBC Driver 17 for SQL Server}'

       connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
       connection = pyodbc.connect(connection_string)
       cursor = connection.cursor()
       query = "INSERT INTO Bank (Name, City, Zone, Street) VALUES (?, ?, ?, ?)"
       values = (bank_name, bank_city, bank_zone, bank_street)

        # Execute the query
       cursor.execute(query, values)
       connection.commit()
       messagebox.showinfo("Success", "Bank created successfully!")
       bank_window.destroy()
     except Exception as e:
        messagebox.showerror("Error", f"An error occurred while adding the bank:\n{str(e)}")
    


    def add_branch(self):
        # Create a new window for adding a branch
        branch_window = Toplevel()
        branch_window.title("Add branch")
        branch_window.configure(bg="#d6e2e0")
        branch_window.geometry("400x350")  # Set the window size here
        branch_window.resizable(False, False)

        lbl_branch_city = Label(branch_window, text="branch City:", bg="#d6e2e0",fg="#152238")
        lbl_branch_city.grid(row=1, column=0, padx=(75, 0), pady=(20, 0))

        entry_branch_city = Entry(branch_window)
        entry_branch_city.grid(row=1, column=1, padx=10, pady=(20, 0))

        lbl_branch_zone = Label(branch_window, text="branch street:", bg="#d6e2e0",fg="#152238")
        lbl_branch_zone.grid(row=2, column=0, padx=(90, 0), pady=(20, 0))

        entry_branch_zone = Entry(branch_window)
        entry_branch_zone.grid(row=2, column=1, padx=10, pady=(20, 0))

        lbl_branch_street = Label(branch_window, text="branch zone:", bg="#d6e2e0",fg="#152238")
        lbl_branch_street.grid(row=3, column=0, padx=(90, 0), pady=(20, 0))

        entry_branch_street = Entry(branch_window)
        entry_branch_street.grid(row=3, column=1, padx=10, pady=(20, 0))      

        banks = self.sql.get_banks()
        banks_dict = {bank.name : bank.id for bank in banks}
        banks_dict[''] = 0
        lbl_banks = Label(branch_window, text="Bank :", bg="#d6e2e0",fg="#152238")
        lbl_banks.grid(row=4, column=0, padx=(90, 0), pady=(20, 0))
        bank_name = tk.StringVar(branch_window)
        selection_combo = ttk.Combobox(branch_window, textvariable=banks_dict, values=list(banks_dict.keys()))
        selection_combo.grid(row=4, column=1, padx=10, pady=(20, 0))

        btn_submit = Button(branch_window, text="Submit", command=lambda: self.submit_branch_info(
            banks_dict[selection_combo.get()], entry_branch_city.get(), entry_branch_zone.get(), entry_branch_street.get(), bank_name.get()),
                            bg="#152238", fg="white", height=1, width=16)
        btn_submit.grid(row=5, column=0, columnspan=2, padx=(160, 0), pady=10)

    def submit_branch_info(self, bank_id, branch_city, branch_zone, branch_street, bank_name):
     try:
        if any(p == '' for p in ( bank_id, branch_city, branch_zone, branch_street, bank_name)):
                e = "Error Empty parameter is not allowed"
                messagebox.showerror("Error" , e)
                return
        self.sql.add_branch(branch_city,branch_zone,branch_street,bank_id,bank_name)
        messagebox.showinfo("Success", "branch created successfully!")
     except Exception as e:
        messagebox.showerror("Error", f"An error occurred while adding the branch:\n{str(e)}")

    def add_employee(self):
        branch_window = Toplevel()
        branch_window.title("Add Employee")
        branch_window.configure(bg="#d6e2e0")
        branch_window.geometry("400x350")  # Set the window size here
        branch_window.resizable(False, False)

        lbl_Employee_Name = Label(branch_window, text="Employee Name:", bg="#d6e2e0",fg="#152238")
        lbl_Employee_Name.grid(row=1, column=0, padx=(75, 0), pady=(20, 0))
        
        lbl_Employee_Name = Entry(branch_window)
        lbl_Employee_Name.grid(row=1, column=1, padx=10, pady=(20, 0))
    
        lbl_Employee_HireYear= Label(branch_window, text="Employee Hire Year:", bg="#d6e2e0",fg="#152238")
        lbl_Employee_HireYear.grid(row=2, column=0, padx=(90, 0), pady=(20, 0))

        lbl_Employee_HireYear = Entry(branch_window)
        lbl_Employee_HireYear.grid(row=2, column=1,padx=10, pady=(20, 0))

        lbl_Employee_HireMonth = Label(branch_window, text="Employee Hire Month:", bg="#d6e2e0",fg="#152238")
        lbl_Employee_HireMonth.grid(row=3, column=0, padx=(90, 0), pady=(20, 0))

        lbl_Employee_HireMonth = Entry(branch_window)
        lbl_Employee_HireMonth.grid(row=3, column=1,padx=10, pady=(20, 0))

        lbl_Employee_HireDay = Label(branch_window, text="Employee Hire Day:", bg="#d6e2e0",fg="#152238")
        lbl_Employee_HireDay.grid(row=4, column=0,padx=(90, 0), pady=(20, 0))

        lbl_Employee_HireDay = Entry(branch_window)
        lbl_Employee_HireDay.grid(row=4, column=1,padx=10, pady=(20, 0))

        lbl_Employee_Position = Label(branch_window, text="Employee Position:", bg="#d6e2e0",fg="#152238")
        lbl_Employee_Position.grid(row=5, column=0, padx=(90, 0), pady=(20, 0))

        lbl_Employee_Position = Entry(branch_window)
        lbl_Employee_Position.grid(row=5, column=1,padx=10, pady=(20, 0))

        bl_Employee_login = Label(branch_window, text="Employee login:", bg="#d6e2e0",fg="#152238")
        bl_Employee_login.grid(row=6, column=0, padx=(90, 0), pady=(20, 0))

        bl_Employee_login = Entry(branch_window)
        bl_Employee_login.grid(row=6, column=1, padx=10, pady=(20, 0))   

        Branch = self.sql.get_branches()
        Branch_dict = {f" {Branch.bank_name} - {Branch.city} - {Branch.street}" : Branch.id for Branch in Branch}
        Branch_dict[''] = 0
        lbl_Branch = Label(branch_window, text="Branch :", bg="#d6e2e0",fg="#152238")
        lbl_Branch.grid(row=7, column=0, padx=(90, 0), pady=(20, 0))
        branch_name = tk.StringVar(branch_window)
        selection_combo = ttk.Combobox(branch_window, textvariable=Branch_dict, values=list(Branch_dict.keys()))
        selection_combo.grid(row=7, column=1, padx=10, pady=(20, 0))

        btn_submit = Button(branch_window, text="Submit", command=lambda: self.submit_Employee_info(
            lbl_Employee_Name.get(),bl_Employee_login.get(),lbl_Employee_Position.get(),lbl_Employee_HireYear.get(),lbl_Employee_HireMonth.get(),lbl_Employee_HireDay.get(),Branch_dict[selection_combo.get()]),
                            bg="#152238", fg="white", height=1, width=16)
        btn_submit.grid(row=8, column=0, columnspan=2, padx=(160, 0), pady=10)

    def submit_Employee_info(self, name, login, pos,hire_year,hire_day,hire_month,branch_id):
        try:
            if any(p == '' for p in (name, login, pos, branch_id)):
                e = "Error Empty parameter is not allowed"
                messagebox.showerror("Error" , e)
                return
            hire_date = date(int(hire_year),int(hire_month),int(hire_day))
            self.sql.create_employee(name, login, pos, hire_date, branch_id)
            messagebox.showinfo("Success", "Employee created successfully!")
        except ValueError as e:
            messagebox.showerror("Error", f"An Error Occurred While Adding The Employee: \n{str(e)}")



    def view_all_loan_types(self):
        
        loan_types_window = Toplevel()
        loan_types_window.title("Loan Types")
        loan_types_window.configure(bg="#d6e2e0")
        loan_types_window.resizable(False, False)

       
        tree = ttk.Treeview(loan_types_window, columns=("Name", "ID", "Branch"), show="headings")
        tree.heading("Name", text="Name")
        tree.heading("ID", text="ID")
        tree.grid(row=0, column=0, padx=10, pady=10)

        types = self.sql.get_all_loan_types()

        for i, loan_type in enumerate(types, start=1):
            tree.insert("", "end", values=(loan_type.name, loan_type.id))


    def view_loans(self):

        loans = self.sql.get_loans()
        self.view_loans_table(loans)

    def view_loans_table(self, loans):
        loans = self.sql.get_loans()
        self.view_loans_gui(loans)

    def show_banks(self):
        window = tk.Tk()
        window.title("Banks") 
        table = ttk.Treeview(window, columns=("Bank Name", "Bank Address","Branches"))
        
        table.heading("#0", text="ID")
        table.heading("Bank Name", text="Bank Name")
        table.heading("Bank Address", text="Bank Address")
        table.heading("Branches", text="Branches Count")

        banks = self.sql.get_banks_for_report()
        total_branches = sum([b.branches_count for b in banks])
        for i,bank in enumerate(banks, start=1):
            table.insert("", "end", text=str(i), values=(bank.name, f'{bank.city} - {bank.zone} - {bank.street}', bank.branches_count))
        table.insert("", "end", text="Total", values=("","",total_branches))

        table.pack()
        window.mainloop() 
    def show_branches(self):
        window = tk.Tk()
        window.title("Branches")
    
        table = ttk.Treeview(window, columns=("Bank Name","Branch Address","n_e","n_c","n_a","n_l"))
                
        table.heading("#0", text="ID")
        table.heading("Bank Name", text="Bank Name")
        table.heading("Branch Address", text="Branch Address")
        table.heading("n_e", text="No. Of employees")
        table.heading("n_c", text="No. Of Customers")
        table.heading("n_a", text="No. Of Accounts")
        table.heading("n_l", text="No. Of loans")
        branches = self.sql.get_branches_for_report()
        t_c = sum([b.no_of_customers for b in branches])
        t_e = sum([b.no_of_employees for b in branches])
        t_l = sum([b.no_of_loans for b in branches])
        t_a = sum([b.no_of_account for b in branches])

        for i,branch in enumerate(branches, start=1):
            table.insert("", "end", text=str(i), values=
(branch.bank_name, f'{branch.city} - {branch.zone} - {branch.street}', 
 branch.no_of_employees,branch.no_of_customers,branch.no_of_account,branch.no_of_loans)
                         )
        table.insert("", "end", text="Total", values=("","",t_e,t_c,t_a,t_l))
        table.pack()
        window.mainloop() 

    def show_loans(self):
        loans = self.sql.get_loans()
        _,table = self.view_loans_gui(loans)
        table.insert("", "end",values=("Total","","","","","",sum([l.amount for l in loans])))
        table.insert("", "end",values=("Total Paid","","","","","",sum([l.amount for l in loans if l.state == 'paid'])))
        table.insert("", "end",values=("Total Accepted","","","","","",sum([l.amount for l in loans if l.state == 'accepted'])))
        table.insert("", "end",values=("Total Rejected","","","","","",sum([l.amount for l in loans if l.state == 'rejected'])))

    def show_account(self):
        
        accounts_window = Toplevel()
        accounts_window.title("Accounts")
        accounts_window.configure(bg="#d6e2e0")
        accounts_window.resizable(False, False)
        tree = ttk.Treeview(accounts_window, columns=("c","b","type", "balance"), show="headings")
        tree.heading("c", text="Customer")
        tree.heading("b", text="Branch")
        tree.heading("type", text="Type")
        tree.heading("balance", text="Balance")
        tree.grid(row=0, column=0, padx=10, pady=10)
        accounts = self.sql.get_accounts_for_report()
        for account in accounts:
            tree.insert("", "end", values=(account.customer_name,account.branch_name,account.type, account.balance))


    def show_report(self):
        admin_window = Tk()
        admin_window.title("report page")
        admin_window.configure(bg="#d6e2e0")
        admin_window.geometry("850x600")
        admin_window.resizable(False, False)
    
        lbl_admin = Label(admin_window, text="choose what you want to view", font=("Helvetica", 30), fg="#152238", bg="#d6e2e0")
        lbl_admin.config(highlightthickness=0)
        lbl_admin.pack(pady=30)
        frame1 = Frame(admin_window, bg="#d6e2e0")
        frame1.pack(pady=(50, 0), padx=80)

        btn_add_employee = Button(frame1, text="list of banks", command=self.show_banks, bg="#152238", fg="white", height=5, width=30)
        btn_add_employee.pack(side="left", padx=(0, 50))

        btn_add_bank = Button(frame1, text="list of branches", command=self.show_branches, bg="#152238", fg="white", height=5, width=30)
        btn_add_bank.pack(side="left", padx=(0, 50))


        frame2 = Frame(admin_window, bg="#d6e2e0")
        frame2.pack(pady=(50, 0), padx=80)

        btn_view_loan_types = Button(frame2, text="list of loans", command=self.show_loans, bg="#152238", fg="white", height=5, width=30)
        btn_view_loan_types.pack(side="left", padx=(0, 50))

        btn_add_branch = Button(frame2, text="list of accounts", command=self.show_account, bg="#152238", fg="white", height=5, width=30)
        btn_add_branch.pack(side="left", padx=(0, 50))   




    def page(self):
        admin_window = Tk()
        admin_window.title("Admin Page")
        admin_window.configure(bg="#d6e2e0")
        admin_window.geometry("850x600")
        admin_window.resizable(False, False)
    
        lbl_admin = Label(admin_window, text="Welcome, Admin", font=("Helvetica", 30), fg="#152238", bg="#d6e2e0")
        lbl_admin.config(highlightthickness=0)
        lbl_admin.pack(pady=30)
        frame1 = Frame(admin_window, bg="#d6e2e0")
        frame1.pack(pady=(50, 0), padx=80)

        btn_add_employee = Button(frame1, text="Add Employee", command=self.add_employee, bg="#152238", fg="white", height=5, width=30)
        btn_add_employee.pack(side="left", padx=(0, 50))

        btn_add_bank = Button(frame1, text="Add Bank", command=self.add_bank, bg="#152238", fg="white", height=5, width=30)
        btn_add_bank.pack(side="left", padx=(0, 50))


        frame2 = Frame(admin_window, bg="#d6e2e0")
        frame2.pack(pady=(50, 0), padx=80)

        btn_view_loan_types = Button(frame2, text="View All Loan Types", command=self.view_all_loan_types, bg="#152238", fg="white", height=5, width=30)
        btn_view_loan_types.pack(side="left", padx=(0, 50))

        btn_add_branch = Button(frame2, text="Add Branch", command=self.add_branch, bg="#152238", fg="white", height=5, width=30)
        btn_add_branch.pack(side="left", padx=(0, 50))


        frame3 = Frame(admin_window, bg="#d6e2e0")
        frame3.pack(pady=(50, 0), padx=80)

        btn_view_loans = Button(frame3, text="View Loans", command=self.view_loans, bg="#152238", fg="white", height=5, width=30)
        btn_view_loans.pack(side="left", padx=(0, 50))

        btn_view_loan_types = Button(frame3, text="Meaningful Report", command=self.show_report, bg="#152238", fg="white", height=5, width=30)
        btn_view_loan_types.pack(side="left", padx=(0, 50))

        
        return admin_window
        