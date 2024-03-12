import psycopg2
import os
from time import sleep

con = psycopg2.connect(
database="Library",
user="postgres",
password="12345678",
host="localhost",
port= '5432'
)

cur = con.cursor()

def getbookname(num):
    sql = "select title from books\
        where book_id = %s"
    cur.execute(sql,(num,))
    rows = cur.fetchall()
    name = rows[0][0]
    return name

def getstname(num):
    sql = "select first_name from students\
        where student_id = %s"
    cur.execute(sql,(num,))
    rows = cur.fetchall()
    name = rows[0][0]
    return name

def checkavail(num):
    sql = "select availablity\
        from books\
        where book_id = %s"
    cur.execute(sql,(num,))
    rows  = cur.fetchall()
    return rows[0][0]

def sbybook():
    name_part = input("\nEnter the name:")
    sql = "Select book_id, title, author from books where title ilike %s"
    cur.execute(sql,('%'+ name_part + '%',))
    rows = cur.fetchall()
    for row in rows:
        print(row)
        if checkavail(row[0]):
            print("Book is available\n")
        else:
            print("Book is currently unavailable\n")

def sbybid():
    id_part = input("\nEnter the book_id:")
    sql = 'Select book_id, title, author from books where book_id = %s'
    cur.execute(sql,(id_part,))
    rows = cur.fetchall()
    for row in rows:
        print(row)
        if checkavail(row[0]):
            print("Book is available\n")
        else:
            print("Book is currently unavailable\n")

def sbyauth():
    auth_part = input("\nEnter the name:")
    sql = "Select book_id, title, author from books where author ilike %s"
    cur.execute(sql,('%'+ auth_part + '%',))
    rows = cur.fetchall()
    for row in rows:
        print(row)
        if checkavail(row[0]):
            print("Book is available\n")
        else:
            print("Book is currently unavailable\n")

def sbysid():
    stid_part = input("\nEnter the student_id:").upper()
    sql = 'Select student_id, first_name, last_name,batch, email \
        from students where student_id ilike %s'
    cur.execute(sql,('%'+stid_part+ '%',))
    rows = cur.fetchall()
    for row in rows:
        print(row)

while True:
    print(" 1.Search \n 2.Check out \n 3.Return \n 4.Add a Book \n 5.Add a Student \n 6.Exit")
    process = int(input("Enter the category:"))
    match process:
        case 1:
            print("\n1. Search by Book name \n2. Search by Book id\n3. Search by Author\n4. Serach by student id")
            search_cat = int(input("Enter the category:"))
            match search_cat:
                case 1: sbybook()
                case 2: sbybid()
                case 3: sbyauth()
                case 4: sbysid()

        case 2:
            st_id = (input("Enter student id:")).upper()
            b_id = int(input("Enter book id:"))
            if checkavail(b_id):
                sql = "insert into history(borrowed_book,borrower,borrow_date,return_date)\
                    values\
                    (%s,%s,CURRENT_DATE,NULL)"
                cur.execute(sql,(b_id,st_id,))
                print(getbookname(b_id)+" issued to "+getstname(st_id))

                sql = "update books\
                    set availablity = false\
                        where book_id = %s"
                cur.execute(sql,(b_id,))
            else:
                print("Book is unavailable currently")


        case 3:
            t_id = int(input("Enter transaction id:"))
            b_id = int(input("Enter book id:"))
            sql = "update history\
                set return_date = current_date\
                where transaction_id = %s"
            cur.execute(sql,(t_id,))
            print(getbookname(b_id) + " has been returned")

            sql = "update books\
                set availablity = true\
                    where book_id = %s"
            cur.execute(sql,(b_id,))
        
        case 4:
            title = input("Enter the book name:")
            auth = input("Enter the authors name:")
            cost = int(input("Enter the replacement cost:"))
            sql = "insert into books(title,author,availablity,replacement_cost)\
                values\
                (%s,%s,True,%s)"
            cur.execute(sql,(title,auth,cost,))
            print(title + " has been added to directory")

        case 5:
            r_num = input("Enter the Student roll number:")
            f_name = input("Enter the first name:")
            l_name = input("Enter the last name:")
            batch = input("Enter the batch name:")
            email = input("Enter the students email:")
            sql = "insert into students(student_id,first_name,last_name,batch,email)\
                values\
                (%s,%s,%s,%s,%s)"
            cur.execute(sql,(r_num,f_name,l_name,batch,email,))
            print(f_name + " has been added to directory")    

        case 6: 
            os.system('cls')
            print("\tTHANK YOU")
            break

        case _: 
            os.system('cls')
            break

    sleep(10)
    os.system('cls')
    con.commit()
    
cur.close()
con.close()