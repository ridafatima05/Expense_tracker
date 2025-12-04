📘 Expense Tracker (Excel Version)
A simple Expense Tracker App built with Python and Streamlit that lets you add, save, and view your daily expenses using an Excel file (expenses.xlsx).

✨ Features
Add new expenses (date, category, amount, description)
View all expenses in a clean table
Data saved automatically in Excel
Simple and beginner-friendly UI
Runs in the browser

🛠 Technologies Used
Python 3.11+
Streamlit (used for create web apps)
Pandas (for data handling)
OpenPyXL (for Excel saving)

Running on Streamlit Cloud: 
Push your repository to GitHub.
Go to Streamlit Cloud
 → Click New App → Connect your GitHub repo.
Set Main file path:
expense_tracker/app.py

Deploy. Streamlit will automatically install dependencies.
Make sure your repository includes a requirements.txt with the dependencies:
streamlit
pandas
openpyxl
matplotlib
Once deployed, open the app link, register a user, and start tracking your expenses!

📂 Data Storage
All expense data is stored in:
expenses.xlsx
Category data is stored in category.xlsx
users data stored in users.xlsx
income data is stored in income.xlsx.
The file is automatically created if it doesn’t exist.

Usage:
Login or Register a user
Add categories for expenses
Add income and expenses
View reports and graphs in the Summary page
Logout to switch users

Installation
1. Clone the Project
git clone https://github.com/yourusername/expense-tracker.git
cd expense-tracker

2. Install Dependencies
pip install streamlit pandas openpyxl

How to Run the App
streamlit run app.py

Open in your browser:
http://localhost:8501
🤝 Contributing
Feel free to open issues or submit pull requests to improve the app.

📜 License
This project is free to use for learning and personal projects.

Notes
Data is stored in local Excel files inside the data/ folder.
Refreshing the page may reset the session; data is preserved.
-----------------------------------------------------------------
Team Leader : Rida Fatima 
Team Members:
Yumna , Haniya and Hussain.

Thankyou!
