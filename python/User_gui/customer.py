from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from User import user

class Customer(user.User):

    def __init__(self,sql, name, login, password, type, ssn, street, city, zone, id, branch_id):
        super().__init__(sql,name, login, password, type, id)
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

       
        lbl_loan_type = Label(branch_window, text="Loan Type:",  bg="#d6e2e0",fg="#152238")
        lbl_loan_type.grid(row=0, column=0, padx=10, pady=10)

        entry_loan_type = Entry(branch_window)
        entry_loan_type.grid(row=0, column=1, padx=10, pady=10)

        lbl_loan_amount = Label(branch_window, text="Loan Amount:", bg="#d6e2e0",fg="#152238")
        lbl_loan_amount.grid(row=1, column=0, padx=10, pady=10)

        entry_loan_amount = Entry(branch_window)
        entry_loan_amount.grid(row=1, column=1, padx=10, pady=10)

        
        btn_submit = Button(branch_window, text="Submit", command=lambda: self.submit_branch_info(
            entry_loan_type.get(), entry_loan_amount.get(), branch_window), bg="#152238", fg="white", height=2, width=10)
        btn_submit.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def submit_branch_info(self, loan_type, loan_amount, branch_window):
        try:
            self.sql.add_branch(loan_type, loan_amount)
            messagebox.showinfo("Success", "Loan created successfully!")
            branch_window.destroy()
        except Exception as e:
            print("An error occurred while adding the branch:", e)
            messagebox.showerror("Error", "An error occurred while adding the branch.")

    def show_loans(self):
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

        btn_start_loan = Button(loan_types_window, text="Start Loan", command=lambda: self.start_loan(entry_loan_id.get()), bg="#173A69", fg="white", height=2, width=10)
        btn_start_loan.grid(row=1, column=2, padx=10, pady=10)

    def start_loan(self, loan_id):
       
        messagebox.showinfo("Loan Started", f"Loan {loan_id} started successfully!")

    def view_loans(self):
        loans = self.sql.get_loans()
        self.view_loans_table(loans)



    def page(self):
        window = Tk()
        window.title("Customer Page")
        window.configure(bg="#d6e2e0")
        window.geometry("950x700")
        window.resizable(False, False)
   
        lbl_customer = Label(window, text="Welcome, Customer", font=("Helvetica", 40), fg="#152238", bg="#d6e2e0")
        lbl_customer.config(highlightthickness=0)
        lbl_customer.pack(pady=50)

        # First Row
        frame1 = Frame(window, bg="#d6e2e0")
        frame1.pack(pady=(130, 0), padx=80)

        btn_request_loan = Button(frame1, text="Request a loan", command=self.request_loan, bg="#152238", fg="white", height=7, width=50)
        btn_request_loan.pack(side="left")

        # Second Row
        frame2 = Frame(window, bg="#bcd0ce")
        frame2.pack(pady=50)

        btn_view_loans = Button(frame2, text="View loans and start a loan", command=self.show_loans, bg="#152238", fg="white", height=7, width=50)
        btn_view_loans.pack(side="left")

        # Return the window
        return window
