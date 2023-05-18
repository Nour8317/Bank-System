from . import user 
class Admin(user.User):
    partition = ''
    hire_date = ''

    def app(self):
        print('admin')

    def __init__(self,name,login,password,type,partition,hire_date):
        super().__init__(name,login,password,type)
        self.partition = partition
        self.hire_date = hire_date
    
    def add_bank():
        print("the code of this method need to be written")
    
    def add_bank_branch():
        print("the code of this method need to be written")
    
    def view_all_loans():#will print all the available loans in the branch
        print("the code of this method need to be written")
    
    def view_loans():#Showing a list of loans with customer name and employee name
        print("the code of this method need to be written")


