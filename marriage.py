import datetime
from datetime import date
from persons import persons

def marriage(c, conn, fname, lname):

    # Finds the two people being married by user input
    marriage = []
    for x in range(2):
        c.execute('SELECT fname, lname from persons')
        names = c.fetchall()
        marriage_fname = input('Enter the first name of partner %s being married: ' % (x + 1))
        if not (marriage_fname.upper() in (name[0].upper() for name in names)):
            print('No such first name exists')
            persons(c, conn)
        marriage_lname = input('Enter the last name of partner %s being married: ' % (x + 1))
        if not (marriage_lname.upper() in (name[1].upper() for name in names)):
            print('No such last name exists')
            persons(c, conn)
        marriage.append((marriage_fname, marriage_lname))
    # Capitalizes the first character of every name
    capitalization = []
    for i in range(len(marriage)):
        for j in range(len(marriage[i])):
            capitalization.append(marriage[i][j].title())

    # Finds all regno in database
    c.execute('SELECT regno from marriages')
    regnums = c.fetchall()
    # Finds a regno not in database
    check = 0
    for x in range(1, 1000):
        for i in range(len(regnums)):
            if x == regnums[i][0]:
                check = 1
        if check == 0:
            regno = x
            break
        else:
            check = 0

    curr_date = str(datetime.date.today())
    year, month, day = curr_date.split('-')
    datetime.datetime(int(year), int(month), int(day))
    #print(curr_date)

    # Finds city of user
    c.execute('SELECT city from users where fname=? and lname=?;', (fname, lname))
    city = c.fetchone()[0]
    # Inserts marriage
    c.execute('INSERT INTO marriages VALUES (?, ?, ?, ?, ?, ?, ?);', (regno, curr_date, city , capitalization[0], capitalization[1], capitalization[2], capitalization[3]))
    conn.commit()
    return
