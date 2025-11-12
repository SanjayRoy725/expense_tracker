import datetime
import sqlite3

import numpy as np
import pandas as pd
import database
import visuals
from database import get_exits_user

database.create_table()

df = pd.DataFrame(columns=["Name" , "salary" , "date" , "Expense_Name" , "Expense_Amt" ,"Savings"])

print("_________WELCOME_________")

def input_name():
    while True:
      name = input("Enter a name ->").strip()
      if name:
          return name
      else:
          print("Name cannot be empty")


def input_salary():
    while True:
        try:
           salary = int(input("Enter a salary :"))
           if salary < 0:
                print("salary can not be less then 0")
                continue
           return salary

        except ValueError:
            print("enter a valid amount")


def date_input():
    formats = ["%d/%m/%Y" , "%d-%m-%Y" , "%d/%m/%y" , "%d-%m-%y"]
    while True:
        date_str = input("Enter a date (dd/mm/yyyy or dd/mm/yy)").strip()
        for fnt in formats:
           try:
               date = datetime.datetime.strptime(date_str,fnt).date()
               return date
           except ValueError:
               continue
        print("enter a valid date")



def insert_expenses():
    input_expenses= []
    while True:
        expense_name = input("Enter expense name :").strip()
        if not expense_name:
            print("Exp_name cannot be empty.")
            continue
        try:
            expense_amt = float(input("Enter a Exp_amt"))
        except ValueError:
            print("Invalid amount enter valid amount:")
            continue
        input_expenses.append((expense_name,expense_amt))
        choice = input("Do you want to add another expenses select(Y/N)").strip().lower()
        if choice != 'y':
            break
    return input_expenses



def delete_expenses(name , expenses ,salary):
    if not expenses:
        print("No expenses found ")
        return expenses

    print("___All expenses___")
    for i , (exp_name , amount) in enumerate (expenses ,start=1):
        print(f"{i} {exp_name} amount = {amount}")

    delete_exp = input("Enter expense name you want to delete ->").strip().lower()

    found = False
    for exp in expenses:
        if exp[0].strip().lower() == delete_exp:
            expenses.remove(exp)
            found = True
            database.delete_expenses(delete_exp)
            print(f"{delete_exp} is delete successfully")
            total_amt = sum(amount for _,amount in expenses)
            savings = salary - total_amt
            print(f"total savings = {savings}")
            break
    if not found:
        print(f"expense {delete_exp} not found")
    return expenses

def all_expenses(name , expenses):
    if not expenses:
        print("no expenses record")
        return

    choice = input("Do you want to see expense list select(y/n)").strip().lower()

    if choice == 'y':
        print("______All expenses_______")
        for i , (exp_name ,  amount) in enumerate(expenses,start = 1):
            print(f"{i} : {exp_name} = {amount}")
        print("all expenses show successfully")
    else:
        print("okay thanks")


def highest_exp(expenses):
    if not expenses:
        print("No expenses record")
        return
    choice = input("Do you want to check highest expense select (y/n)").strip().lower()
    if choice == 'y':
        print("___Highest Expense___")
        high_exp = max(expenses , key=lambda x:x[1])
        print(f"Highest expenses : {high_exp[0]} = Amount{high_exp[1]}")

    else:
        print("Okay thanks")
# high_exp = highest_exp(expenses)


def lowest_exp(expenses):
    if not expenses:
        print("No expenses record")
        return
    choice = input("Do you want to check lowest expense select (y/n)").strip().lower()
    if choice == 'y':
        print("___Lowest Expense___")
        low_exp = min(expenses , key=lambda x:x[1])
        print(f"Lowest expense : {low_exp[0]} = amount{low_exp[1]}")

    else:
        print("Okay thanks")


def calculate_percent(salary , expenses):
    if not expenses:
        print("No expenses record")
        return
    choice = input("do you want to see percent of salary uses select (y/n):").strip().lower()
    if choice == 'y':

       total_spent = sum(amount for _ , amount in expenses)
       percent = (total_spent / salary) * 100
       print(f"you spent {percent} % of your salary.")
    else:
        print("No record it yet")
# cal_percent = calculate_percent(salary, expenses)


