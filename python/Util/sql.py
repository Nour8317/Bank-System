import pypyodbc
from User import employee,admin,customer
driver = '{ODBC Driver 17 for SQL Server}'
server = 'Hatem'
db = 'AdventureWorks2019'
connection_string = f"""
    DRIVER={driver};
    SERVER={server};
    DATABASE={db};
    trusted_connection=yes;
"""
print(connection_string)
connection = pypyodbc.connect(connection_string)
cursor = connection.cursor()
# print(cursor.execute('SELECT name FROM Sales.Store;').fetchall())
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
cursor.close()
connection.close()