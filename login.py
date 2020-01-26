from getpass import getpass
import re

def login(cursor):        
    
    c = cursor
    i = True

    while i == True:
        username = input('Input a Username: ')
        password = getpass()

        if re.match("^[A-Za-z0-9_]*$", username.lower()) and re.match("^[A-Za-z0-9_]*$", password):
            c.execute('SELECT * FROM users WHERE lower(uid)=? and pwd=?;' , (username.lower(), password))
            user = c.fetchone()
            if user != None:
                return user
            else:
                print('Incorrect username or password')
