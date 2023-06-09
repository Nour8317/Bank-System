import pandas as pd

class User():
    name = ''
    login = ''
    password = ''
    type = '' #'customer' or 'admin' or 'employee'
    id = 0
    def view_loans_table(self,loans):
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
    def app(self):
        pass
    def __init__(self,name,login,password,type,id):
        self.id = id
        self.name = name
        self.login = login
        self.password = password
        self.type = type