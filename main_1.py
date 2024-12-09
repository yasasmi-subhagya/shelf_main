import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Connect to the database
connection = mysql.connector.connect(
    host="localhost", database="shelf_wise_library", user="root", password=""
)

logged_id = None  # Initialize logged_id as None to indicate no user is logged in

try:
    print("Successful connection!")
    cursor = connection.cursor()
except Error as e:
    print(f"Error: {e}")

# Function to handle the initial options
def option():
    while True:
        print("Choose an option:")
        print("1 - Sign up")
        print("2 - Login")
        print("3 - Exit")
        try:
            choice = int(input("Enter your option: "))
            if choice in [1, 2, 3]:
                return choice
            else:
                print("Invalid choice. Please enter a valid option.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Sign up function
def sign_up():
    user_name = input("Enter your name: ")
    password = input("Enter your password: ")
    query = f"INSERT INTO register(user_name, password) VALUES('{user_name}', '{password}')"
    cursor.execute(query)
    connection.commit()
    print("Sign-up successful!")

# Show menu after successful login
def show_menu():
    while True:
        print("Choose an option:")
        print("1 - Add a member")
        print("2 - Check member list")
        print("3 - Add a new book")
        print("4 - Check book list")
        print("5 - allocate book to a Member")
        print("6 - Exit")
        try:
            choice = int(input("Enter your option: "))
            if choice in [1, 2, 3, 4, 5, 6]:
                return choice
            else:
                print("Invalid choice. Please enter a valid option.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Login function
def login():
    global logged_id
    user_name = input("Enter your name: ")
    password = input("Enter your password: ")
    cursor.execute(f"SELECT * FROM register WHERE user_name = '{user_name}' AND password = '{password}'")
    myresult = cursor.fetchall()

    if len(myresult) == 0:
        print("Invalid credentials. Please try again.")
    else:
        logged_id = myresult[0][0]  # Assuming the ID is in the first column
        print(f"Logged in successfully! User ID: {logged_id}")

# Add a new member
def add_member():
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    address_1 = input("Enter your home number or name: ")
    address_2 = input("Enter your village or lane: ")
    city = input("Enter your city name: ")
    nic = input("Enter your NIC number: ")
    mobile_No = input("Enter your mobile number: ")
    gender = input("Enter your gender: ")
    

    query = f"""INSERT INTO member (f_name, l_name, address_1, address_2, city, NIC, mobile, gender, status)
                VALUES ('{first_name}', '{last_name}', '{address_1}', '{address_2}', '{city}', '{nic}', '{mobile_No}', '{gender}', 'normal')"""
    cursor.execute(query)
    connection.commit()
    print("Member added successfully!")

# Add a new book
def add_book():
    b_name = input("Enter book name: ")
    author = input("Enter author's name: ")
    genre = input("Enter genre: ")
    price = float(input("Enter the price: "))
    no_of_copies = int(input("Enter number of copies: "))
    status = "Available"
    book_type = input("Enter the type: ")

    query = f"""INSERT INTO book (name, author, genre, price, no_of_copies, status, type)
                VALUES ('{b_name}', '{author}', '{genre}', {price}, {no_of_copies}, '{status}', '{book_type}')"""
    cursor.execute(query)
    connection.commit()
    print("Book added successfully!")

# Check member list
def check_member_list():
    cursor.execute("SELECT * FROM member")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

# Check book list
def check_book_list():
    cursor.execute("SELECT * FROM book")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def allocate_book_to_member():
    global logged_id
    
    # Ensure the user is logged in
    if logged_id is None:
        print("Please log in first.")
        return
    check_book_list()
    # Ask for the book ID to be borrowed
    book_id = input("Enter the book ID you want to borrow: ")
    check_member_list()
    mem_id = input("Enter the member ID you want to borrow: ")
    
    # Get the current date for issue_date
    issue_date = datetime.now().date()  # Current date
    
    # Prepare the query to check if the book is available
    cursor.execute(f"SELECT no_of_copies, status FROM book WHERE book_id = '{book_id}'")
    book_data = cursor.fetchone()

    if not book_data:
        print("Book not found.")
        return

    no_of_copies, status = book_data
    if status != "Available":
        print(f"The book is not available for borrowing. Current status: {status}")
        return
    
    if no_of_copies <= 0:
        print("No copies available to borrow.")
        return

   

    # Insert the borrow record into the database
    query = f"""
        INSERT INTO borrow (mem_id, book_id, issue_date, return_date)
        VALUES ('{mem_id}', '{book_id}', '{issue_date}', NULL)
    """
    cursor.execute(query)
    connection.commit()

    # Update the number of copies of the book after the borrow
    new_no_of_copies = no_of_copies - 1
    cursor.execute(f"UPDATE book SET no_of_copies = {new_no_of_copies} WHERE book_id = '{book_id}'")
    connection.commit()

    print(f"Book {book_id} allocated to you successfully! Issue Date: {issue_date}")

# Run the selected option from the menu
def run_menu(choice):
    if choice == 1:
        add_member()
    elif choice == 2:
        check_member_list()
    elif choice == 3:
        add_book()
    elif choice == 4:
        check_book_list()
    elif choice == 5:
        allocate_book_to_member()
    elif choice == 6:
        exit()
    else:
        print("Invalid option. Please try again.")



# Main program loop
while True:
    
    if logged_id is not None:
        menu_choice = show_menu()  # Show menu if the user is logged in
        run_menu(menu_choice)  # Run the selected option
    else:
        response = option()  # Ask for login or sign up if not logged in
        if response == 1:
            sign_up()  # Call sign-up if the user chooses 1
        elif response == 2:
            login()  # Call login if the user chooses 2
        elif response == 3:
            exit()  # Exit if the user chooses 3
            connection.close()
        else:
            print("Please enter a valid number.")
