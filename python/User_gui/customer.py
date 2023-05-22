from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from User import user
import tkinter as tk

class Customer(user.User):
    def __init__(self, sql, name, login, password, type, ssn, street, city, zone, id, branch_id):
        super().__init__(sql, name, login, password, type, id)
        self.ssn = ssn
        self.street = street
        self.city = city
        self.zone = zone
        self.branch_id = branch_id

    def request_loan(self):
        branch_window = Toplevel()
        branch_window.title("Request Loan")
        branch_window.configure(bg="#d6e2e0")
        branch_window.resizable(False, False)
        branch_window.geometry("400x350")

        loans = self.sql.get_all_loan_types(self.branch_id)
        loans_dict = {loan.name: loan.id for loan in loans}

        lbl_loans = Label(branch_window, text="Loan:", bg="#d6e2e0", fg="#152238")
        lbl_loans.grid(row=0, column=0, padx=10, pady=(20, 0), sticky="w")

        loan_name = tk.StringVar(branch_window)
        selection_combo = ttk.Combobox(branch_window, textvariable=loan_name, values=list(loans_dict.keys()), width=25)
        selection_combo.grid(row=0, column=1, padx=10, pady=(20, 0), sticky="w")

        lbl_loan_amount = Label(branch_window, text="Loan Amount:", bg="#d6e2e0", fg="#152238")
        lbl_loan_amount.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        entry_loan_amount = Entry(branch_window, width=25)
        entry_loan_amount.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        btn_submit = Button(branch_window, text="Submit", command=lambda: self.submit_loan_info(
            loans_dict[loan_name.get()], entry_loan_amount.get()),
                            bg="#152238", fg="white", height=2, width=10)
        btn_submit.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Configure column weights to evenly distribute the space
        branch_window.grid_columnconfigure(0, weight=1)
        branch_window.grid_columnconfigure(1, weight=1)

        # Configure row weights to allow vertical centering
        branch_window.grid_rowconfigure(0, weight=1)
        branch_window.grid_rowconfigure(1, weight=1)
        branch_window.grid_rowconfigure(2, weight=1)

        branch_window.mainloop()


    def submit_loan_info(self, loan_type, loan_amount):
        try:
            self.sql.create_loan(loan_type," ", loan_amount,self.id,self.branch_id)
            messagebox.showinfo("Success", "Loan created successfully!")
           
        except Exception as e:
            print("An error occurred while adding the loan:", e)
            messagebox.showerror("Error", "An error occurred while adding the loan.")

    def show_loans_table(self):
        loan_types_window = Toplevel()
        loan_types_window.title("Loans")
        loan_types_window.configure(bg="#d6e2e0")
        loan_types_window.resizable(False, False)

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

        for loan in types:
            tree.insert("", "end", values=(loan.loan_id, loan.state, loan.branch_no, loan.amount, loan.customer_id, loan.employee_id, loan.loan_type_id))

        lbl_loan_id = Label(loan_types_window, text="Write Loan ID:")
        lbl_loan_id.grid(row=1, column=0, padx=10, pady=10)

        entry_loan_id = Entry(loan_types_window)
        entry_loan_id.grid(row=1, column=1, padx=10, pady=10)

        btn_start_loan = Button(loan_types_window, text="Start Loan", command=lambda: self.show_loan(entry_loan_id.get()), bg="#173A69", fg="white", height=2, width=10)
        btn_start_loan.grid(row=1, column=2, padx=10, pady=10)

    def show_loan(self, loan_id):
        messagebox.showinfo("Loan Started", f"Loan {loan_id} started successfully!")
    
    def start_loan(self):
        branch_window = Toplevel()
        branch_window.title("Start Loan")
        branch_window.configure(bg="#d6e2e0")
        branch_window.resizable(False, False)
        branch_window.geometry("400x350")

        lbl_loan_id = Label(branch_window, text="Loan ID:", bg="#d6e2e0", fg="#152238")
        lbl_loan_id.grid(row=0, column=0, padx=10, pady=10)

        entry_loan_id = Entry(branch_window)
        entry_loan_id.grid(row=0, column=1, padx=10, pady=10)

        btn_start = Button(branch_window, text="Start", command=lambda: self.process_loan(entry_loan_id.get(), branch_window), bg="#152238", fg="white", height=2, width=10)
        btn_start.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def process_loan(self, loan_id, branch_window):
        try:
            self.sql.start_loan(loan_id)
            messagebox.showinfo("Success", "Loan started successfully!")
            branch_window.destroy()
        except Exception as e:
            print("An error occurred while starting the loan:", e)
            messagebox.showerror("Error", "An error occurred while starting the loan.")



    def show_accounts(self):
        accounts_window = Toplevel()
        accounts_window.title("Accounts")
        accounts_window.configure(bg="#d6e2e0")
        accounts_window.resizable(False, False)

        tree = ttk.Treeview(accounts_window, columns=("type", "balance", "loan_type_id"), show="headings")
        tree.heading("type", text="Type")
        tree.heading("balance", text="Balance")
        tree.grid(row=0, column=0, padx=10, pady=10)

        accounts = self.sql.get_accounts()

        for account in accounts:
            tree.insert("", "end", values=(account.type, account.balance, account.loan_type_id))

    def page(self):
        window = Tk()
        window.title("Customer Page")
        window.configure(bg="#d6e2e0")
        window.geometry("950x700")
        window.resizable(False, False)

        lbl_customer = Label(window, text="Welcome, Customer", font=("Helvetica", 40), fg="#152238", bg="#d6e2e0")
        lbl_customer.pack(pady=60)

        frame1 = Frame(window, bg="#d6e2e0")
        frame1.pack(pady=15)

        btn_request_loan = Button(frame1, text="Request a loan", command=self.request_loan, bg="#152238", fg="white", height=6, width=40)
        btn_request_loan.grid(row=0, column=0, padx=(30, 20), pady=10)

        btn_view_loans = Button(frame1, text="View loans and start a loan", command=self.show_loans_table, bg="#152238", fg="white", height=6, width=40)
        btn_view_loans.grid(row=0, column=1, padx=(20, 30), pady=10)

        frame2 = Frame(window, bg="#d6e2e0")
        frame2.pack(pady=15)

        btn_start_loan = Button(frame2, text="Start Loan", command=self.start_loan, bg="#152238", fg="white", height=6, width=40)
        btn_start_loan.grid(row=0, column=0, padx=(30, 20), pady=10)

        btn_show_accounts = Button(frame2, text="Show accounts", command=self.show_accounts, bg="#152238", fg="white", height=6, width=40)
        btn_show_accounts.grid(row=0, column=1, padx=(20, 30), pady=10)



        window.mainloop()

