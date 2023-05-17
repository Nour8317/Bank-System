from User.employee import Employee
from User.user import User
from Util import sql
def main():
    login = input('login : ')
    password = input('password : ')
    current_user = sql.login(login,password)
    current_user.app()

if __name__ == '__main__':
    main()