from database import create_tables  # Import your create_tables function from database.py
from app import app, create_tables  # Import your Flask app and create_tables function
import sqlite3


def create_tables():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create the 'users' table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT,
        username TEXT,
        companyname TEXT,
        emailaddress TEXT,
        jobtitle TEXT,
        companyaddress TEXT,
        password_hash TEXT
    )''')

    # Create other tables if needed

    conn.commit()
    conn.close()



if __name__ == '__main':
    create_tables()  # Call the function to create tables
    app.run(debug=True)

