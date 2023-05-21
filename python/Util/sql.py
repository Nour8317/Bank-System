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
    
class SQL():
    connection = ''
    cursor = ''
    def __init__(self):
        self.connection = pypyodbc.connect(connection_string)
        self.cursor = self.connection.cursor()
    def __del__(self):
        print('dest')
        self.connection.commit()
        self.cursor.close()
        self.connection.close()


    def create_account(self,customer_id, type, balance):
        sql = """
            INSERT INTO "Accounts" (AccountType,Balance,CustomerID)
            VALUES (?,?,?);
        """
        vals = (type, balance, customer_id)
        self.cursor.execute(sql, vals)

        return account.Account(1, type, balance, customer_id)


    def update_customer_name(self,customer_id, new_value):
        sql = """
            UPDATE [User] SET Name = ? WHERE UserID = ?;
        """
        vals = (new_value, customer_id)
        self.cursor.execute(sql, vals)



    def update_customer_login(self,customer_id, new_value):
        sql = """
            UPDATE [User] SET Email = ? WHERE UserID = ?;
        """
        vals = (new_value, customer_id)
        self.cursor.execute(sql, vals)



    def get_branch_name(self,branch_id):
        sql = """
            SELECT bn.Name,br.City,br.Zone,br.Street,br.BranchID,bn.BankID FROM 
            Bank as bn,
            Branch as br
            WHERE br.Bank_Code = bn.BankID and br.BranchID = ?;
        """
        vals = (branch_id,)
        self.cursor.execute(sql, vals)
        rows = self.cursor.fetchone()

        return f'{rows[0]} - {rows[1]} - {rows[2]}'


    def get_customer_name(self,customer_id):
        sql = """
            SELECT Name FROM [User] WHERE UserID = ?;
        """
        vals = (customer_id,)
        self.cursor.execute(sql, vals)
        rows = self.cursor.fetchone()

        return rows[0]


    def get_employee_name(self,employee_id):
        return self.get_customer_name(employee_id)


    def get_accounts(self,customer_id):
        sql = """
            SELECT AccountID, AccountType, Balance, CustomerID FROM Accounts WHERE CustomerID = ?;
        """
        vals = (customer_id,)  # Make sure to provide the parameter value as a tuple
        self.cursor.execute(sql, vals)
        rows = self.cursor.fetchall()
        accounts = []
        for row in rows:
            accounts.append(account.Account(row[0], row[1], row[2], row[3]))

        return accounts


    def get_loans(self,customer_id=False,state = False ,employee_id=False, branch_id=False):
        # if customer id passed query loans of this customer only
        # if employee id passed query loans of this employee or loans of the employee's branch that are draft or opened
        # if both are false return all loans

        if not customer_id and not employee_id:
            sql = """
                SELECT lt.Loan_Type,l.Amount,l.Loan_ID,c.Name,e.Name,l.Loan_State,b.computed_name 
                FROM Loan_Type as lt,Loan as l,[User] as c,[User] as e,Branch as b 
                WHERE lt.loan_TypeID = l.Loan_Type_ID and e.UserID = l.Employee_ID and c.UserID = l.Customer_ID and  l.Branch_ID = b.BranchID;
            """
            self.cursor.execute(sql)
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
            self.cursor.execute(sql, (customer_id,))
        else:
            sql = """
                SELECT lt.Loan_Type,l.Amount,l.Loan_ID,c.Name,e.Name,l.Loan_State,b.computed_name 
                FROM Loan_Type as lt,Loan as l,[User] as c,[User] as e,Branch as b
                WHERE lt.loan_TypeID = l.Loan_Type_ID  and e.UserID = l.Employee_ID and c.UserID = l.Customer_ID and l.Branch_ID = b.BranchID
                AND ((l.Employee_ID = ? and l.Loan_State = 'accepted') OR (l.Loan_State = 'opened' AND l.Branch_ID = ?));
            """
            self.cursor.execute(sql, (employee_id, branch_id))
        rows = self.cursor.fetchall()
        loans = []
        for row in rows:
            loans.append(loan.Loan(row[0], row[1], row[2],
                        row[3], row[4], row[5], row[6]))

        return loans


    def get_all_loan_types(self,branch_id=False):
        if not branch_id:
            sql = """
                SELECT loan_Type,loan_TypeID FROM Loan_Type;
            """
            self.cursor.execute(sql)
        else:
            sql = """
                SELECT  lt.Loan_Type,c.LoanTypeID
                FROM Contain AS c, Loan_Type AS lt
                WHERE BranchID = ?
                AND c.LoanTypeID = lt.Loan_TypeID;
            """
            self.cursor.execute(sql, (branch_id,))

        rows = self.cursor.fetchall()
        loan_types = []
        for row in rows:
            loan_types.append(loan_type.LoanType(row[0], row[1]))

        return loan_types


    def add_branch(self,branch_city, branch_zone, branch_street, bank_code, bank_name):
        sql = """
            INSERT INTO "Branch" (City,Street,Zone,Bank_Code)
            VALUES (?,?,?,?);
        """
        vals = (branch_city, branch_street, branch_zone, bank_code)
        self.cursor.execute(sql, vals)
        return branch.Branch(bank_code, branch_city, branch_zone, branch_street, 6, bank_name)

    def add_bank(self,bank_name, bank_city, bank_zone, bank_street):
        sql = """
            INSERT INTO "Bank" (Name,Street,City,Zone)
            VALUES (?,?,?,?);
        """
        vals = (bank_name, bank_street, bank_city, bank_zone)
        self.cursor.execute(sql, vals)

        return bank.Bank(bank_name, bank_city, bank_zone, bank_street, 6)


    def get_banks(self):
        sql = """
            SELECT Name,City,Zone,Street,BankID FROM Bank;
        """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        banks = []
        for row in rows:
            banks.append(bank.Bank(row[0], row[1], row[2], row[3], row[4]))

        return banks


    def get_branches(self):
        sql = """
            SELECT br.City,br.Zone,br.Street,br.BranchID,bn.Name,bn.BankID FROM 
            Bank as bn,
            Branch as br
            WHERE br.Bank_Code = bn.BankID;
        """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        branches = []
        for row in rows:
            branches.append(branch.Branch(
                row[5], row[0], row[1], row[2], row[3], row[4]))

        return branches


    def create_user(self, name, login, type):
        create_user_sql = """
            INSERT INTO "User" (Name, Email, UserType)
            OUTPUT inserted.UserID
            VALUES (?,?,?);
        """
        user_values = (name, login, type)
        self.cursor.execute(create_user_sql, user_values)
        return self.cursor.fetchone()[0]


    def create_employee(self,name, login, pos, hire_date, branch_id):
        user_id = self.create_user(name, login, 'employee')
        customer_sql = """
        INSERT INTO "Employee" (Position, HireDate , Branch_Number, EmployeeID) 
        VALUES (?,?,?,?);
        """
        customer_values = (pos, hire_date, branch_id, user_id)
        self.cursor.execute(customer_sql, customer_values)

        return employee.Employee(self,name, login, False, 'employee', pos, hire_date, 4, branch_id)


    def create_customer(self,name, login, city, street, zone, ssn, branch_id):
        user_id = user_id = self.create_user(name, login, 'customer')

        customer_sql = """
        INSERT INTO "Customer" (SSN, Street, City, Zone, CustomerID,BranchID) 
        VALUES (?,?,?,?,?,?);
        """
        customer_values = (ssn, street, city, zone, user_id, branch_id)
        self.cursor.execute(customer_sql, customer_values)

        return customer.Customer(self,name, login, False, 'customer', ssn, street, city, zone, 7, branch_id)


    def change_loan_state(self,loan_id, state):

        sql = """
            UPDATE Loan SET Loan_State = ? WHERE Loan_ID = ?;
        """
        values = (state, loan_id)
        self.cursor.execute(sql, values)



    def set_employee_id(self,loan_id, employee_id):

        sql = """
            UPDATE Loan SET Employee_ID = ? WHERE Loan_ID = ?;
        """
        values = (employee_id, loan_id)
        self.cursor.execute(sql, values)



    def get_customers(self,branch_id=False,user_id = False):
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
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        customers = []
        for row in rows:
            if branch_id and branch_id != row[9]:
                continue
            customers.append(customer.Customer(self,
                row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],))

        return customers


    def get_employees(self,user_id = False):
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
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        employees = []
        for row in rows:
            employees.append(employee.Employee(self,
                row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],))

        return employees


    def create_loan(self,type_id, type_name, amount, customer_id,branch_id):
        sql = """
            INSERT INTO "Loan" (Loan_Type_ID, Loan_State, Customer_ID, Amount,Branch_ID) 
            VALUES (?,?,?,?,?);
        """
        vals = (type_id, 'draft', customer_id, amount,branch_id)
        self.cursor.execute(sql, vals)

        return loan.Loan(type_name, amount, 5, customer_id, False, 'draft', False)


    # returns Admin or Employee or Customer or False[if failed]
    def get_user_for_login(self,login,password):
        sql = """
            SELECT UserType,Name,UserID,Password FROM [User] WHERE Email = ? and (Password = ? or Password IS NULL);
        """
        vals = (login,password)
        self.cursor.execute(sql, vals)
        row = self.cursor.fetchone()
        if not row:
            return False
        if not row[3]:
            sql = """
                UPDATE [User] Set Password = ? WHERE UserID = ?;
            """
            vals = (password,row[2])
            self.cursor.execute(sql, vals)

        return (row[0],row[1],row[2])
    def login(self,login, password):
        # if password column value is null
        # so password passed put in database and return the user
        # if user is admin dont aplly this rule admin must have password
        user = self.get_user_for_login(login,password)
        if not user:
            return False
        type,name,user_id = user
        if type == 'admin':
            return admin.Admin(self,name, login, password,'admin',user_id)
        if type == 'customer':
            return self.get_customers(user_id = user_id)[0]
        if type == 'employee':
            return self.get_employees(user_id = user_id)[0]
