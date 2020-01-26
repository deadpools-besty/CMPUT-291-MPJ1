import sqlite3
'''from getpass import getpass'''
import re
import datetime 
from datetime import date
import random

'''TRAFFIC OFFICERS QUESTION 1'''

def traffic_1(conn, curs):


    regno = input("Enter a registration number: ")
    type = ("o")

    if re.match("^[A-Za-z0-9_]*$", regno):
        curs.execute('SELECT r.fname, r.lname, v.make, v.model, v.color FROM users as u, registrations as r, vehicles as v WHERE r.regno=? and r.fname = u.fname and r.lname = u.lname and u.utype=? and r.vin = v.vin;' , (regno, type))

        rows = curs.fetchall() 
        for row in rows:
            print('{0}, {1}, {2}, {3}, {4}'.format(row[0], row[1], row[2], row[3], row[4]))

    violation = input("Enter your violation: ")
    fine2 = True
    while (fine2):
        fine = input("Enter a fine amount: ")
        try:
            num = int(fine)
            fine2 = False
        except ValueError:
            print("Not the correct input for fine amount.")
            fine2 = True

    date = True
    while(date):
        vdate = input("Enter a violation date in the format yyyy-mm-dd: ")
        if vdate == '':
            vdate = datetime.date.today()
            date = False
        else:
            try:
                datetime.datetime.strptime(vdate, '%Y-%m-%d')
                date = False
            except ValueError:
                print("Incorrect data format, should be YYYY-MM-DD")
                date = True

    curs.execute('SELECT max(tno) from tickets;')
    tno = curs.fetchone()[0] + 1

    curs.execute('INSERT INTO tickets values (?, ?, ?, ?, ?);', (tno, regno, fine, violation, vdate))
   
    conn.commit()
