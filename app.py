import streamlit as st

# Importing the pages
from login import login_page, logout_button
from income import income_page
from expense import expense_page
from summary import summary_page

# --- Configuration and Theming ---
st.set_page_config(
    page_title="Personal Finance Tracker",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better look
st.markdown(
    """
    <style>
    /* Styling Streamlit containers for better padding */
    .stApp {
        padding-top: 10px;
    }
    /* Style the sidebar menu items */
    .st-emotion-cache-1g8wz3g > div {
        font-size: 1.1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Core Logic ---
# Initialize session state with guaranteed keys
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Dashboard"

# --- Routing ---
if not st.session_state.get("logged_in"):
    # If not logged in, show login page
    login_page()

else:
    # User is logged in, show the main menu
    # here we get the username from the session state
    user = st.session_state["username"]
    
    st.sidebar.title(f"Welcome, {user}!")
    
    menu = ["Dashboard", "Income", "Expense", "Summary"]
    
    
    choice = st.sidebar.radio("What would you like to do?", menu)
    
    
    st.session_state["current_page"] = choice
    
    # Add Logout button
    logout_button() 

    # Page Routing 
    if st.session_state["current_page"] == "Dashboard":
        st.title("📊 Expense Tracker Dashboard")
        st.header(f"Hello, {user}!")
        st.markdown(
            """
            Welcome to your financial dashboard.
Use the left menu to add income, track expenses, and see summaries.
            """
        )

    elif st.session_state["current_page"] == "Income":
        income_page(user)

    elif st.session_state["current_page"] == "Expense":
        expense_page(user)

    elif st.session_state["current_page"] == "Summary":
        summary_page(user)