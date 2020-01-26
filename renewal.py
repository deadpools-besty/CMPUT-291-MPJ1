from datetime import datetime

def addYears(d, years):
    return d.replace(year = d.year + years)

def vehicle_renewal(c, conn):

    regno_list = []
    regnum = 0
    check = 0
    c.execute('SELECT regno from registrations')
    regno_list = c.fetchall()
    while check == 0:
        regnum = int(input('Enter your registration number: '))
        for i in range(len(regno_list)):
            if int(regnum) == regno_list[i][0]:
                check = 1
        if check == 1:
            break
        else:
            print('Sorry, no such registration number exists')
    c.execute('SELECT expiry from registrations where regno=?;', (str(regnum),))
    expiry = str(c.fetchone()[0])
    expiry = datetime.strptime(expiry, '%Y-%m-%d')
    expiry = datetime.date(expiry)
    curr_date = datetime.date(datetime.now())
    if expiry < curr_date:
        curr_date = addYears(curr_date, 1)
        c.execute('UPDATE registrations SET expiry=? where regno=?', (curr_date, regnum))
    else:
        expiry = addYears(expiry, 1)
        c.execute('UPDATE registrations SET expiry=? where regno=?', (expiry, regnum))
    conn.commit()
    return