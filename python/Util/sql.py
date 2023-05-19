import pypyodbc
from User import employee,admin,customer
from Bank import bank
from Branch import branch
from Loan import loan,loan_type

server = '34.123.49.27'
database = 'BankSystem'
username = 'sqlserver'
password = '123456'
driver = '{ODBC Driver 17 for SQL Server}'
connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
connection = pypyodbc.connect(connection_string)
cursor = connection.cursor()
def get_banks():
    #TODO : remove demo data and query bank from DB
    return [
        bank.Bank('Bank 1','city 1','zone 1','street 1',1),
        bank.Bank('Bank 2','city 2','zone 2','street 2',2),
        bank.Bank('Bank 3','city 3','zone 3','street 3',3),
        bank.Bank('Bank 4','city 4','zone 4','street 4',4),
        bank.Bank('Bank 5','city 5','zone 5','street 5',5),
    ]
def get_branches():
    #TODO : remove demo data and query bank from DB
    return [
        branch.Branch(1,'city 1','zone 1','maadi',1,'Alahly'),
        branch.Branch(1,'city 1','zone 1','kk 1',1,'Alahly'),
        branch.Branch(1,'city 1','zone 1','sasac 1',1,'Alahly'),
        branch.Branch(1,'city 1','zone 1','sss 1',1,'Alahly'),
    ]
def get_branch_name(branch_id):
    return 'Test Branch'
def get_customer_name(customer_id):
    return 'Test Customer'
def get_employee_name(employee_id):
    return 'Test Employee'
def get_loans(customer_id = False,employee_id = False):
    #if customer id passed query loans of this customer only 
    #if employee id passed query loans of this employee or loans of the employee's branch that are draft or opened
    #if both are false return all loans
    return [
        loan.Loan('Loan Type 1',100,1,1,1,'Accepted',1),
        loan.Loan('Loan Type 2',200,1,1,1,'Rejected',1),
        loan.Loan('Loan Type 3',300,1,1,False,'opened',False),
        loan.Loan('Loan Type 4',400,1,1,False,'draft',False)
    ]
def get_all_loan_types(branch_id = False):
    #if branch id passed get loan types of this branch id
    return [loan_type.LoanType('loan 1',1,2),loan_type.LoanType('loan 2',2,2),]
def add_bank(bank_name,bank_city,bank_zone,bank_street):
    #TODO : query to create bank
    return bank.Bank(bank_name,bank_city,bank_zone,bank_street,6)
def add_branch(branch_city,branch_zone,branch_street,bank_code,bank_name):
    #TODO : query to create branch
    return branch.Branch(bank_code,branch_city,branch_zone,branch_street,6,bank_name)
def create_employee(name,login,pos,hire_date,branch_id):
    return employee.Employee(name,login,False,'employee',pos,hire_date,4,branch_id)
def create_customer(name,login,city,street,zone,ssn,branch_id):
    return customer.Customer(name,login,False,'customer',ssn,street,city,zone,7,branch_id)
def change_loan_state(loan_id,state):
    pass
def set_employee_id(loan_id,employee_id,branch_id):
    pass
def get_customers(branch_id):
    demo_id = 6
    demo_name = 'name'
    demo_hire_date = 'hire date'
    demo_dept = 'dept'
    demo_partition = 'partition'
    demo_ssn = '12345678999999999'
    demo_city = 'city'
    demo_zone = 'zone'
    demo_street = 'street'
    demo_customer = customer.Customer(demo_name,login,password,'customer',demo_ssn,demo_street,demo_city,demo_zone,demo_id,1)
    return [
        demo_customer,demo_customer,demo_customer,demo_customer,demo_customer
    ]
def create_loan(type_id,type_name,amount,customer_id):
    return loan.Loan(type_name,amount,5,customer_id,False,'draft',False)
def login(login,password):#returns Admin or Employee or Customer or False[if failed]
    #if password column value is null
    #so password passed put in database and return the user
    #if user is admin dont aplly this rule admin must have password
    demo_id = 6
    demo_name = 'name'
    demo_hire_date = 'hire date'
    demo_dept = 'dept'
    demo_partition = 'partition'
    demo_ssn = '12345678999999999'
    demo_city = 'city'
    demo_zone = 'zone'
    demo_street = 'street'
    demo_customer = customer.Customer(demo_name,login,password,'customer',demo_ssn,demo_street,demo_city,demo_zone,demo_id,1)
    demo_employee = employee.Employee(demo_name,login,password,'employee',demo_dept,demo_hire_date,demo_id,2)
    demo_admin = admin.Admin(demo_name,login,password,'admin',demo_partition,demo_hire_date,demo_id)
    return demo_employee
connection.commit()
cursor.close()
connection.close()