def check_exp_warning(salary , expenses):
    total_exp = sum(amount for _,amount in expenses)
    if total_exp > salary:
        print("____Warning____: Please reduce your expenses otherwise it might cause problem in the future")
    elif total_exp > 0.8 * salary:
        print("____Warning____: Use 80% of salary . Now stop")
    else:
        print("____Great balance____:You save upto 80% of your salary:")




# Choose any one add new or existing user

choice = input("1.)Add expenses for existing user 2.) Add new user  select one  3.) Delete user(1 , 2 , 3) ->").strip()
# while True:
if choice == '1':
    user = get_exits_user()
    if not user:
        print("No existing user found please add new user")
    else:
        print("_______Existing User_______")
        for i, u in enumerate(user, start=1):
            print(f"{i} Name: {u}")
        user_name = input("Select user number or name :").strip()
        if user_name.isdigit():
            name = user[int(user_name) - 1]
        else:
            name = user_name

        conn = sqlite3.connect("expense.db")
        curr = conn.cursor()
        curr.execute("select salary , date ,savings from expenses where name = ? order by rowid desc limit 1" , (name,))
        row = curr.fetchone()
        conn.close()

        if row:
            salary, exp_date , savings = row
            print(f"Welcome {name} salary = {salary} savings = {savings} date = {exp_date}")
            # expenses = []
            add_more = input("Do you want to add more expenses select (y/n)").strip().lower()
            if add_more == 'y':


                new_expense = insert_expenses()
                old_expense = database.get_user_expenses(name)
                total_exp = sum(a for _,a in old_expense) + sum(a for _,a in new_expense)
                savings = salary - total_exp


                database.insert_exp(name , salary,exp_date,new_expense,savings)
                print(f"Total savings now {savings}")
                print(f"Total expense added in database")
                view_all = database.view_all(name)
                all_expenses(name , view_all)
                lowest_exp(view_all)
                highest_exp(view_all)
                calculate_percent(salary,view_all)
                check_exp_warning(salary,view_all)

            elif add_more == 'n':
                print("Okay done")
                expenses = database.get_user_expenses(user_name)

            else:
                print("Okay done")
        else:
            print("User not found in database")

elif choice == '2':
    name = input_name()
    salary = input_salary()
    date = date_input()
    expenses = insert_expenses()
    total_exp = sum(a for _,a in expenses)
    savings = salary - total_exp
    database.insert_exp(name , salary , date , expenses , savings)
    print("New user add successfully")


elif choice == '3':
    user = database.get_exits_user()
    if not user:
        print("No user found")
    else:
        print("Exits User")
        for i , n in enumerate(user , start=1):
            print(f"{i} Name = {n}")
        user_name = input("Enter user name to delete").strip()
        confirm_del = input(f"Are you sure to delete {user_name}. select(y/n)").strip().lower()
        if confirm_del == 'y':
            database.delete_user(user_name)
            print(f"User {user_name} delete successfully.")
            updated_user = database.get_exits_user()
            if updated_user:
                print("____Exist User_____")
                for i , n in enumerate (updated_user ,start = 1):
                    print(f"{i} Name = {n}")
            else:
                print("NO user left")
        else:
            print("Deletion cancel")

else:
    print("Invalid option")

# SEE VISUALS REPRESENTATION OF DATA

view_visuals = input("Do you want to see visuals representation of data select(y/n)").strip().lower()
expenses = database.get_user_expenses(name)
if view_visuals == 'y':
    print("1.) View visuals of (expenses / salary) pie chart")
    print("2.) View visuals of (expenses_name / expenses_amt) bar chart")
    print("3.) View visuals of lowest expense (expense_name / expense_amt) pie chart")
    print("4.) View visuals of highest expense (expense_name / expense_amt) pie chart")
    print("5.) View visuals of (Savings) pie chart")
    choice = input("Select option (1/5) ->")

    if choice == '1':
        visuals.view_details(salary , expenses)
    elif choice == '2':
        visuals.view_expenses(expenses)
    elif choice == '3':
        visuals.view_lowest_expense(salary, expenses)
    elif choice == '4':
        visuals.view_highest_expense(salary, expenses)
    elif choice == '5':
        visuals.view_savings(salary, expenses)
    else:
        print("Invalid number1"
              "")



