class Account():
    id = 0
    type = ''
    balance = 0
    customer_id = 0
    def __init__(self,id,type,balance,customer_id):
        self.id = id
        self.type = type
        self.balance = balance
        self.customer_id = customer_id