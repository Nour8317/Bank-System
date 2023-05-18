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
    
    def AddBank():
        print("the code of this method need to be written")
    
    def AddBankBranch():
        print("the code of this method need to be written")
    
    def ViewAllLoans():#will print all the available loans in the branch
        print("the code of this method need to be written")
    
    def ViewLoans():#Showing a list of loans with customer name and employee name
        print("the code of this method need to be written")


