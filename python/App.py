from User.employee import Employee
from User.user import User
from Util import sql

def login():
    print("the code of this method need to be written")

def main():
    login = input('login : ')
    password = input('password : ')
    current_user = sql.login(login,password)
    print(f'Current User is : {current_user.name}')
    current_user.app()
if __name__ == '__main__':
    main()