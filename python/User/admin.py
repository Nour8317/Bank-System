from . import user 
from Util import sql
from datetime import date
class Admin(user.User):
    partition = ''
    hire_date = ''

    def __init__(self,name,login,password,type,partition,hire_date,id):
        super().__init__(name,login,password,type,id)
        self.partition = partition
        self.hire_date = hire_date
    
    def add_bank(self):
        bank_name = input("Enter The Bank Name Please: ")
        bank_city = input("Enter The Bank city Please: ")
        bank_zone = input("Enter The Bank Zone Please: ")
        bank_street = input("Enter The Bank Street Please: ")
        try:
            sql.add_bank(bank_name,bank_city,bank_zone,bank_street)
            print('Bank Created Succeccfully')
        except Exception as e:
            print(f'An Error Occured : {e}')
    def add_branch(self):
        banks = sql.get_banks()
        i = 1
        print('Banks to choose from :-')
        for bank in banks:
            print(f'{i} . {bank.name}')
            i += 1
        bank_index = int(input("Bank Index : ")) - 1
        if bank_index >= len(banks) or len(banks) < 0:
            print('Invalid Index')
            return
        branch_city = input("Enter The Brach City: ")
        branch_zone = input("Enter The Brach Zone: ")
        branch_street = input("Enter The Brach Street: ")

        actual_bank = banks[bank_index - 1]
        try:
            branch = sql.add_branch(branch_city,branch_zone,branch_street,actual_bank.id,actual_bank.name)
            print('branch created succefully')
        except:
            print('Error occured !!')
    def view_all_loan_types(self):#will print all the available loans in the branch
        types = sql.get_all_loan_types()
        i = 1
        for type in types:
            print(f"{i}. Name  = {type.name} , ID = {type.id}")
            i += 1
    def view_loans(self):#Showing a list of loans with customer name and employee name
        loans = sql.get_loans()
        self.view_loans_table(loans)
    def add_employee(self):
        branches = sql.get_branches()
        i = 1
        print('Branches to choose from :-')
        for branch in branches:
            print(f'{i} . {branch.bank_name} - {branch.city} - {branch.street}')
            i += 1
        index = int(input("Branch Index : ")) - 1
        if index >= len(branches) or len(branches) < 0:
            print('Invalid Index')
            return
        name = input("Enter The Employee Name Please: ")
        hire_year = int(input("Enter The Employee Hire Year Please: "))
        hire_month = int(input("Enter The Employee Hire Month Please: "))
        hire_day = int(input("Enter The Employee Hire Day Please: "))
        hire_date = date(hire_year,hire_month,hire_day)
        position = input("Enter The Employee Position Please: ")
        login = input("Enter The Employee login Please: ")
        try:
            sql.create_employee(name,login,position,hire_date,branches[index].id)
        except Exception as e:
            print(f'Error : {e}')

    def print_menu(self):
        print("1-Add Bank.")
        print("2-Add Branch.")
        print("3-View All Available Loan Types.")
        print("4-View All Loans With Customer Name and Employee Name.")#TODO
        print("5-Add Employee.")
        print("6-Exit.")
    def app(self):
        choice = -1
        while choice != 6:
            self.print_menu()
            choice = int(input("Enter Your Choice Please: "))
            if choice == 1:
                self.add_bank()
            elif choice == 2:
                self.add_branch()
            elif choice == 3:
                self.view_all_loan_types()
            elif choice == 4:
                self.view_loans()
            elif choice == 5:
                self.add_employee()


