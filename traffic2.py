import sqlite3
import re

def traffic_2(curs):
    make = input("Enter a make: ")
    model = input("Enter a model: ")
    year = input("Enter a year: ")
    color = input("Enter a color: ")
    plate = input("Enter a plate: ")
    
    curs.execute('SELECT distinct v.make, v.model, v.year, v.color, r.plate FROM vehicles as v, registrations as r WHERE (v.make=? and v.model=? and v.year=? and v.color=? and r.plate=?) or (v.make=? or v.model=? or v.year =? or v.color=? or r.plate=?);', 
    (make, model, year, color, plate, make, model, year, color, plate))

    rows = curs.fetchall() 
    for row in rows:
        print('{0}, {1}, {2}, {3}, {4}'.format(row[0], row[1], row[2], row[3], row[4]))