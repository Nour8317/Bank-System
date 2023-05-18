from User.employee import Employee
from User.user import User
from Util import sql

def AdminSystem():#will contain the Admin interface
    print("the code of this method need to be written")

def CustomerSystem():#will contain the Customer interface
    print("the code of this method need to be written") 

def EmployeeSystem():#will contain the Employee interface
    print("the code of this method need to be written")

def Register():
    print("the code of this method need to be written")

def Login():
    print("the code of this method need to be written")

def main():
    login = input('login : ')
    password = input('password : ')
    current_user = sql.login(login,password)
    current_user.app()
if __name__ == '__main__':
    main()