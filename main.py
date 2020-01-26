import sqlite3
import os
from login import login
from process_sale import process_sale
from process_payment import process_payment
from driver_abstract import driver_abstract
from renewal import vehicle_renewal
from traffic1 import traffic_1
from traffic2 import traffic_2
from birth import birth_reg
from marriage import marriage


def main():
    
    db_exists = False
    while not db_exists:
        db_name = input('Enter a database name: ')
        if os.path.exists(db_name):
            conn = sqlite3.connect(db_name)	
            c = conn.cursor()
            c.execute('PRAGMA foreign_keys=ON;')
            db_exists = True
        else:
            print("Database does not exist.")

    q = False
    while not q:
        logout = False
        user = login(c)
        while not logout:
            print("Main Menu")
            valid_input = False
            if user[2].lower() == 'a':
                while not valid_input:
                    print('\n')
                    print("1. Register a birth")
                    print("2. Register a marriage")
                    print("3. Renew a vehicle registration")
                    print("4. Process a bill of sale")
                    print("5. Process a payment")
                    print("6. Get a driver abstract") 
                    u_input = input("Enter a number (l to 6), or 'l' to logout, or 'q' to quit: ")
                    if u_input == '1':
                        birth_reg(c, conn, user[3], user[4])
                    elif u_input == '2':
                        marriage(c, conn, user[3], user[4])
                    elif u_input == '3':
                        vehicle_renewal(c, conn)
                    elif u_input == '4':
                        process_sale(conn, c)
                    elif u_input == '5':
                        process_payment(conn, c)
                    elif u_input == '6':
                        driver_abstract(conn, c)
                    elif u_input.lower() == 'l':
                        logout = True
                        break
                    elif u_input.lower() == 'q':
                        quit()
                    else:
                        print('Invalid input')
            else:
                while not valid_input:
                    print("1. Issue ticket")
                    print("2. Find a car owner")
                    u_input = input("Enter a number (1 or 2), or 'l' to logout or 'q' to quit: ")
                    if u_input == '1':
                        traffic_1(conn, c)
                    elif u_input == '2':
                        traffic_2(c)
                    elif u_input.lower() == 'l':
                        logout = True
                        break
                    elif u_input.lower() == 'q':
                        quit()
                        break
                    else:
                        print('Invalid input')
                        
    conn.close()
main()