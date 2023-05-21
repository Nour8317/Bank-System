import pypyodbc
from User import employee, admin, customer
from Bank import bank
from Branch import branch
from Loan import loan, loan_type
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
    return cursor, connection


def create_account(customer_id, type, balance):
    cursor, connection = create_connection()
    sql = """
        INSERT INTO "Accounts" (AccountType,Balance,CustomerID)
        VALUES (?,?,?);
    """
    vals = (type, balance, customer_id)
    cursor.execute(sql, vals)
    connection.commit()
    cursor.close()
    connection.close()
    return account.Account(1, type, balance, customer_id)


def update_customer_name(customer_id, new_value):
    cursor, connection = create_connection()
    sql = """
        UPDATE [User] SET Name = ? WHERE UserID = ?;
    """
    vals = (new_value, customer_id)
    cursor.execute(sql, vals)
    connection.commit()
    cursor.close()
    connection.close()


def update_customer_login(customer_id, new_value):
    cursor, connection = create_connection()
    sql = """
        UPDATE [User] SET Email = ? WHERE UserID = ?;
    """
    vals = (new_value, customer_id)
    cursor.execute(sql, vals)
    connection.commit()
    cursor.close()
    connection.close()


def get_branch_name(branch_id):
    cursor, connection = create_connection()
    sql = """
        SELECT bn.Name,br.City,br.Zone,br.Street,br.BranchID,bn.BankID FROM 
        Bank as bn,
        Branch as br
        WHERE br.Bank_Code = bn.BankID and br.BranchID = ?;
    """
    vals = (branch_id,)
    cursor.execute(sql, vals)
    rows = cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()
    return f'{rows[0]} - {rows[1]} - {rows[2]}'


def get_customer_name(customer_id):
    cursor, connection = create_connection()
    sql = """
        SELECT Name FROM [User] WHERE UserID = ?;
    """
    vals = (customer_id,)
    cursor.execute(sql, vals)
    rows = cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()
    return rows[0]


def get_employee_name(employee_id):
    return get_customer_name(employee_id)


def get_accounts(customer_id):
    cursor, connection = create_connection()
    sql = """
        SELECT AccountID, AccountType, Balance, CustomerID FROM Accounts WHERE CustomerID = ?;
    """
    vals = (customer_id,)  # Make sure to provide the parameter value as a tuple
    cursor.execute(sql, vals)
    rows = cursor.fetchall()
    accounts = []
    for row in rows:
        accounts.append(account.Account(row[0], row[1], row[2], row[3]))
    connection.commit()
    cursor.close()
    connection.close()
    return accounts


def get_loans(customer_id=False,state = False ,employee_id=False, branch_id=False):
    # if customer id passed query loans of this customer only
    # if employee id passed query loans of this employee or loans of the employee's branch that are draft or opened
    # if both are false return all loans
    cursor, connection = create_connection()

    if not customer_id and not employee_id:
        sql = """
            SELECT lt.Loan_Type,l.Amount,l.Loan_ID,c.Name,e.Name,l.Loan_State,b.computed_name 
            FROM Loan_Type as lt,Loan as l,[User] as c,[User] as e,Branch as b 
            WHERE lt.loan_TypeID = l.Loan_Type_ID and e.UserID = l.Employee_ID and c.UserID = l.Customer_ID and  l.Branch_ID = b.BranchID;
        """
        cursor.execute(sql)
    elif customer_id:
        sql = """
            SELECT lt.Loan_Type,l.Amount,l.Loan_ID,c.Name,e.Name,l.Loan_State,b.computed_name 
            FROM Loan_Type as lt,Loan as l,[User] as c,[User] as e,Branch as b
            WHERE lt.loan_TypeID = l.Loan_Type_ID and l.Customer_ID = ? and e.UserID = l.Employee_ID and c.UserID = l.Customer_ID and  l.Branch_ID = b.BranchID
        """
        if state:
            sql += f"and Loan_State = '{state}'"
        else:
            sql += ';'
        cursor.execute(sql, (customer_id,))
    else:
        sql = """
            SELECT lt.Loan_Type,l.Amount,l.Loan_ID,c.Name,e.Name,l.Loan_State,b.computed_name 
            FROM Loan_Type as lt,Loan as l,[User] as c,[User] as e,Branch as b
            WHERE lt.loan_TypeID = l.Loan_Type_ID  and e.UserID = l.Employee_ID and c.UserID = l.Customer_ID and l.Branch_ID = b.BranchID
            AND ((l.Employee_ID = ? and l.Loan_State = 'accepted') OR (l.Loan_State = 'opened' AND l.Branch_ID = ?));
        """
        cursor.execute(sql, (employee_id, branch_id))
    rows = cursor.fetchall()
    loans = []
    for row in rows:
        loans.append(loan.Loan(row[0], row[1], row[2],
                     row[3], row[4], row[5], row[6]))
    connection.commit()
    cursor.close()
    connection.close()
    return loans


