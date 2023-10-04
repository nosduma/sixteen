import sqlite3

def create_database():
    conn = sqlite3.connect('calendar.db')
    cursor = conn.cursor()

    # Create a table to store calendar events
    cursor.execute('''CREATE TABLE IF NOT EXISTS events
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       event_name TEXT,
                       event_date DATE,
                       event_description TEXT)''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
