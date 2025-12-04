import streamlit as st
import pandas as pd
import os
from datetime import date

DATA_DIR = "data"
INCOME_FILE = os.path.join(DATA_DIR, "income.xlsx")


if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Create income file if not exists 
if not os.path.exists(INCOME_FILE):
    pd.DataFrame(columns=["username", "date", "source", "amount"]).to_excel(INCOME_FILE, index=False)

def load_income():
    df = pd.read_excel(INCOME_FILE, engine='openpyxl')
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    return df

def save_income(df):
    df.to_excel(INCOME_FILE, index=False)

def income_page(username):
    st.title("💰 Income Tracker")

    income_df = load_income()

    with st.form("income_form", clear_on_submit=True):
        st.subheader("Add New Income Record")
        date_input = st.date_input("Date", value=date.today())
        source = st.text_input("Source (e.g., Salary, Freelance)")
        
        amount = st.number_input("Amount (PKR)", min_value=0.0, format="%.2f")

        submitted = st.form_submit_button("➕ Add Income")
        if submitted:
            if not source or amount <= 0:
                st.error("Please enter a valid source and amount.")
            else:
                new_row = pd.DataFrame([{
                    "username": username,
                    "date": date_input.isoformat(), 
                    "source": source, 
                    "amount": amount
                }])
                income_df = pd.concat([income_df, new_row], ignore_index=True)
                save_income(income_df)
                # Currency changed to PKR
                st.success(f"Income of PKR {amount:,.2f} added successfully!")

    st.subheader("Your Income Records")
    user_income = income_df[income_df["username"] == username]
    if not user_income.empty:
        user_income_display = user_income.sort_values(by="date", ascending=False)
        # Currency changed to PKR
        st.dataframe(
            user_income_display[["date", "source", "amount"]].style.format({"amount": "PKR {:,.2f}"}), 
            use_container_width=True
        )
    else:
        st.info("You haven't recorded any income yet.")