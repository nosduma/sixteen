from app import app
import sqlite3



def create_tables():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create the 'users' table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            username TEXT NOT NULL,
            companyname TEXT NOT NULL,
            emailaddress TEXT NOT NULL,
            jobtitle TEXT NOT NULL,
            companyaddress TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Create the 'events' table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            event_date DATE NOT NULL,
            event_time TIME
        )
    ''')


    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
