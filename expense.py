import streamlit as st
import pandas as pd
import os
from datetime import date

DATA_DIR = "data"
EXPENSE_FILE = os.path.join(DATA_DIR, "expenses.xlsx")
CATEGORY_FILE = os.path.join(DATA_DIR, "categories.xlsx")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Create files if they do not exist
if not os.path.exists(EXPENSE_FILE):
    pd.DataFrame(columns=["username", "date", "amount", "category", "note"]).to_excel(EXPENSE_FILE, index=False)

if not os.path.exists(CATEGORY_FILE):
    pd.DataFrame(columns=["username", "category"]).to_excel(CATEGORY_FILE, index=False)

def load_categories():
    df = pd.read_excel(CATEGORY_FILE, engine='openpyxl')
    return df

def save_categories(df):
    df.to_excel(CATEGORY_FILE, index=False)

# --- Category Management ---
def add_category(username):
    st.subheader("➕ Add New Category")
    with st.form("category_form", clear_on_submit=True):
        cat_name = st.text_input("Category Name").strip()
        if st.form_submit_button("Add Category"):
            if not cat_name:
                st.error("Category name cannot be empty.")
                return

            df = load_categories()
            if ((df["username"] == username) & (df["category"].str.lower() == cat_name.lower())).any():
                st.warning(f"Category '{cat_name}' already exists!")
            else:
                new_row = pd.DataFrame([{"username": username, "category": cat_name}])
                df = pd.concat([df, new_row], ignore_index=True)
                save_categories(df)
                st.success(f"Category '{cat_name}' added!")

def view_categories(username):
    st.subheader("📋 Your Categories")
    df = load_categories()
    user_categories = df[df["username"] == username]
    if not user_categories.empty:
        st.dataframe(user_categories[["category"]], use_container_width=True, hide_index=True)
    else:
        st.info("No categories added yet.")

# --- Expense Management ---
def load_expenses():
    df = pd.read_excel(EXPENSE_FILE, engine='openpyxl')
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    return df

def save_expenses(df):
    df.to_excel(EXPENSE_FILE, index=False)

def add_expense(username):
    st.subheader("➕ Add New Expense")
    
    categories_df = load_categories()
    user_categories = categories_df[categories_df["username"]==username]["category"].tolist()

    if not user_categories:
        st.warning("No categories found. Please add a category first via the 'Manage Categories' tab.")
        return

    with st.form("expense_form", clear_on_submit=True):
        date_input = st.date_input("Date", value=date.today())
        # Currency changed to PKR
        amount = st.number_input("Amount (PKR)", min_value=0.0, format="%.2f")
        category = st.selectbox("Category", user_categories)
        note = st.text_input("Note/Description")

        submitted = st.form_submit_button("💸 Add Expense")
        if submitted:
            if amount <= 0:
                st.error("Amount must be greater than zero.")
            else:
                df = load_expenses()
                new_row = pd.DataFrame([{
                    "username": username,
                    "date": date_input.isoformat(),
                    "amount": amount,
                    "category": category,
                    "note": note
                }])
                df = pd.concat([df, new_row], ignore_index=True)
                save_expenses(df)
                # Currency changed to PKR
                st.success(f"Expense of PKR {amount:,.2f} for '{category}' added!")

def view_expense(username):
    st.subheader("📋 Your Expenses")
    df = load_expenses()
    user_data = df[df["username"]==username]
    
    if not user_data.empty:
        user_data_display = user_data.sort_values(by="date", ascending=False)
        # Currency changed to PKR
        st.dataframe(
            user_data_display[["date", "category", "amount", "note"]].style.format({"amount": "PKR {:,.2f}"}), 
            use_container_width=True
        )
    else:
        st.info("You haven't recorded any expenses yet.")

# --- Main Expense Page ---
def expense_page(username):
    st.title("💸 Expenses")
    action = st.radio("What would you like to do?", 
                      ["Add Expense", "Manage Categories", "View Expenses"])

    if action == "Add Expense":
        add_expense(username)
    elif action == "Manage Categories":
        col1, col2 = st.columns(2)
        with col1:
            add_category(username)
        with col2:
            view_categories(username)
    else: # View Expenses
        view_expense(username)