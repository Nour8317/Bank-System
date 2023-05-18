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

    def AddCustomer():
        print("the code of this method need to be written")

    def ViewAllCustomers():
        print("the code of this method need to be written")

    def ChangeLoanState():#perform operation on loans(Accept,reject)
        print("the code of this method need to be written")
