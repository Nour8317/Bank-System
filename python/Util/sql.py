import pypyodbc
from User import employee,admin,customer
server = '34.123.49.27'
database = 'BankSystem'
username = 'sqlserver'
password = '123456'
driver = '{ODBC Driver 17 for SQL Server}'
connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
connection = pypyodbc.connect(connection_string)
cursor = connection.cursor()
def login(login,password):#returns Admin or Employee or Customer or False[if failed]
    demo_name = 'name'
    demo_hire_date = 'hire date'
    demo_dept = 'dept'
    demo_partition = 'partition'
    demo_ssn = 'ssn'
    demo_city = 'city'
    demo_zone = 'zone'
    demo_street = 'street'
    demo_customer = customer.Customer(demo_name,login,password,'customer',demo_ssn,demo_street,demo_city,demo_zone)
    demo_employee = employee.Employee(demo_name,login,password,'employee',demo_dept,demo_hire_date)
    demo_admin = admin.Admin(demo_name,login,password,'admin',demo_partition,demo_hire_date)
    return demo_admin
connection.commit()
cursor.close()
connection.close()