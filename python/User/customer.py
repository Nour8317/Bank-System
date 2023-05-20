from . import user
import pandas as pd
from Util import sql


class Customer(user.User):
    street = ''
    city = ''
    zone = ''
    ssn = ''
    branch_id = 0

    def __init__(self, name, login, password, type, ssn, street, city, zone, id, branch_id):
        super().__init__(name, login, password, type, id)
        self.ssn = ssn
        self.street = street
        self.city = city
        self.zone = zone
        self.branch_id = branch_id

    def request_loan(self):
        loan_types = sql.get_all_loan_types(self.branch_id)
        index = 1
        for loan in loan_types:
            print(f'{index} - {loan.name}')
            index += 1
        loan_index = int(input('Please Choose Loan Type : ')) - 1
        if loan_index < 0 or loan_index >= len(loan_types):
            print('Invalid Index')
        amount = float(input('Loan Amount : '))
        try:
            sql.create_loan(loan_types[loan_index].id,
                            loan_types[loan_index].name, amount, self.id)
            print('Loan Created Successfully')
        except:
            print('An Error Occured')

    def view_loans(self):
        loans = sql.get_loans(customer_id=self.id)
        self.view_loans_table(loans)

    def start_loan(self):
        loans = sql.get_loans(customer_id=self.id)
        self.view_loans_table(loans)
        loan_index = int(input('Please Choose Loan to start its operation : '))
        if loan_index < 0 or loan_index >= len(loans):
            print('Invalid Index')
            return
        try:
            loans[loan_index].change_loan_state('opened')
            print('Operation Started Successfully')
        except:
            print('An Error Occured')
    def show_accounts(self):
        accounts = sql.get_accounts(self.id)
        data = {
            'type' : [account.type for account in accounts],
            'balance' : [account.balance for account in accounts],
        }
        df = pd.DataFrame(data)
        print(df)
    def print_menu(self):
        print("1-Show Loans.")#TODO
        print("2-Request Loan.")#TODO
        print("3-Start Operation On Loan.")#TODO
        print("4-Show Accounts.")
        print("5-Exit.")
    def update_name(self,new_value):
        sql.update_customer_name(self.id,new_value)
    def update_login(self,new_value):
        sql.update_customer_login(self.id,new_value)
    def app(self):
        choice = -1
        while choice != 5:
            self.print_menu()
            choice = int(input("Enter Your Choice Please: "))
            if choice == 1:
                self.view_loans()
            elif choice == 2:
                self.request_loan()
            elif choice == 3:
                self.start_loan()
            elif choice == 4:
                self.show_accounts()
