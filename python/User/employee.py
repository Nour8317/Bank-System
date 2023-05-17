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
