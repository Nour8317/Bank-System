from Util import sql
class Loan():
    loan_type_name = ''
    amount = 0
    branch_id = False
    id = 0
    customer_id = ''
    employee_id = False
    state = '' #[draft or opened or accepted or rejected or paid]
    def __init__(self, loan_type_name, amount, id, customer, employee, state,branch_id):
        self.loan_type_name = loan_type_name
        self.amount = amount
        self.id = id
        self.customer_id = customer
        self.employee_id = employee
        self.branch_id = branch_id
        self.state = state
    
    def get_branch_name(self):
        if not self.branch_id:
            return 'Not Assigned Yet'
        return sql.get_branch_name(self.branch_id)
    def get_employee_name(self):
        if not self.employee_id:
            return 'Not Assigned Yet'
        return sql.get_employee_name(self.employee_id)
    def get_customer_name(self):
        return sql.get_customer_name(self.customer_id)
    def change_loan_state(self,state):
        sql.change_loan_state(self.id,state)
    def set_employee_id(self,employee_id,branch_id):
        sql.set_employee_id(self.id,employee_id,branch_id)
