class User():
    name = ''
    login = ''
    password = ''
    type = '' #'customer' or 'admin' or 'employee'
    def app(self):
        pass
    def __init__(self,name,login,password,type):
        self.name = name
        self.login = login
        self.password = password
        self.type = type