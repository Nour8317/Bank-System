from . import user 
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
        print("4-Update Customer.")
        print("5-Add Account.")
        print("6-Exit.")
    def app(self):
        choice = -1
        while choice != 6:
            self.print_menu()
            choice = int(input("Enter Your Choice Please: "))
            if choice == 1:
                self.add_customer()
            elif choice == 2:
                self.view_all_customers()
            elif choice == 3:
                self.change_loan_state()
            elif choice == 4:
                self.update_customer()
            elif choice == 5:
                self.add_account()

    def __init__(self,sql,name,login,password,type,pos,hire_date,id,branch_id):
        super().__init__(sql,name,login,password,type,id)
        self.hire_date = hire_date
        self.pos = pos
        self.branch_id = branch_id

    def add_customer(self):
        name = input("Enter The Customer Name Please: ")
        city = input("Enter The Customer City Please: ")
        zone = input("Enter The Customer zone Please: ")
        street = input("Enter The Customer street Please: ")
        ssn = input("Enter The Customer ssn Please (14 digits): ")
        if len(ssn) != 14:
            print('Please Provide A valid ssn')
            return
        login = input("Enter The Customer login Please: ")
        try:
            self.sql.create_customer(name,login,city,street,zone,ssn,self.branch_id)
            print('Customer Created Successfully !!')
        except Exception as e:
            print(e)
    def show_customers(self,customers):
        data = {
            'name' : [customer.name for customer in customers],
            'ssn' : [re.sub(r'\d(?=\d{4})', '#', customer.ssn) for customer in customers],
            'street' : [customer.street for customer in customers],
            'city' : [customer.city for customer in customers],
            'zone' : [customer.zone for customer in customers],
        }
        df = pd.DataFrame(data)
        print(df)
    def view_all_customers(self):
        customers = self.sql.get_customers(self.branch_id)
        self.show_customers(customers)
    def get_choosen_customer(self):
        customers = self.sql.get_customers(self.branch_id)
        self.show_customers(customers)
        index = int(input('Please Choose Customer To Update: '))
        if index < 0 or index >= len(customers):
            print('Invalid Index')
            return False
        return customers[index]
    def update_customer(self):
        choosen_customer = self.get_choosen_customer()
        if not choosen_customer:
            return 
        print('Current Values :-')
        print(f'1.Name : {choosen_customer.name}')
        print(f'2.login : {choosen_customer.login}')
        choice = int(input('Choose Value index to update : '))
        try:
            if choice == 1:
                new_value = input('New Value : ')
                choosen_customer.update_name(new_value)
                print('Updated Successfully')
            elif choice == 2:
                new_value = input('New Value : ')
                choosen_customer.update_login(new_value)
                print('Updated Successfully')
            else:
                print('Invalid Index')
        except Exception as e:
            print(e)
    def add_account(self):
        choosen_customer = self.get_choosen_customer()
        if not choosen_customer:
            return 
        type = input('Please Enter Account Type : ')
        balance = float(input('Please Enter Account Balance : '))
        try:
            self.sql.create_account(choosen_customer.id,type,balance)
            print('Account Created Successfully')
        except Exception as e:
            print(e)
    def change_loan_state(self):#perform operation on loans(Accept,reject,paid)
        loans = self.sql.get_loans(employee_id=self.id,branch_id=self.branch_id)
        if not self.view_loans_table(loans):
            return
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
            choosen_loan.set_employee_id(self.id)
        elif option == 2 and is_opened:
            choosen_loan.change_loan_state('rejected')
            choosen_loan.set_employee_id(self.id)
        elif option == 1 and not is_opened:
            choosen_loan.change_loan_state('paid')

            
        



