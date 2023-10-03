import sqlite3

# Create a SQLite database and establish a connection
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Books (
        BookID TEXT PRIMARY KEY,
        Title TEXT,
        Author TEXT,
        ISBN TEXT,
        Status TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        UserID TEXT PRIMARY KEY,
        Name TEXT,
        Email TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Reservations (
        ReservationID TEXT PRIMARY KEY,
        BookID TEXT,
        UserID TEXT,
        ReservationDate TEXT,
        FOREIGN KEY (BookID) REFERENCES Books(BookID),
        FOREIGN KEY (UserID) REFERENCES Users(UserID)
    )
''')

# Function to add a new book to the database
def add_book():
    book_id = input("Enter BookID: ")
    title = input("Enter Title: ")
    author = input("Enter Author: ")
    isbn = input("Enter ISBN: ")
    status = input("Enter Status: ")

    cursor.execute('''
        INSERT INTO Books (BookID, Title, Author, ISBN, Status)
        VALUES (?, ?, ?, ?, ?)
    ''', (book_id, title, author, isbn, status))

    conn.commit()
    print("Book added successfully.")

# Function to find book details based on BookID
def find_book_details(book_id):
    cursor.execute('''
        SELECT Books.Title, Books.Author, Books.ISBN, Users.Name, Users.Email
        FROM Books
        LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
        LEFT JOIN Users ON Reservations.UserID = Users.UserID
        WHERE Books.BookID = ?
    ''', (book_id,))

    result = cursor.fetchone()
    if result:
        title, author, isbn, user_name, user_email = result
        print(f"Title: {title}")
        print(f"Author: {author}")
        print(f"ISBN: {isbn}")
        if user_name and user_email:
            print(f"Reserved by: {user_name} ({user_email})")
        else:
            print("Not reserved.")
    else:
        print("Book not found.")

# Function to check reservation status
def check_reservation_status():
    text = input("Enter BookID, UserID, or ReservationID: ")
    if text.startswith('LB'):
        book_id = text
        find_book_details(book_id)
    elif text.startswith('LU'):
        user_id = text
        cursor.execute('''
            SELECT Books.Title, Books.Author, Users.Name, Users.Email, Reservations.ReservationDate
            FROM Reservations
            LEFT JOIN Books ON Reservations.BookID = Books.BookID
            LEFT JOIN Users ON Reservations.UserID = Users.UserID
            WHERE Users.UserID = ?
        ''', (user_id,))
        result = cursor.fetchall()
        if result:
            for row in result:
                title, author, user_name, user_email, reservation_date = row
                print(f"Title: {title}")
                print(f"Author: {author}")
                print(f"Reserved by: {user_name} ({user_email})")
                print(f"Reservation Date: {reservation_date}")
        else:
            print("No reservations found for this user.")
    elif text.startswith('LR'):
        reservation_id = text
        cursor.execute('''
            SELECT Books.Title, Books.Author, Users.Name, Users.Email, Reservations.ReservationDate
            FROM Reservations
            LEFT JOIN Books ON Reservations.BookID = Books.BookID
            LEFT JOIN Users ON Reservations.UserID = Users.UserID
            WHERE Reservations.ReservationID = ?
        ''', (reservation_id,))
        result = cursor.fetchone()
        if result:
            title, author, user_name, user_email, reservation_date = result
            print(f"Title: {title}")
            print(f"Author: {author}")
            print(f"Reserved by: {user_name} ({user_email})")
            print(f"Reservation Date: {reservation_date}")
        else:
            print("Reservation not found.")
    else:
        title = text
        cursor.execute('''
            SELECT Books.BookID, Books.Author, Users.Name, Users.Email, Reservations.ReservationDate
            FROM Books
            LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
            LEFT JOIN Users ON Reservations.UserID = Users.UserID
            WHERE Books.Title = ?
        ''', (title,))
        result = cursor.fetchall()
        if result:
            for row in result:
                book_id, author, user_name, user_email, reservation_date = row
                print(f"BookID: {book_id}")
                print(f"Author: {author}")
                print(f"Reserved by: {user_name} ({user_email})")
                print(f"Reservation Date: {reservation_date}")
        else:
            print("Book not found.")

# Function to list all books
def list_all_books():
    cursor.execute('''
        SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN, Books.Status,
        Users.UserID, Users.Name, Users.Email,
        Reservations.ReservationID, Reservations.ReservationDate
        FROM Books
        LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
        LEFT JOIN Users ON Reservations.UserID = Users.UserID
    ''')

    result = cursor.fetchall()
    if result:
        for row in result:
            book_id, title, author, isbn, status, user_id, user_name, user_email, reservation_id, reservation_date = row
            print("BookID:", book_id)
            print("Title:", title)
            print("Author:", author)
            print("ISBN:", isbn)
            print("Status:", status)
            if user_id:
                print("Reserved by:", user_name, "(", user_email, ")")
                print("Reservation ID:", reservation_id)
                print("Reservation Date:", reservation_date)
            print("-" * 30)
    else:
        print("No books found in the database.")

# Function to update book details based on BookID
def update_book_details():
    book_id = input("Enter BookID to update: ")
    new_status = input("Enter new status: ")

    cursor.execute('''
        UPDATE Books
        SET Status = ?
        WHERE BookID = ?
    ''', (new_status, book_id))

    conn.commit()

    if cursor.rowcount > 0:
        print("Book details updated successfully.")
    else:
        print("Book not found. Update failed.")

# Function to delete a book based on BookID
def delete_book():
    book_id = input("Enter BookID to delete: ")

    cursor.execute('''
        DELETE FROM Books
        WHERE BookID = ?
    ''', (book_id,))

    cursor.execute('''
        DELETE FROM Reservations
        WHERE BookID = ?
    ''', (book_id,))

    conn.commit()

    if cursor.rowcount > 0:
        print("Book deleted successfully.")
    else:
        print("Book not found. Deletion failed.")

# Main program loop
while True:
    print("\nLibrary Management System")
    print("1. Add a new book")
    print("2. Find book details")
    print("3. Check reservation status")
    print("4. List all books")
    print("5. Update book details")
    print("6. Delete a book")
    print("7. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        add_book()
    elif choice == '2':
        book_id = input("Enter BookID to find details: ")
        find_book_details(book_id)
    elif choice == '3':
        check_reservation_status()
    elif choice == '4':
        list_all_books()
    elif choice == '5':
        update_book_details()
    elif choice == '6':
        delete_book()
    elif choice == '7':
        print("Exiting the program.")
        break
    else:
        print("Invalid choice. Please try again.")

# Close the database connection when done
conn.close()
