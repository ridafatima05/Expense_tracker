import streamlit as st
import pandas as pd
import os
import plotly.express as px

# --- File Paths ---
DATA_DIR = "data"
EXPENSE_FILE = os.path.join(DATA_DIR, "expenses.xlsx")
INCOME_FILE = os.path.join(DATA_DIR, "income.xlsx")

def load_data(file_path):
    """Load data and ensure 'amount' is numeric and 'date' is datetime."""
    if not os.path.exists(file_path):
        return pd.DataFrame()
    df = pd.read_excel(file_path, engine='openpyxl')
    if "amount" in df.columns:
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    if "date" in df.columns:
        # here we Set format to handle date objects saved as strings by Streamlit
        df["date"] = pd.to_datetime(df["date"], errors="coerce", format='mixed') 
    return df

def summary_page(username):
    st.title("📈 Financial Summary")
    
    # here we Load user-specific data
    df_expense = load_data(EXPENSE_FILE)
    df_income = load_data(INCOME_FILE)
    
    user_exp = df_expense[df_expense["username"] == username].dropna(subset=["amount"])
    user_inc = df_income[df_income["username"] == username].dropna(subset=["amount"])

    # --- Total Balance Calculation ---
    total_expense = user_exp["amount"].sum()
    total_income = user_inc["amount"].sum()
    net_balance = total_income - total_expense

    st.subheader("Account Overview")
    
    col1, col2, col3 = st.columns(3)
    
    
    col1.metric("Total Income 💰", f"PKR {total_income:,.2f}")
    col2.metric("Total Expense 💸", f"PKR {total_expense:,.2f}")
    
    
    balance_delta = f"({net_balance/total_income*100:.1f}%)" if total_income != 0 else ""
    balance_label = "Net Balance"
    
    
    if net_balance >= 0:
        col3.metric(balance_label, f"PKR {net_balance:,.2f}", balance_delta, delta_color="normal")
    else:
        col3.metric(balance_label, f"PKR {net_balance:,.2f}", balance_delta, delta_color="inverse")


    st.markdown("---")
    
    # --- Graphs Section ---
    st.subheader("Visual Reports")

    col_chart_exp, col_chart_inc = st.columns(2)
    
    # Expenses by Category (Pie Chart)
    with col_chart_exp:
        if not user_exp.empty:
            st.markdown("##### Expenses by Category")
            cat_sum = user_exp.groupby("category")["amount"].sum().reset_index()
            
            fig_pie = px.pie(
                cat_sum, 
                values="amount", 
                names="category", 
                title="Expense Distribution",
                hole=.3,
                color_discrete_sequence=px.colors.sequential.Plasma
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No expense data to generate category chart.")

    #  Income Over Time (Line Chart)
    with col_chart_inc:
        if not user_inc.empty and "date" in user_inc.columns:
            st.markdown("##### Income Over Time")
            # Group by month
            user_inc["Month"] = user_inc["date"].dt.to_period("M")
            time_sum = user_inc.groupby("Month")["amount"].sum().reset_index()
            time_sum["Month"] = time_sum["Month"].astype(str)
            
            fig_line = px.line(
                time_sum, 
                x="Month", 
                y="amount", 
                title="Monthly Income Trends",
                markers=True
            )
            fig_line.update_traces(line_color="#4CAF50") 
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.info("No income data to generate time series chart.")