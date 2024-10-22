#by Sanjana Medarametla of XII B
import math 
import mysql.connector as my
import random
    
#connecting to mysql
con = my.connect(host = "localhost", user="root", password="Root@123", database="sanjana")
cursor = con.cursor()

#creating table investor
TableUser=('''CREATE TABLE if not exists Investor (
email_id varchar(25) primary key,
name varchar(25),
age int,
gender char(1))''')

#creating table FD
TableFD=('''CREATE TABLE if not exists FD (
fd_slno int AUTO_INCREMENT,
email_id varchar(25) references Investor(email_id),
invested_date varchar(15),
time_period_years int,
invested_amt float,
rateofinterest float,
PRIMARY KEY(fd_slno,email_id))''')

#creating table Stock
TableStock=('''CREATE TABLE if not exists Stock (
stock_slno
int AUTO_INCREMENT,
email_id varchar(25) references Investor(email_id),
invested_date varchar(15),
stock_name varchar(20),
units int,
unit_rate float,
current_rate float,
PRIMARY KEY(stock_slno,email_id))''')

cursor.execute(TableUser)
cursor.execute(TableFD)
cursor.execute(TableStock)
con.commit()

from tkinter import *
import tkinter as tk
from tkinter import messagebox,simpledialog
root = tk.Tk()
root.title("Invest")
root.geometry('500x500')
root.configure(bg='lightblue')

root2 = tk.Tk()
root2.title("Investment Tracker")
root2.geometry('200x200')
root2.configure(bg='lightblue')

askaemail = Label(root,text = "Enter email id: ",bg = "pink").grid(row = 0, column = 0)
email = tk.StringVar() 
e1 = Entry(root, textvariable=email).grid(row = 0, column = 1)

