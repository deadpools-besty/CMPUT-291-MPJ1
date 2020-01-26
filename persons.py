def persons(c, conn):

    print('System requires information to add person to database')
    Default = 'NULL'
    fname, lname = '',''
    while not fname:
        fname = input('Enter first name: ')
    while not lname:
        lname = input('Enter last name: ')
    bdate = input('Enter birth date in format yyyymmdd: ')
    if not bdate:
        bdate = Default
    bplace = input('Enter birth place: ')
    if not bplace:
        bplace = Default
    address = input('Enter address')
    if not address:
        address = Default
    phone = input('Enter 10 digit phone number in format XXXXXXXXXX:')
    if not phone:
        phone = Default
    c.execute('INSERT into persons VALUES (?, ?, ?, ?, ?, ?)', (fname, lname, bdate, bplace, address, phone))
    conn.commit()
    return
