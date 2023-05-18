from . import user 
from Util import sql
class Admin(user.User):
    partition = ''
    hire_date = ''

    

    def __init__(self,name,login,password,type,partition,hire_date):
        super().__init__(name,login,password,type)
        self.partition = partition
        self.hire_date = hire_date
    
    def add_bank():
        bank_name = input("Enter The Bank Name Please: ")
        bank_city = input("Enter The Bank city Please: ")
        bank_zone = input("Enter The Bank Zone Please: ")
        bank_street = input("Enter The Bank Street Please: ")
        sql.add_bank(bank_name,bank_city,bank_zone,bank_street)
    
    def add_bank_branch():
        bank_code = input("Enter The Bank Code: ")
        branch_city = input("Enter The Brach City: ")
        branch_zone = input("Enter The Brach Zone: ")
        branch_street = input("Enter The Brach Street: ")
        sql.add_branch(branch_city,branch_zone,branch_street,bank_code)
    def view_all_loans():#will print all the available loans in the branch
        sql.view_all_loans()
    
    def view_loans():#Showing a list of loans with customer name and employee name
        sql.view_loans()

    def app(self):
        print("1-Add Bank.\n")
        print("2-Add Branch.\n")
        print("3-View All Available Loans.\n")
        print("4-View All Loans With Customer Name and Employee Name.\n")
        print("5-Exit.\n")
        print("\n")
        choice = input("Enter Your Choice Please: ")
        if choice == 1:
            self.add_bank()
        if choice == 2:
            self.add_branch()
        if choice == 3:
            self.view_all_loans()
        if choice == 4:
            self.view_loans()