def get_all_loan_types(branch_id=False):
    cursor, connection = create_connection()
    if not branch_id:
        sql = """
            SELECT loan_Type,loan_TypeID FROM Loan_Type;
        """
        cursor.execute(sql)
    else:
        sql = """
            SELECT  lt.Loan_Type,c.LoanTypeID
            FROM Contain AS c, Loan_Type AS lt
            WHERE BranchID = ?
            AND c.LoanTypeID = lt.Loan_TypeID;
        """
        cursor.execute(sql, (branch_id,))

    rows = cursor.fetchall()
    loan_types = []
    for row in rows:
        loan_types.append(loan_type.LoanType(row[0], row[1]))
    connection.commit()
    cursor.close()
    connection.close()
    return loan_types


def add_branch(branch_city, branch_zone, branch_street, bank_code, bank_name):
    cursor, connection = create_connection()
    sql = """
        INSERT INTO "Branch" (City,Street,Zone,Bank_Code)
        VALUES (?,?,?,?);
    """
    vals = (branch_city, branch_street, branch_zone, bank_code)
    cursor.execute(sql, vals)
    connection.commit()
    cursor.close()
    connection.close()
    return branch.Branch(bank_code, branch_city, branch_zone, branch_street, 6, bank_name)


def add_bank(bank_name, bank_city, bank_zone, bank_street):
    cursor, connection = create_connection()
    sql = """
        INSERT INTO "Bank" (Name,Street,City,Zone)
        VALUES (?,?,?,?);
    """
    vals = (bank_name, bank_street, bank_city, bank_zone)
    cursor.execute(sql, vals)
    connection.commit()
    cursor.close()
    connection.close()
    return bank.Bank(bank_name, bank_city, bank_zone, bank_street, 6)


