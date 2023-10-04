def update_event(event_id, event_name, event_date, event_description):
    conn = sqlite3.connect('calendar.db')
    cursor = conn.cursor()

    cursor.execute('''UPDATE events
                      SET event_name=?, event_date=?, event_description=?
                      WHERE id=?''', (event_name, event_date, event_description, event_id))

    conn.commit()
    conn.close()

def delete_event(event_id):
    conn = sqlite3.connect('calendar.db')
    cursor = conn.cursor()

    cursor.execute('''DELETE FROM events WHERE id=?''', (event_id,))

    conn.commit()
    conn.close()
