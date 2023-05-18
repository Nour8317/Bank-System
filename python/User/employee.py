from . import user 
class Employee(user.User):
    dept = ''
    hire_date = ''

    def app(self):
        print('employee')

    def __init__(self,name,login,password,type,dept,hire_date):
        super().__init__(name,login,password,type)
        self.hire_date = hire_date
        self.dept = dept

    def add_customer():
        print("the code of this method need to be written")

    def view_all_customers():
        print("the code of this method need to be written")

    def change_loan_state():#perform operation on loans(Accept,reject)
        print("the code of this method need to be written")