def get_banks():
    cursor, connection = create_connection()
    sql = """
        SELECT Name,City,Zone,Street,BankID FROM Bank;
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    banks = []
    for row in rows:
        banks.append(bank.Bank(row[0], row[1], row[2], row[3], row[4]))
    connection.commit()
    cursor.close()
    connection.close()
    return banks


def get_branches():
    cursor, connection = create_connection()
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
        branches.append(branch.Branch(
            row[5], row[0], row[1], row[2], row[3], row[4]))
    connection.commit()
    cursor.close()
    connection.close()
    return branches


def create_user(cursor, name, login, type):
    create_user_sql = """
        INSERT INTO "User" (Name, Email, UserType)
        OUTPUT inserted.UserID
        VALUES (?,?,?);
    """
    user_values = (name, login, type)
    cursor.execute(create_user_sql, user_values)
    return cursor.fetchone()[0]


def create_employee(name, login, pos, hire_date, branch_id):
    cursor, connection = create_connection()
    user_id = create_user(cursor, name, login, 'employee')
    customer_sql = """
    INSERT INTO "Employee" (Position, HireDate , Branch_Number, EmployeeID) 
    VALUES (?,?,?,?);
    """
    customer_values = (pos, hire_date, branch_id, user_id)
    cursor.execute(customer_sql, customer_values)
    connection.commit()
    cursor.close()
    connection.close()
    return employee.Employee(name, login, False, 'employee', pos, hire_date, 4, branch_id)


def create_customer(name, login, city, street, zone, ssn, branch_id):
    cursor, connection = create_connection()
    user_id = user_id = create_user(cursor, name, login, 'customer')

    customer_sql = """
    INSERT INTO "Customer" (SSN, Street, City, Zone, CustomerID,BranchID) 
    VALUES (?,?,?,?,?,?);
    """
    customer_values = (ssn, street, city, zone, user_id, branch_id)
    cursor.execute(customer_sql, customer_values)
    connection.commit()
    cursor.close()
    connection.close()
    return customer.Customer(name, login, False, 'customer', ssn, street, city, zone, 7, branch_id)


def change_loan_state(loan_id, state):
    cursor, connection = create_connection()

    sql = """
        UPDATE Loan SET Loan_State = ? WHERE Loan_ID = ?;
    """
    values = (state, loan_id)
    cursor.execute(sql, values)
    connection.commit()
    cursor.close()
    connection.close()


def set_employee_id(loan_id, employee_id):
    cursor, connection = create_connection()

    sql = """
        UPDATE Loan SET Employee_ID = ? WHERE Loan_ID = ?;
    """
    values = (employee_id, loan_id)
    cursor.execute(sql, values)
    connection.commit()
    cursor.close()
    connection.close()


def get_customers(branch_id=False,user_id = False):
    cursor, connection = create_connection()
    sql = """
        SELECT u.Name,u.Email,u.Password,u.UserType,c.SSN,c.street,c.city,c.zone,c.CustomerID,c.BranchID FROM 
        Customer as c,
        [User] as u
        WHERE c.CustomerID = u.UserID
    """
    if user_id:
        sql += f" AND c.CustomerID = {user_id};"
    else:
        sql += ';'
    cursor.execute(sql)
    rows = cursor.fetchall()
    customers = []
    for row in rows:
        if branch_id and branch_id != row[9]:
            continue
        customers.append(customer.Customer(
            row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],))
    connection.commit()
    cursor.close()
    connection.close()
    return customers


def get_employees(user_id = False):
    cursor, connection = create_connection()
    sql = """
        SELECT u.Name,u.Email,u.Password,u.UserType,e.Position,e.HireDate,e.EmployeeID,e.Branch_Number FROM 
        Employee as e,
        [User] as u
        WHERE e.EmployeeID = u.UserID
    """
    if user_id:
        sql += f" AND e.EmployeeID = {user_id};"
    else:
        sql += ';'
    cursor.execute(sql)
    rows = cursor.fetchall()
    employees = []
    for row in rows:
        employees.append(employee.Employee(
            row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],))
    connection.commit()
    cursor.close()
    connection.close()
    return employees


def create_loan(type_id, type_name, amount, customer_id,branch_id):
    cursor, connection = create_connection()
    sql = """
        INSERT INTO "Loan" (Loan_Type_ID, Loan_State, Customer_ID, Amount,Branch_ID) 
        VALUES (?,?,?,?,?);
    """
    vals = (type_id, 'draft', customer_id, amount,branch_id)
    cursor.execute(sql, vals)
    connection.commit()
    cursor.close()
    connection.close()
    return loan.Loan(type_name, amount, 5, customer_id, False, 'draft', False)


# returns Admin or Employee or Customer or False[if failed]
def get_user_for_login(login,password):
    cursor, connection = create_connection()
    sql = """
        SELECT UserType,Name,UserID,Password FROM [User] WHERE Email = ? and (Password = ? or Password IS NULL);
    """
    vals = (login,password)
    cursor.execute(sql, vals)
    row = cursor.fetchone()
    if not row:
        return False
    if not row[3]:
        sql = """
            UPDATE [User] Set Password = ? WHERE UserID = ?;
        """
        vals = (password,row[2])
        cursor.execute(sql, vals)
    connection.commit()
    cursor.close()
    connection.close()
    return (row[0],row[1],row[2])
def login(login, password):
    # if password column value is null
    # so password passed put in database and return the user
    # if user is admin dont aplly this rule admin must have password
    user = get_user_for_login(login,password)
    if not user:
        return False
    type,name,user_id = user
    if type == 'admin':
        return admin.Admin(name, login, password,'admin',user_id)
    if type == 'customer':
        return get_customers(user_id = user_id)[0]
    if type == 'employee':
        return get_employees(user_id = user_id)[0]
