import sqlite3

def driver_abstract(connection, cursor):
    c = cursor
    print('To obtain a driver abstract, enter the name of the driver you are looking for')
    valid_input = False
    while not valid_input: # get driver
        f_name = input("Enter first name: ")
        l_name = input("Enter last name: ")
        c.execute("select * from registrations where lower(fname)=? and lower(lname) = ?;", (f_name.lower(), l_name.lower())) # check if person is driver
        r = c.fetchone()
        if r != None:
            valid_input = True
        else:
            print("Person entered is not a driver. Please enter again")
    
    # sql statement to get number of tickets
    c.execute('''select count(tno) 
                from tickets join registrations using (regno) 
                where lower(fname)=? and lower(lname)=? group by regno;''', (f_name.lower(), l_name.lower()))
    ticket_amount = c.fetchone()
    if ticket_amount != None:
        ticket_amount = ticket_amount[0]
    else:
        ticket_amount = 0
    
    # sql statement to get number of demerit notices for driver
    c.execute('''select count(points) 
                from demeritNotices 
                where lower(fname)=? and lower(lname)=? group by fname, lname;''', (f_name.lower(), l_name.lower()))
    demerit_amount = c.fetchone()
    if demerit_amount != None:
        demerit_amount = demerit_amount[0]
    else:
        demerit_amount = 0

    #sql statement to get demerit sum in last 2 years
    c.execute('''select sum(points) 
                from demeritNotices 
                where ddate <= date('now') and ddate >= date('now', '-2 years') and 
                lower(fname)=? and lower(lname)=? 
                group by fname, lname;''', (f_name.lower(), l_name.lower()))
    demerit_sum_2yr = c.fetchone()
    if demerit_sum_2yr != None:
        demerit_sum_2yr = demerit_sum_2yr[0]
    else:
        demerit_sum_2yr = 0

    # sql statement to get demerit sum in lifetime
    c.execute('''select sum(points) 
                from demeritNotices 
                where lower(fname)=? and lower(lname)=? 
                group by fname, lname;''', (f_name.lower(), l_name.lower()))
    demerit_sum_life = c.fetchone()
    if demerit_sum_life != None:
        demerit_sum_life = demerit_sum_life[0]
    else:
        demerit_sum_life = 0

    print('''%s %s Driver Abstract: \nNumber of tickets: %d \nNumber of demerits: %d \nDemerit points in past 2 years: %d \nDemerits points in lifetime: %d'''
        %(f_name, l_name, ticket_amount, demerit_amount, demerit_sum_2yr, demerit_sum_life))
    
    if ticket_amount > 0:
        see_tix = input('Press enter to see tickets or q to close: ')
        if see_tix.lower() == 'q':
            return
        else:
            # get all tickets
            c.execute('''select tno, vdate, violation, fine, regno, make, model
                        from tickets
                        join registrations using (regno)
                        join vehicles using (vin) 
                        where lower(fname)=? and lower(lname)=?
                        order by vdate desc;''', (f_name.lower(), l_name.lower()))
            print('''|%-4s|%-11s|%-30s|%-5s|%-5s|%-20s|%-20s|''' %('TNO', 'VDATE', 'VIOLATION', 'FINE', 'REGNO', 'MAKE', 'MODEL'))
            data = c.fetchall()
            if len(data) < 5:
                for r in data:
                    print('|%-4s|%-11s|%-30s|%-5s|%-5s|%-20s|%-20s|' %(str(r[0]), r[1], r[2], str(r[3]), str(r[4]), r[5], r[6]))
            else:
                for i in range(5):
                    print('|%-4s|%-11s|%-30s|%-5s|%-5s|%-20s|%-20s|' %(str(data[i][0]), data[i][1], data[i][2], str(data[i][3]), str(data[i][4]), data[i][5], data[i][6]))
                view_more = input('Press enter to view more tickets or q to quit.')
                if view_more.lower() == 'q':
                    return
                else:
                    for i in range(5, len(data)):
                        print('|%-4s|%-11s|%-30s|%-5s|%-5s|%-20s|%-20s|' %(str(data[i][0]), data[i][1], data[i][2], str(data[i][3]), str(data[i][4]), data[i][5], data[i][6]))
    input(' ')
'''
conn = sqlite3.connect("test.db")	
c = conn.cursor()
c.execute('PRAGMA foreign_keys=ON;')
driver_abstract(conn, c)

conn.close()
'''