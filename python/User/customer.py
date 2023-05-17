from . import user 
class Customer(user.User):
    street = ''
    city = ''
    zone = ''
    ssn = ''
    def app(self):
        print('Customer')
    def __init__(self,name,login,password,type,ssn,street,city,zone):
        super().__init__(name,login,password,type)
        self.ssn = ssn
        self.street = street
        self.city = city
        self.zone = zone
