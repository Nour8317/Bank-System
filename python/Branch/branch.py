class Branch():
    city = ''
    zone = ''
    street = ''
    id = 0
    bank_name = ''
    bank_code = ''
    no_of_customers = 0
    no_of_employees = 0
    no_of_loans = 0
    no_of_account = 0
    def __init__(self,code,city,zone,street,id,bank_name,no_of_customers = 0,no_of_employees = 0,no_of_loans = 0,no_of_account = 0):
        self.id = id
        self.bank_code = code
        self.bank_name = bank_name
        self.city = city
        self.zone = zone
        self.street = street
        self.no_of_account = no_of_account
        self.no_of_employees = no_of_employees
        self.no_of_loans = no_of_loans
        self.no_of_customers = no_of_customers


