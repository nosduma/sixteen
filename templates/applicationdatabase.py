import sqlite3

def create_table():
    conn = sqlite3.connect('applications.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY,
            job_title TEXT NOT NULL,
            application_data TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def insert_application(job_title, application_data):
    conn = sqlite3.connect('applications.db')
    cursor = conn.cursor()

    application_json = json.dumps(application_data)
    cursor.execute('''
        INSERT INTO applications (job_title, application_data)
        VALUES (?, ?)
    ''', (job_title, application_json))

    conn.commit()
    conn.close()

def get_application_by_job_title(job_title):
    conn = sqlite3.connect('applications.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT application_data FROM applications WHERE job_title = ?
    ''', (job_title,))

    application_data = cursor.fetchone()
    if application_data:
        application_json = application_data[0]
        application = json.loads(application_json)
        return application

    conn.close()
    return None
