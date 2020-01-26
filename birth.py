import datetime
from datetime import date
from persons import persons

def birth_reg(c, conn, fname, lname):

    c.execute('SELECT regno from births')
    regnums = c.fetchall()
    check = 0
    regno = 0
    for x in range(1, 1000):
        for i in range(len(regnums)):
            if x == regnums[i][0]:
                check = 1
        if check == 0:
            regno = x
            break
        else:
            check = 0
    b_fname = str(input('Enter the first name of the newborn child: '))
    b_lname = str(input('Enter the last name of the newborn child: '))
    c.execute('SELECT city from users where fname=? and lname=?;', (fname, lname))
    city = c.fetchone()[0]
    gender = None
    while (gender != 'F' and gender != 'M'):
        gender = str(input('Enter the gender of the newborn child:')).upper()
    parents = []
    f_fname = str(input('Enter the father\'s first name: ')).capitalize()
    f_lname = str(input('Enter the father\'s last name: ')).capitalize()
    m_fname = str(input('Enter the mother\'s first name: ')).capitalize()
    m_lname = str(input('Enter the mother\'s last name: ')).capitalize()
    parents.append((f_fname, f_lname))
    parents.append((m_fname, m_lname))
    for parent in parents:
        for x in range(len(parents) - 1):
            c.execute('SELECT fname, lname from persons where fname=? and lname=?;', (parent[x], parent[x + 1]))
            f = c.fetchall()
            if not f:
                print('Person not in database, please provide information')
                Default = 'NULL'
                bdate = input('Enter birthdate in format YYYY-MM-DD: ')
                if not bdate:
                    bdate = Default
                bplace = input('Enter birthplace: ')
                if not bplace:
                    bplace = Default
                address = input('Enter address: ')
                if not address:
                    address = Default
                phone = input('Enter phone number in format XXX-XXX-XXXX: ')
                if not phone:
                    address = Default
                c.execute('INSERT into persons values (?, ?, ?, ?, ?, ?);', (parent[x], parent[x + 1], bdate, bplace, address, phone))
    curr_date = str(datetime.date.today())
    year, month, day = curr_date.split('-')
    datetime.datetime(int(year), int(month), int(day))
    c.execute("select address, phone from persons where fname=? and lname=?", (m_fname, m_lname))
    address_phone = c.fetchone()
    address = address_phone[0]
    phone = address_phone[1]
    c.execute("insert into persons values (?, ?, date('now'), ?, ?, ?);", (b_fname, b_lname, city, address, phone))
    print(regno, b_fname, b_lname, city, gender, f_fname, f_lname, m_fname, m_lname)
    c.execute("INSERT into births VALUES (?, ?, ?, date('now'), ?, ?, ?, ?, ?, ?);", (regno, b_fname, b_lname, city, gender, f_fname, f_lname, m_fname, m_lname))
    conn.commit()
    return