def emailcheck():
    
    from tkinter import messagebox
    import math as m
    import mysql.connector as my
    import random
    id = email.get() # inputing email_id of the user
    email_ids = cursor.execute("SELECT * FROM Investor WHERE email_id='%s' " %(id,))
    global ids
    ids = cursor.fetchone()
    if not ids : # if email_id does not exist in table investor
        name = tk.StringVar()
        nameask = Label(root,text = "Enter name: ").grid(row = 1, column = 0) 
        n = Entry(root, textvariable=name).grid(row = 1, column = 1)
        age = tk.IntVar()
        ageask = Label(root,text = "Enter Age: ").grid(row = 2, column = 0)  
        a = Entry(root, textvariable=age).grid(row = 2,  column = 1)
        gender = tk.StringVar()
        genderask = Label(root,text = "Enter Gender (F) or (M) or (O): ").grid(row = 3, column = 0)  
        g = Entry(root, textvariable=gender).grid(row = 3, column = 1)
        
        def entervalues(id,name,age,gender):
            valuesold = ("INSERT INTO Investor(email_id,name,age,gender) VALUES('{}','{}',{},'{}')".format(id,name,age,gender))
            cursor.execute(valuesold)
            con.commit()
            email_ids = cursor.execute("SELECT * FROM Investor WHERE email_id='%s' " %(id,))
            global ids
            ids = list(cursor.fetchone())
            messagebox.showinfo("Success", "details added to the database")
            investorbutton.grid_forget()

        investorbutton = Button(root,text = "save",command =lambda: entervalues(id, name.get(),age.get(),gender.get()) , activeforeground = "red",activebackground = "pink",pady=10)
        investorbutton.grid(row=4,column=0)
        
    else: # if email_id already exists in table investor
        email_ids = cursor.execute("SELECT * FROM Investor WHERE email_id='%s' " %(id,))
        ids = cursor.fetchone()
        name = ids[1]
        age = ids[2]
        gender = ids[3]
        

    def amt():
        amt = tk.IntVar()
        askamt = Label(root,text = "Enter amount available for all investments:  ",bg = "pink").grid(row = 5, column = 0)        
        e2 = Entry(root, textvariable=amt).grid(row = 5, column = 1)

        def options():
            global balamt
            balamt = amt.get() # declared to keep track of the balance amount after each transaction
            messagebox.showinfo("balance amount", balamt)
            
            def investment(opt):
                def invest_fd():
                    global balamt
                    messagebox.showinfo("Hello", f"You have chosen Fixed Deposit for {id}")

                    # Get the amount from the user using simpledialog
                    amtFD = simpledialog.askinteger("Enter Amount", "Enter amount to be invested:", minvalue=0)
                    if amtFD is None:  # If the user clicks Cancel
                        return

                    if amtFD > balamt:
                        messagebox.showinfo("Invalid Amount", f"Maximum amount: {balamt}")
                        return

                    # Get the time period from the user using simpledialog
                    time = simpledialog.askinteger("Enter Time Period", "Enter the time period (in years):", minvalue=1)
                    if time is None:  # If the user clicks Cancel
                        return

                    else:
                        balamt = round((balamt - amtFD), 2)
                        totalamt = round((amtFD * math.pow(1 + (7 / 100) / 1, 1 * time)), 2)

                        if ids[2] >= 60:
                            seniortotalamt = round((amtFD * math.pow(1 + (8.5 / 100) / 1, 1 * time)), 2)
                            messagebox.showinfo("Investment Details", f"Since you are a senior citizen\nThe total amount after {time} years is {totalamt} based on compound interest at 8.5% per annum compounded annually")
                            messagebox.showinfo("Balance Amount", f"Balance amount: {balamt}")
                            valuesFD = ("INSERT INTO FD(email_id, invested_date, time_period_years, invested_amt, rateofinterest) VALUES('{}', curdate(), {}, {}, {})".format(id, time, amtFD, 8.5))
                            cursor.execute(valuesFD)
                            con.commit()
                            messagebox.showinfo("Success", "Fixed Deposit details added to the database")

                        else:
                            messagebox.showinfo("Investment Details", f"The total amount after {time} years is {totalamt} based on compound interest at 7% per annum compounded annually")
                            messagebox.showinfo("Balance Amount", f"Balance amount: {balamt}")
                            valuesFD = ("INSERT INTO FD(email_id, invested_date, time_period_years, invested_amt, rateofinterest) VALUES('{}', curdate(), {}, {}, {})".format(id, time, amtFD, 7))
                            cursor.execute(valuesFD)
                            con.commit()
                            messagebox.showinfo("Success", "Fixed Deposit details added to the database")
                    
                def invest_stock():
                    global balamt 
                    stock_window = tk.Toplevel(root)
                    stock_window.title("Stock Investment")

                    # Stock data
                    stock_options = ["Asian Paints", "Coal India", "ITC", "Apollo Hospitals", "SBI"]

                    # Create dropdown menu for stock selection
                    stock_var = tk.StringVar()
                    stock_var.set(stock_options[0])  # Default selection
                    stock_label = tk.Label(stock_window, text="Select Stock:")
                    stock_menu = tk.OptionMenu(stock_window, stock_var, *stock_options)
                    stock_label.pack()
                    stock_menu.pack()

                    # Entry for number of units
                    units_var = tk.IntVar()
                    units_label = tk.Label(stock_window, text="Enter number of units:")
                    units_entry = tk.Entry(stock_window, textvariable=units_var)
                    units_label.pack()
                    units_entry.pack()

                    def calculate_investment():
                        global balamt 
                        stock_name = stock_var.get()
                        units = units_var.get()

                        if units <= 0:
                            messagebox.showinfo("Invalid Units", "Please enter a valid number of units.")
                            return

                        # Fetch stock data or use predefined values
                        stock_data = {
                            "Asian Paints": (3343.70, 23.48),
                            "Coal India": (229.71, 68.47),
                            "ITC": (334.11, 25.06),
                            "Apollo Hospitals": (4394.10, 10.88),
                            "SBI": (530.35, 12.33)
                        }

                        if stock_name not in stock_data:
                            messagebox.showinfo("Invalid Stock", "Please select a valid stock.")
                            return

                        current_rate = stock_data[stock_name][0] + random.uniform(-100, 100)
                        total_amt_req = units * current_rate
                        

                        if total_amt_req > balamt:
                            messagebox.showinfo("Invalid Amount", "Maximum amount: {}".format(balamt))
                            return

                        balamt = round((balamt - total_amt_req), 2)
                        messagebox.showinfo("Investment Details", "You have chosen {}\n"
                                                                  "The current unit rate is: {}\n"
                                                                  "The total amount required is: {}\n"
                                                                  "The amount left: {}".format(stock_name, current_rate, round(total_amt_req, 2), balamt))

                        # Insert values into the Stock table
                        values_stock = ("INSERT INTO Stock(email_id, invested_date, stock_name, units, unit_rate, current_rate) VALUES('{}', curdate(), '{}', {}, {}, {})".format(id, stock_name, units, current_rate, current_rate))
                        cursor.execute(values_stock)
                        con.commit()
                        messagebox.showinfo("Success", "Stock details added to the database")
                        
                        messagebox.showinfo("Balance Amount", f"Balance amount: {balamt}")

                    # Button to perform the investment calculation
                    invest_button = tk.Button(stock_window, text="Invest", command=calculate_investment)
                    invest_button.pack()

                    def show_stock_details():
                        stock_details_window = tk.Toplevel(root)
                        stock_details_window.title("Stock Details")

                        stock_name = stock_var.get()

                        # Fetch stock data or use predefined values
                        stock_data = {
                            "Asian Paints": (3343.70, 23.48),
                            "Coal India": (229.71, 68.47),
                            "ITC": (334.11, 25.06),
                            "Apollo Hospitals": (4394.10, 10.88),
                            "SBI": (530.35, 12.33)
                        }

                        if stock_name not in stock_data:
                            messagebox.showinfo("Invalid Stock", "Please select a valid stock.")
                            return

                        current_rate, avg_returns = stock_data[stock_name]

                        details_label = tk.Label(stock_details_window, text="Stock Details for {}".format(stock_name))
                        details_label.pack()

                        details_text = "Current Unit Rate: {}\nAverage Returns: {}".format(current_rate, avg_returns)
                        details_info = tk.Label(stock_details_window, text=details_text)
                        details_info.pack()


                    # Button to show stock details
                    details_button = tk.Button(stock_window, text="Show Stock Details", command=show_stock_details)
                    details_button.pack()



        
                if opt == 'Fixed deposit':
                    invest_fd()
                elif opt == 'Stock':
                    invest_stock()
                elif opt == 'Exit':
                    messagebox.showinfo("Exit", "Thank you!")
                    root.destroy()
                    root2.destroy()

                

            # Dropdown for investment options
            label_options = tk.Label(root, text="Investment options:", bg="pink")
            label_options.grid(row=7, column=0)

            option_var = tk.StringVar()
            options = ['Fixed deposit', 'Stock', 'Exit']
            dropdown_options = tk.OptionMenu(root, option_var, *options, command = investment)
            dropdown_options.grid(row=7, column=1)
            opt = option_var.get()            

            done.grid_forget()

            
        done = Button(root,text = "done",command = options, activeforeground = "red",activebackground = "pink",pady=10)
        done.grid(row=6,column=0)

        
        start.grid_forget()

    start = Button(root,text = "Start investing",command = amt, activeforeground = "red",activebackground = "pink",pady=10)
    start.grid(row=5,column=0)

    emailbutton.grid_forget()

    

