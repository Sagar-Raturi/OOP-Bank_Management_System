import streamlit as st
from bank import Bank
import pandas as pd

bank = Bank()
st.set_page_config(page_title = "Bank System", page_icon = ":bank:", layout = "centered")
st.title("Bank Management System :bank:")

menu = st.sidebar.selectbox("Menu", ['Create Account', 'Deposit Money', 'Withdraw Money', 'Check Balance', 'View Transactions'])

if menu == "Create Account":
    st.subheader("Create a New Account")
    name = st.text_input("Enter your name")
    email = st.text_input("Enter your email ID")
    pin = st.text_input("Set a security pin", type = "password")
    balance = st.number_input("Enter initial balance (default is 0)", min_value = 0.0, value = 0.0)

    if st.button("Create Account"):
        success, message = bank.create_account(name, email, pin, balance)
        if success:
            st.success(message)
        else:
            st.error(message)
    
elif menu == "Deposit Money":
    st.subheader("Deposit Money")
    email = st.text_input("Enter your email ID")
    pin = st.text_input("Enter your security pin",type = "password")
    amount = st.number_input("Enter amount to deposit", min_value = 0.0)

    if st.button("Deposit"):
        success, message = bank.deposit(email, pin, amount)
        if success:
            st.success(message)
        else:
            st.error(message)

elif menu == "Withdraw Money":
    st.subheader("Withdraw Money")
    email = st.text_input("Enter your email ID")
    pin = st.text_input("Enter your security pin", type = "password")
    amount = st.number_input("Enter amount to withdraw", min_value = 0.0)

    if st.button("Withdraw"):
        success, message = bank.withdraw(email, pin, amount)
        if success:
            st.success(message)
        else:
            st.error(message)

elif menu == "Check Balance":
    st.subheader("Check Balance")
    email = st.text_input("Enter your email ID")
    pin = st.text_input("Enter your security pin", type = "password")
    if st.button("Check Balance"):
        success, message = bank.check_balance(email, pin)
        if success:
            st.success(f"Your current balance is : {message}")
        else:
            st.error(message)

elif menu == "View Transactions":
    st.subheader("View Transaction History ")
    email = st.text_input("Enter your email ID")
    pin = st.text_input("Enter your security pin", type = "password")
    if st.button("View Transactions"):
        success, message = bank.view_transactions(email, pin)
        if success:
            st.success("Transaction History:")
            df = pd.DataFrame(message)
            df.rename(columns={"type": "Type", "amount": "Amount", "timestamp": "Timestamp", "balance_after": "Balance After"}, inplace=True)
            st.dataframe(df)
        else:
            st.error(message)
    