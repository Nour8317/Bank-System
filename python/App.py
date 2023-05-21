from User.employee import Employee
from User.user import User
from Util import sql as sql_file

def login():
    print("the code of this method need to be written")

def main():
    login = input('login : ')
    password = input('password : ')
    sql = sql_file.SQL()
    current_user = sql.login(login,password)
    if not current_user:
        print('Invalid Credintials')
        return
    current_user.app()
if __name__ == '__main__':
    main()