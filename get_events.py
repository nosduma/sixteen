import sqlite3

def get_events(start_date, end_date):
    conn = sqlite3.connect('calendar.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM events
                      WHERE event_date BETWEEN ? AND ?''', (start_date, end_date))

    events = cursor.fetchall()
    conn.close()
    return events

# Example: Get events for a specific date range
events = get_events('2023-10-10', '2023-10-20')
for event in events:
    print(event)