emailbutton = Button(root,text = "Submit",command = emailcheck, activeforeground = "red",activebackground = "pink",pady=10)
emailbutton.grid(row=2,column=0)


from tkinter import ttk

def show_investor_table():
    # Fetch data for the inputted email ID from the Investor table
    id = email.get()
    cursor.execute("SELECT * FROM Investor WHERE email_id='%s'" % (id,))
    data = cursor.fetchall()

    # Create a new window to display the table
    table_window = Toplevel(root2)
    table_window.title("Investor Table")

    # Create Treeview widget
    tree = ttk.Treeview(table_window, columns=("Email ID", "Name", "Age", "Gender"), show="headings")
    tree.heading("Email ID", text="Email ID")
    tree.heading("Name", text="Name")
    tree.heading("Age", text="Age")
    tree.heading("Gender", text="Gender")

    # Insert data into the Treeview
    for row in data:
        tree.insert("", "end", values=row)

    # Pack the Treeview
    tree.pack()
        
show_table_button = Button(root2, text="Show Investor Table", command=show_investor_table, activeforeground="red", activebackground="pink", pady=10)
show_table_button.grid(row=0, column=7)

def show_fd_table():
    # Fetch data for the inputted email ID from the FD table
    id = email.get()
    cursor.execute("SELECT * FROM FD WHERE email_id='%s'" % (id,))
    data = cursor.fetchall()

    # Create a new window to display the table
    table_window = Toplevel(root2)
    table_window.title("FD Table")

    # Create Treeview widget
    tree = ttk.Treeview(table_window, columns=("FD Serial No", "Email ID", "Invested Date", "Time Period", "Invested Amount", "Interest Rate"), show="headings")
    tree.heading("FD Serial No", text="FD Serial No")
    tree.heading("Email ID", text="Email ID")
    tree.heading("Invested Date", text="Invested Date")
    tree.heading("Time Period", text="Time Period")
    tree.heading("Invested Amount", text="Invested Amount")
    tree.heading("Interest Rate", text="Interest Rate")

    # Insert data into the Treeview
    for row in data:
        tree.insert("", "end", values=row)

    # Pack the Treeview
    tree.pack()

# Similar function for Stock
def show_stock_table():
    # Fetch data for the inputted email ID from the Stock table
    id = email.get()
    cursor.execute("SELECT * FROM Stock WHERE email_id='%s'" % (id,))
    data = cursor.fetchall()

    # Create a new window to display the table
    table_window = Toplevel(root2)
    table_window.title("Stock Table")

    # Create Treeview widget
    tree = ttk.Treeview(table_window, columns=("Stock Serial No", "Email ID", "Invested Date", "Stock Name", "Units", "Unit Rate", "Current Rate"), show="headings")
    tree.heading("Stock Serial No", text="Stock Serial No")
    tree.heading("Email ID", text="Email ID")
    tree.heading("Invested Date", text="Invested Date")
    tree.heading("Stock Name", text="Stock Name")
    tree.heading("Units", text="Units")
    tree.heading("Unit Rate", text="Unit Rate")
    tree.heading("Current Rate", text="Current Rate")

    # Insert data into the Treeview
    for row in data:
        tree.insert("", "end", values=row)

    # Pack the Treeview
    tree.pack()

show_fd_table_button = Button(root2, text="Show FD Table", command=show_fd_table, activeforeground="red", activebackground="pink", pady=10)
show_fd_table_button.grid(row=1, column=7)

show_stock_table_button = Button(root2, text="Show Stock Table", command=show_stock_table, activeforeground="red", activebackground="pink", pady=10)
show_stock_table_button.grid(row=2, column=7)


root.mainloop()    
root2.mainloop()

