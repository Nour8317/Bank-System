import pypyodbc
from User import employee,admin,customer
from Bank import bank
from Branch import branch
from Loan import loan,loan_type
from Account import account
server = '34.123.49.27'
database = 'BankSystem'
username = 'sqlserver'
password = '123456'
driver = '{ODBC Driver 17 for SQL Server}'
connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
def create_connection():
    connection = pypyodbc.connect(connection_string)
    cursor = connection.cursor()
    return cursor,connection

def create_account(customer_id,type,balance):
    cursor,connection = create_connection()
    sql = """
        INSERT INTO "Accounts" (AccountType,Balance,CustomerID)
        VALUES (?,?,?);
    """
    vals = (type,balance,customer_id)
    cursor.execute(sql, vals)
    connection.commit()
    cursor.close()
    connection.close()
    return account.Account(1,type,balance,customer_id)
def update_customer_name(customer_id,new_value):
    cursor,connection = create_connection()
    sql = """
        UPDATE [User] SET Name = ? WHERE UserID = ?;
    """
    vals = (new_value, customer_id)
    cursor.execute(sql, vals)
    connection.commit()
    cursor.close()
    connection.close()
def update_customer_login(customer_id,new_value):
    cursor,connection = create_connection()
    sql = """
        UPDATE [User] SET Email = ? WHERE UserID = ?;
    """
    vals = (new_value, customer_id)
    cursor.execute(sql, vals)
    connection.commit()
    cursor.close()
    connection.close()
def get_branch_name(branch_id):
    cursor,connection = create_connection()
    sql = """
        SELECT Name FROM Branch WHERE BranchID = ?;
    """
    vals = (branch_id)
    cursor.execute(sql, vals)
    rows = cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()
    return rows[0]
def get_customer_name(customer_id):
    cursor,connection = create_connection()
    sql = """
        SELECT Name FROM User WHERE UserID = ?;
    """
    vals = (customer_id)
    cursor.execute(sql, vals)
    rows = cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()
    return rows[0]
def get_employee_name(employee_id):
    get_customer_name(employee_id)
def get_accounts(customer_id):
    cursor,connection = create_connection()
    sql = """
        SELECT AccountID, AccountType, Balance, CustomerID FROM Accounts WHERE CustomerID = ?;
    """
    vals = (customer_id,)  # Make sure to provide the parameter value as a tuple
    cursor.execute(sql, vals)
    rows = cursor.fetchall()
    accounts = []
    for row in rows:
        accounts.append(account.Account(row[0],row[1],row[2],row[3]))
    connection.commit()
    cursor.close()
    connection.close()
    return accounts
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
    cursor,connection = create_connection()
    if not branch_id:
        sql = """
            SELECT loan_Type,loan_TypeID FROM Loan_Type;
        """
        cursor.execute(sql)
        rows = cursor.fetchall()
    loan_types = []
    for row in rows:
        loan_types.append(loan_type.LoanType(row[0],row[1]))
    connection.commit()
    cursor.close()
    connection.close()
    return loan_types

def add_branch(branch_city,branch_zone,branch_street,bank_code,bank_name):
    cursor,connection = create_connection()
    sql = """
        INSERT INTO "Branch" (City,Street,Zone,Bank_Code)
        VALUES (?,?,?,?);
    """
    vals = (branch_city, branch_street, branch_zone,bank_code)
    cursor.execute(sql, vals)
    connection.commit()
    cursor.close()
    connection.close()
    return branch.Branch(bank_code,branch_city,branch_zone,branch_street,6,bank_name)
def add_bank(bank_name,bank_city,bank_zone,bank_street):
    cursor,connection = create_connection()
    sql = """
        INSERT INTO "Bank" (Name,Street,City,Zone)
        VALUES (?,?,?,?);
    """
    vals = (bank_name, bank_street, bank_city,bank_zone)
    cursor.execute(sql, vals)
    connection.commit()
    cursor.close()
    connection.close()
    return bank.Bank(bank_name,bank_city,bank_zone,bank_street,6)
def get_banks():
    cursor,connection = create_connection()
    sql = """
        SELECT Name,City,Zone,Street,BankID FROM Bank;
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    banks = []
    for row in rows:
        banks.append(bank.Bank(row[0],row[1],row[2],row[3],row[4]))
    connection.commit()
    cursor.close()
    connection.close()
    return banks
def get_branches():
    cursor,connection = create_connection()
    sql = """
        SELECT br.City,br.Zone,br.Street,br.BranchID,bn.Name,bn.BankID FROM 
        Bank as bn,
        Branch as br
        WHERE br.Bank_Code = bn.BankID;
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    branches = []
    for row in rows:
        branches.append(branch.Branch(row[5],row[0],row[1],row[2],row[3],row[4]))
    connection.commit()
    cursor.close()
    connection.close()
    return branches
def create_user(cursor,name,login,type):
    create_user_sql = """
        INSERT INTO "User" (Name, Email, UserType)
        OUTPUT inserted.UserID
        VALUES (?,?,?);
    """
    user_values = (name, login, type)
    cursor.execute(create_user_sql, user_values)
    return cursor.fetchone()[0]
def create_employee(name,login,pos,hire_date,branch_id):
    cursor,connection = create_connection()
    user_id = create_user(cursor,name,login,'employee')
    customer_sql = """
    INSERT INTO "Employee" (Position, HireDate , Branch_Number, EmployeeID) 
    VALUES (?,?,?,?);
    """
    customer_values = (pos,hire_date,branch_id,user_id)
    cursor.execute(customer_sql, customer_values)
    connection.commit()
    cursor.close()
    connection.close()
    return employee.Employee(name,login,False,'employee',pos,hire_date,4,branch_id)
def create_customer(name,login,city,street,zone,ssn,branch_id):
    cursor,connection = create_connection()
    user_id = user_id = create_user(cursor,name,login,'customer')

    customer_sql = """
    INSERT INTO "Customer" (SSN, Street, City, Zone, CustomerID,BranchID) 
    VALUES (?,?,?,?,?,?);
    """
    customer_values = (ssn,street,city,zone,user_id,branch_id)
    cursor.execute(customer_sql, customer_values)
    connection.commit()
    cursor.close()
    connection.close()
    return customer.Customer(name,login,False,'customer',ssn,street,city,zone,7,branch_id)
def change_loan_state(loan_id,state):
    pass
def set_employee_id(loan_id,employee_id,branch_id):
    pass
def get_customers(branch_id = False):
    cursor,connection = create_connection()
    sql = """
        SELECT u.Name,u.Email,u.Password,u.UserType,c.SSN,c.street,c.city,c.zone,c.CustomerID,c.BranchID FROM 
        Customer as c,
        [User] as u
        WHERE c.CustomerID = u.UserID;
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    customers = []
    for row in rows:
        if branch_id and branch_id != row[9]:
            continue
        customers.append(customer.Customer(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],))
    connection.commit()
    cursor.close()
    connection.close()
    return customers
def get_employees():
    cursor,connection = create_connection()
    sql = """
        SELECT u.Name,u.Email,u.Password,u.UserType,e.Position,e.HireDate,e.EmployeeID,e.Branch_Number FROM 
        Employee as e,
        [User] as u
        WHERE e.EmployeeID = u.UserID;
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    employees = []
    for row in rows:
        employees.append(employee.Employee(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],))
    connection.commit()
    cursor.close()
    connection.close()
    return employees
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
    demo_customer = get_customers()[0]
    demo_employee = get_employees()[0]
    demo_admin = admin.Admin(demo_name,login,password,'admin',demo_partition,demo_hire_date,demo_id)
    return demo_customer
