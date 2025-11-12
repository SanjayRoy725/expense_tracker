import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def view_details(salary , expenses):
    if not expenses:
        print("No expenses data for visuals")
        return

    total_expenses = sum(amount for _, amount in expenses)
    savings = salary - total_expenses

    labels = ['Expenses', 'Savings']
    values = [total_expenses , savings]

    plt.figure(figsize=(2.1,2.1) , dpi=120)
    plt.pie(values,labels = labels , autopct='%1.1f%%' , startangle=90, textprops={'fontsize':8})
    plt.title("Saving vs Expenses")
    plt.show()

def view_expenses(expenses):
    df = pd.DataFrame(expenses , columns = ['expense_name' , 'expense_amt'])
    sns.barplot(data = df , x = 'expense_name' , y = 'expense_amt' , palette = 'rainbow')
    plt.xlabel("expenses_name")
    plt.ylabel("expense_amt")
    plt.show()

def view_lowest_expense(salary , expenses):
    df = pd.DataFrame(expenses , columns = ['expense_name' , 'expense_amt'])

    if df.empty or df['expense_name'].empty:
        print("No expense data available")
        return

    df = df.dropna(subset=['expense_amt'])
    if df.empty:
        print("No expense data available")
        return

    df['expense_amt'] = pd.to_numeric(df['expense_amt'] , errors = 'coerce')
    df = df.dropna(subset=['expense_amt'])
    if df.empty:
        print("No expense data available")
        return

    lowest = df.loc[df['expense_amt'].idxmin()]
    expense_name = lowest['expense_name']
    expense_amt = lowest['expense_amt']

    percent = (expense_amt / salary) * 100
    print(f"Lowest expense :{expense_name}  amount = {expense_amt}")
    print(f"It is a {percent} % of your salary {salary}")

    labels = [expense_name , 'remaining_salary']
    values = [expense_amt , salary - expense_amt]

    plt.pie(values , labels = labels , autopct='%1.1f%%' , startangle=90)
    plt.title(f"low expenses ({expense_name}) of salary {percent} %")
    plt.show()

def view_highest_expense(salary , expenses):
    df = pd.DataFrame(expenses , columns = ['expense_name' , 'expense_amt'])

    if df.empty or df['expense_name'].empty:
        print("No expense data available")
        return

    df = df.dropna(subset=['expense_amt'])
    if df.empty:
        print("No expense data available")
        return

    df['expense_amt'] = pd.to_numeric(df['expense_amt'], errors='coerce')
    df = df.dropna(subset=['expense_amt'])
    if df.empty:
        print("No expense data available")
        return

    highest = df.loc[df['expense_amt'].idxmax()]
    expense_name = highest['expense_name']
    expense_amt = highest['expense_amt']

    percent = (expense_amt  / salary) * 100
    print(f"Highest expense :{expense_name} amount = {expense_amt}")
    print(f"It is a {percent} % of your salary {salary}")

    labels = [expense_name , 'remaining_salary']
    values = [expense_amt , salary - expense_amt]

    plt.pie(values , labels=labels , autopct='%1.1f%%' , startangle=90)
    plt.title(f"Highest expense ({expense_name}) of salary {percent} %")
    plt.show()

def view_savings(salary,expenses):
    df = pd.DataFrame(expenses, columns = ['expense_name' , 'expense_amt'])
    total_expense = sum(amount for _, amount in expenses)
    savings = salary - total_expense
    print(f"total expense = {total_expense}")
    print(f"total savings = {savings}")

    labels = ['salary' , 'savings']
    values = [salary , savings]

    plt.pie(values , labels = labels , autopct='%1.1f%%' , startangle=90)
    plt.title("Salary and Savings")
    plt.show()







