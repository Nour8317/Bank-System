from . import user 
from Util import sql
import pandas as pd
import re
class Employee(user.User):
    pos = ''
    hire_date = ''
    branch_id = False
    def print_menu(self):
        print("1-Add Customer.")
        print("2-View All Customers.")
        print("3-Change Loan State.")
        print("4-Exit.")
    def app(self):
        choice = -1
        while choice != 4:
            self.print_menu()
            choice = int(input("Enter Your Choice Please: "))
            if choice == 1:
                self.add_customer()
            elif choice == 2:
                self.view_all_customers()
            elif choice == 3:
                self.change_loan_state()

    def __init__(self,name,login,password,type,pos,hire_date,id,branch_id):
        super().__init__(name,login,password,type,id)
        self.hire_date = hire_date
        self.pos = pos
        self.branch_id = branch_id

    def add_customer(self):
        name = input("Enter The Employee Name Please: ")
        city = input("Enter The Employee City Please: ")
        zone = input("Enter The Employee zone Please: ")
        street = input("Enter The Employee street Please: ")
        ssn = input("Enter The Employee ssn Please (14 digits): ")
        if len(ssn) != 14:
            print('Please Provide A valid ssn')
        login = input("Enter The Employee login Please: ")
        sql.create_customer(name,login,city,street,zone,ssn,self.branch_id)
    def view_all_customers(self):
        customers = sql.get_customers(self.branch_id)
        data = {
            'name' : [customer.name for customer in customers],
            'ssn' : [re.sub(r'\d(?=\d{4})', '#', customer.ssn) for customer in customers],
            'street' : [customer.street for customer in customers],
            'city' : [customer.city for customer in customers],
            'zone' : [customer.zone for customer in customers],
        }
        df = pd.DataFrame(data)
        print(df)
    def change_loan_state(self):#perform operation on loans(Accept,reject,paid)
        loans = sql.get_loans(employee_id=self.id)
        self.view_loans_table(loans)
        loan_index = int(input('Please Choose Loan to Change its state : '))
        if loan_index < 0 or loan_index >= len(loans):
            print('Invalid Index')
            return
        choosen_loan = loans[loan_index]
        open_loan_options = '1.accept\n2.reject'
        accept_loan_options = '1.pay'
        is_opened = choosen_loan.state == 'opened'
        if is_opened:
            print(open_loan_options)
        else:
            print(accept_loan_options)
        option = int(input('Your Action : '))
        if option == 1 and is_opened:
            choosen_loan.change_loan_state('accepted')
            choosen_loan.set_employee_id(self.id,self.branch_id)
        elif option == 2 and is_opened:
            choosen_loan.change_loan_state('rejected')
            choosen_loan.set_employee_id(self.id,self.branch_id)
        elif option == 1 and not is_opened:
            choosen_loan.change_loan_state('paid')

            
        



