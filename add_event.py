import sqlite3

def add_event(event_name, event_date, event_description):
    conn = sqlite3.connect('calendar.db')
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO events (event_name, event_date, event_description)
                      VALUES (?, ?, ?)''', (event_name, event_date, event_description))

    conn.commit()
    conn.close()

# Example: Insert an event
add_event('Meeting', '2023-10-15', 'Discuss project')
