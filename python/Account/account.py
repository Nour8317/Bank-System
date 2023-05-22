class Account():
    id = 0
    type = ''
    balance = 0
    customer_id = 0
    customer_name = ''
    branch_name = ''

    def __init__(self,id,type,balance,customer_id,customer_name = '',branch_name = ''):
        self.id = id
        self.type = type
        self.balance = balance
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.branch_name = branch_name