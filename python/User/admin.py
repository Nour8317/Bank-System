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