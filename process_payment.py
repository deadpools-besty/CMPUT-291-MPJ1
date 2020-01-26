import sqlite3

def process_payment(connection, cursor):
    
    c = cursor
    print("To enter a payment, enter a valid ticket number and an amount.")
    

    valid_input = False # get ticket number
    while not valid_input:
        ticketno = input("Enter a ticket number: ")
        c.execute("select * from tickets where tno=?;", (ticketno,))
        ticket = c.fetchone()
        if ticket != None:
            fine = ticket[2]
            valid_input = True
        else:
            print('Invalid ticket number. Please try again')
    

    valid_input = False # get payment amount
    while not valid_input:
        pay = input("Enter a payment amount or 'q' to quit: ")
        c.execute("select sum(amount) from payments where tno=? group by tno", (ticketno,))
        paid = c.fetchone()
        if paid == None:
            paid = 0
        else:
            paid = paid[0]
        if pay == 'q':
            return
        elif int(pay) + paid <= fine:
            valid_input = True
        else:
            print("Total payment ($%d) greater than ticket amount ($%d). Please enter a lower amount" %(paid + int(pay), fine))
    try:
        c.execute("insert into payments values (?, date('now'), ?);", (ticketno, pay))
        connection.commit()
        print("Successfully paid $%d towards ticket number %s\nRemaining amont: $%d" %(int(pay), ticketno, (fine - int(pay) + paid)))
        print("Returning to main menu...")
    except:
        print("Error: Cannot make multiple payments to same ticket on same day")
    
'''
conn = sqlite3.connect("test.db")	
c = conn.cursor()
c.execute('PRAGMA foreign_keys=ON;')
process_payment(conn, c)

conn.close()
'''