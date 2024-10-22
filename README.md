# Investment Tracker

## Description
The **Investment Tracker** is a desktop-based application built using Python's Tkinter library, along with MySQL for database management. The application allows users to manage and track their investments in Fixed Deposits (FD) and Stocks. It enables users to enter their personal details, invest in various financial instruments, and view their investment history. This project also includes features such as dynamic balance management and real-time data storage.

## Features
- **User Registration**: Allows new users to enter their details, including email, name, age, and gender.
- **Investment Options**: Users can invest in Fixed Deposits or Stocks.
  - **Fixed Deposits**: Users can input investment amount, time period, and get compound interest calculated based on predefined interest rates (7% for general users and 8.5% for senior citizens).
  - **Stocks**: Users can invest in selected stocks like Asian Paints, Coal India, ITC, Apollo Hospitals, and SBI. The stock prices are dynamically fetched and adjusted.
- **Balance Tracking**: Tracks the available balance after each investment, ensuring the user does not invest more than the available funds.
- **Database Integration**: All user and investment data is stored in a MySQL database, enabling easy retrieval and manipulation.
- **Tables**: Users can view their personal information, Fixed Deposit details, and Stock investment history in organized tables using Tkinter’s Treeview widget.

## Technologies Used
- **Python**: Main programming language for logic and GUI.
- **Tkinter**: Used for creating the graphical user interface.
- **MySQL**: Used to store and manage user and investment data.
- **Random**: Used to simulate the stock market by varying stock prices.
- **Math**: Used for calculating compound interest for Fixed Deposits.

## Database Schema
1. **Investor Table**:
   - `email_id` (Primary Key)
   - `name`
   - `age`
   - `gender`

2. **FD Table**:
   - `fd_slno` (Auto Increment, Primary Key)
   - `email_id` (Foreign Key referencing `Investor`)
   - `invested_date`
   - `time_period_years`
   - `invested_amt`
   - `rateofinterest`

3. **Stock Table**:
   - `stock_slno` (Auto Increment, Primary Key)
   - `email_id` (Foreign Key referencing `Investor`)
   - `invested_date`
   - `stock_name`
   - `units`
   - `unit_rate`
   - `current_rate`

## How to Use
1. **Initial Setup**:
   - Install the required packages (`mysql-connector-python`, `Tkinter`).
   - Set up a MySQL database and update the connection credentials in the script (`host`, `user`, `password`, `database`).

2. **Running the Application**:
   - Run the Python script to open the main investment window.
   - Enter your email ID to start.
   - If the email ID exists, the user data is fetched from the database; otherwise, new user details will be requested.
   - Choose an investment option (Fixed Deposit or Stock) and follow the prompts to invest.
   - Check the "Investor", "FD", or "Stock" tables to view investment details.

3. **Data Viewing**:
   - View user information in the "Investor Table".
   - View Fixed Deposit history in the "FD Table".
   - View Stock investment history in the "Stock Table".

## Prerequisites
- **Python 3.x**
- **MySQL**
- Required Python packages:
  ```bash
  pip install mysql-connector-python
  ```

## Getting Started

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/investment-tracker.git
   ```
2. Set up the MySQL database:
   - Create a new database named `sanjana`.
   - Run the SQL queries within the script to create the tables.
   
3. Modify the MySQL connection credentials in the script to match your local setup:
   ```python
   con = my.connect(host="localhost", user="root", password="Root@123", database="sanjana")
   ```

4. Run the Python script:
   ```bash
   python investment_tracker.py
   ```
