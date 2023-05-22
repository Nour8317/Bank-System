class Branch():
    city = ''
    zone = ''
    street = ''
    id = 0
    bank_name = ''
    bank_code = ''
    def __init__(self,code,city,zone,street,id,bank_name):
        self.id = id
        self.bank_code = code
        self.bank_name = bank_name
        self.city = city
        self.zone = zone
        self.street = street


