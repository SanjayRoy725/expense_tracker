import sqlite3

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import database
import visuals

# from expenses_tracking import savings

st.set_page_config(page_title = "Expense.tracker" , layout = "wide")
st.title("💰 Expense Tracker Dashboard")
users = database.get_exits_user()

tab_1 , tab_2 , tab_3 , tab_4 , tab_5 , tab_6= st.tabs(["🧍‍ Add new user" , "👤 Add exp existing user" , "📋 View user exp" , "📊 Visuals of exp" , "💡📊 Salary vs Savings" , "🧹 Delete User"])

with tab_1:
    st.header(" 🧍‍♂️ Add New User")
    name = st.text_input("Enter User Name")
    salary = st.number_input("Enter Salary" , min_value=0)
    date = st.date_input("Select Date")
    exp_name = st.text_input("Expense Name")
    exp_amt = st.number_input("Expense Amt" , min_value=0)

    if st.button("👤➕Add Expense"):
        if name and  exp_name:
            savings = salary - exp_amt
            database.insert_exp(name , salary , date , [(exp_name,exp_amt)], savings)
            st.success(f"Add expense {exp_name} for {name}")
        else:
            st.warning("Please fill all details")

with tab_2:
    st.header("👤 Add exp for existing User")
    if users:
        select_user = st.selectbox("Select existing user" , users)
        conn = sqlite3.connect("expense.db")
        curr = conn.cursor()
        curr.execute("select salary , date , savings from expenses where name = ? order by rowid desc limit 1" , (select_user,))
        row = curr.fetchone()
        conn.close()

        if row:
            salary,date,savings = row
            st.info(f"Salary {salary} / Date {date} / Savings {savings}")

            exp_name = st.text_input("Enter New Expense")
            exp_amt = st.number_input("Enter Exp Amount" , min_value=0)

            if st.button("💰➕Add New Expense"):
                if exp_name:
                    database.insert_exp(select_user,salary,date , [(exp_name,exp_amt)] , 0)
                    st.success(f"Expense {exp_name} of amount {exp_amt} add successfully {select_user}")
                else:
                    st.warning("Please enter exp_name")
        else:
            st.warning("Please select exits user , Add new User")

with tab_3:
    st.header("📋 View User Expenses")
    if users:
        select_user = st.selectbox("SELECT USER 👉" , users)
        expenses = database.get_user_expenses(select_user)

        if expenses:
            df = pd.DataFrame(expenses,columns = ["Exp_name" , "Amount"])
            st.dataframe(df)
        else:
            st.info("No exp found")

    else:
        st.warning("No user found in database")

with tab_4:
    st.header("📊 Visuals of Expense")
    if users:
        select_user = st.selectbox("Select User To View Visuals 👉" , users)

        expenses = database.get_user_expenses(select_user)
        if expenses:
            conn = sqlite3.connect("expense.db")
            curr = conn.cursor()
            curr.execute("select salary from expenses where name = ? order by rowid desc limit 1", (select_user,))
            row = curr.fetchone()
            curr.close()
            if row:
                salary = row[0]
                st.write(f"Salary {salary}")

                chart_option = st.selectbox("Select Visual Type 👉" , ["Savings VS Expenses(PIE)" , "All Expenses (Bar_Chart)" , "Lowest Expenses (PIE)" , "Highest Expenses(PIE)" , "Salary VS Savings(PIE)"])
                plt.clf()
                if chart_option == "Savings VS Expenses(PIE)":
                    visuals.view_details(salary, expenses)
                    st.pyplot(plt.gcf())

                elif chart_option == "All Expenses (Bar_Chart)":
                    visuals.view_expenses(expenses)
                    st.pyplot(plt.gcf())

                elif chart_option == "Lowest Expenses (PIE)":
                    visuals.view_lowest_expense(salary, expenses)
                    st.pyplot(plt.gcf())

                elif chart_option == "Highest Expenses(PIE)":
                    visuals.view_highest_expense(salary, expenses)
                    st.pyplot(plt.gcf())

                elif chart_option == "Salary VS Savings(PIE)":
                    visuals.view_savings(salary , expenses)
                    st.pyplot(plt.gcf())

            else:
                st.warning("No salary found")

        else:
            st.warning("No expenses found")

    else:
        st.warning("No user found")


with tab_5:
    st.header("💡 📊Insight & Charts")
    if users:
        select_user = st.selectbox("Select User for Insight 👉" , users)
        expenses = database.get_user_expenses(select_user)
        if expenses:
            df = pd.DataFrame(expenses,columns=["exp_name" , "Amount"])
            total_exp = df["Amount"].sum()

            st.metric(label = "Total Expense" , value = f"{total_exp}")
            st.metric(label = "Total Savings" , value = f"{salary - total_exp}")

            st.subheader("Expense Distribution")
            st.bar_chart(df.set_index("exp_name"))

        else:
            st.info("No data available")


with tab_6:
    st.header("🧹 Delete User")
    if users:
        select_user = st.selectbox("Select User To Delete 👉" , users)
        if st.button("Delete User"):
            database.delete_user(select_user)
            st.success(f"User {select_user} deleted successfully")

    else:
        st.warning("No user available")






