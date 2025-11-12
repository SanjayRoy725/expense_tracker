import sqlite3

def create_table():
   conn = sqlite3.connect("expense.db")
   curr = conn.cursor()
   curr.execute('''create table if not exists expenses
   (name TEXT,
   salary INTEGER,
   date TEXT,
   expense_name TEXT,
   expense_amt INTEGER,
   savings INTEGER)
   ''')
   conn.commit()
   conn.close()
   print("Table create successfully")

def insert_exp(name , salary , date , expenses , savings):
    conn = sqlite3.connect("expense.db")
    curr = conn.cursor()
    for exp_name , exp_amt in expenses:
       curr.execute('insert into expenses (name , salary , date , expense_name , expense_amt , savings) values (?, ?, ?, ?, ?, ?)',(name , salary , date , exp_name , exp_amt , savings))
    conn.commit()
    conn.close()
    print("insert expenses into database")


def view_all(name):
    conn = sqlite3.connect("expense.db")
    curr = conn.cursor()
    curr.execute("select expense_name , expense_amt from expenses where name = ?", (name,))
    rows = curr.fetchall()
    conn.close()
    return rows

def delete_expenses(expense_name):
    conn = sqlite3.connect("expense.db")
    curr = conn.cursor()
    curr.execute("delete from expenses where expense_name = ?" , (expense_name,))
    conn.commit()
    conn.close()

def get_exits_user():
    conn = sqlite3.connect("expense.db")
    curr = conn.cursor()
    curr.execute("select distinct name from expenses where name is not null and name != ''")
    rows = [row[0] for row in curr.fetchall()]
    conn.close()
    return rows

def delete_user(user_name):
    conn = sqlite3.connect("expense.db")
    curr = conn.cursor()
    curr.execute("delete from expenses where lower(trim(name)) = lower(trim(?))" , (user_name,))
    conn.commit()
    conn.close()
    print(f"User '{user_name}' deleted successfully from database.")

def get_user_expenses(user_name):
    conn = sqlite3.connect("expense.db")
    curr = conn.cursor()
    curr.execute("select expense_name , expense_amt from expenses where name = ?" , (user_name,))
    data = curr.fetchall()
    conn.close()
    return data

