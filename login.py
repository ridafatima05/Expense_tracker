import streamlit as st
import pandas as pd
import os

# --- Configuration ---
DATA_DIRECTORY = "data"
USERS_FILE = os.path.join(DATA_DIRECTORY, "users.xlsx")

# Ensure data folder and users file exist
if not os.path.exists(DATA_DIRECTORY):
    os.makedirs(DATA_DIRECTORY)

if not os.path.exists(USERS_FILE):
    # headers
    pd.DataFrame(columns=["username", "password"]).to_excel(USERS_FILE, index=False)

# --- User Management Functions ---

def load_users():
    """Load users from Excel file with all columns as string type for consistency."""
    try:
        # Here we use openpyxl 
        df = pd.read_excel(USERS_FILE, dtype=str, engine='openpyxl')
        return df.fillna("") 
    except Exception as e:
        st.error(f"Error loading user data: {e}")
        # If read fails, return an empty dataframe
        return pd.DataFrame(columns=["username", "password"])

def save_users(df):
    """Save the updated user dataframe back to the Excel file."""
    df.to_excel(USERS_FILE, index=False)

def register_user(username, password):
    """Registers a new user if the username is not taken."""
    users = load_users()
    
    if not username or not password:
        st.error("Username and Password cannot be empty.")
        return

    # Check for existing user (case-insensitive)
    if username.lower() in users["username"].str.lower().values:
        st.error("Username already exists! Choose another one.")
        return
    
    # Create new user record
    new_user = pd.DataFrame([{"username": username, "password": password}])
    users = pd.concat([users, new_user], ignore_index=True)
    save_users(users)
    st.success("✅ Account Created Successfully! Please log in.")

# --- UI Components ---

def logout_button():
    """Handles logging out the user."""
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.rerun()

def login_page():
    """Displays the login and registration interface."""
    st.set_page_config(page_title="Expense Tracker Login", layout="centered")
    st.title("💸 Personal Expense Tracker")
    st.markdown("---")

    menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("Access Mode", menu)

    if choice == "Login":
        st.subheader("Sign In to Track Expenses")
        with st.form("login_form"):
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
            submit_button = st.form_submit_button("🔑 Login")

            if submit_button:
                if not username or not password:
                    st.error("Please enter both username and password.")
                    return

                users = load_users()
                
                # here we Check for credentials
                match = users[
                    (users["username"] == username) & 
                    (users["password"] == password)
                ]
                
                if not match.empty:
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = username
                    st.success(f"Welcome back, {username}! Redirecting...")
                    st.rerun()
                else:
                    st.error("Invalid Credentials or User not registered.")
                
    else: # Register
        st.subheader("Create Your Free Account")
        with st.form("register_form"):
            username = st.text_input("Choose Username", key="reg_user")
            password = st.text_input("Choose Password", type="password", key="reg_pass")
            submit_button = st.form_submit_button("✍️ Register Account")

            if submit_button:
                register_user(username, password)

def main_app_interface():
    """The main application interface (Expense Tracker)."""
    st.set_page_config(page_title="Expense Tracker", layout="wide")
    
    st.sidebar.title("App Menu")
    logout_button()
    
    st.header(f"Welcome, {st.session_state.get('username', 'User')}!")
    st.title("💰 Expense Tracker Dashboard")
    st.markdown("This is where your expense tracking application logic would reside.")
    st.info("You are successfully logged in and can now access your private data.")

    # --- Placeholder Content for a real app ---
    st.subheader("Quick Expense Entry (Placeholder)")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.number_input("Amount ($)", min_value=0.01, format="%.2f", key="amount")
    with col2:
        st.selectbox("Category", ["Food", "Transport", "Bills", "Income"], key="category")
    with col3:
        st.date_input("Date", key="date")
        
    st.text_input("Description", key="description")
    
    if st.button("➕ Add Transaction", help="This is a dummy button, no data is saved yet."):
        st.toast(f"Transaction added: ${st.session_state.amount} for {st.session_state.category} on {st.session_state.date}")
        
    st.markdown("---")
    st.subheader("Your Recent Transactions (Mock Data)")
    
    mock_data = {
        "Date": ["2025-10-26", "2025-10-25", "2025-10-24"],
        "Category": ["Food", "Income", "Transport"],
        "Description": ["Coffee at Local Cafe", "Monthly Salary Deposit", "Uber Ride Home"],
        "Amount": [-5.50, 4500.00, -18.75]
    }
    st.dataframe(pd.DataFrame(mock_data), use_container_width=True)


# --- Main Application Execution ---

if __name__ == "__main__":
    # Initialize session state variables if they don't exist
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "username" not in st.session_state:
        st.session_state["username"] = ""

    if st.session_state["logged_in"]:
        main_app_interface()
    else:
        login_page()