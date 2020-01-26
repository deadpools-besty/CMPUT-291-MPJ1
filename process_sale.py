import sqlite3

def process_sale(connection, cursor):
    
    c = cursor
    correct_input = False
    print('To record a bill of sale enter the vin of a car, the name of the current owner,\n the name of the new owner, '
    + 'and a plate number for the new registration.')
    
    
    while not correct_input: # get vin
        vin = input('Enter VIN: ')
        c.execute("select * from vehicles where vin=?;", (vin,))
        car = c.fetchone()
        if car != None:
            correct_input = True
        else: 
            print("VIN entered is not in database. Please try again")

    correct_input = False # get current owner
    while not correct_input:
        c_owner_fname = input("Enter the current owner's first name: ")
        c_owner_lname = input("Enter the current owner's last name: ")
        c.execute("select * from registrations where vin=? order by regdate desc;", (vin,))
        owner = c.fetchone()
        if owner != None and owner[5].lower() + owner[6].lower() == c_owner_fname.lower() + c_owner_lname.lower(): #.lower() method used to make sure program is string insensitive
            correct_input = True
        else: 
            print("Owner in database does not match given owner. Sale cannot be processed.")
    
    correct_input = False
    while not correct_input: # get new owner
        n_owner_fname = input("Enter the new owner's first name: ") 
        n_owner_lname = input("Enter the new owner's last name: ")
        c.execute("select * from persons where lower(fname)=? and lower(lname)=?;", (n_owner_fname.lower(), n_owner_lname.lower()))
        n_owner = c.fetchone()
        if n_owner != None:
            correct_input = True
        else:
            print("Person does not exist in database. Please enter again.")
    
    plate = input("Enter a plate number (1 to 7 characters): ")

    # split names into list of characters to ensure the first letter of each name is a capital
    s = list(n_owner_fname)
    s[0] = s[0].upper()
    n_owner_fname = ''.join(s)
    
    s = list(n_owner_lname)
    s[0] = s[0].upper()
    n_owner_lname = ''.join(s)

    c.execute("update registrations set expiry = date('now') where lower(fname)=? and lower(lname)=?;", (c_owner_fname.lower(), c_owner_lname.lower()))
    c.execute("select max(regno) from registrations")
    regno = c.fetchone()[0] + 1
    c.execute("insert into registrations values (?, date('now'), date('now', '+1 year'), ?, ?, ?, ?);", (regno, plate, vin, n_owner_fname, n_owner_lname))
    connection.commit()
    print("Successfully added %s %s as the new owner of car no: %d under registration number %d" %(n_owner_fname, n_owner_lname, int(vin), int(regno)))
    print("Returning to main menu...")
'''
conn = sqlite3.connect("test.db")	
c = conn.cursor()
c.execute('PRAGMA foreign_keys=ON;')
process_sale(conn, c)

conn.close()
'''