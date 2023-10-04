from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from flask import Flask, jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key in a real application

# Dummy user data (for demonstration purposes)
users = {
    'user1': {
        'username': 'user1',
        'password': 'password1'
    }
}

# Define a function to create the events table
def create_table():
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

# Function to get events from the database
def get_events():
    conn = sqlite3.connect('calendar.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM events')
    events = cursor.fetchall()
    conn.close()
    return events

@app.route('/get_events', methods=['GET'])
def fetch_events():
    # Retrieve events from your database or source
    events = get_events()

    # Convert events to a JSON response using jsonify
    response = jsonify(events=events)
    
    return response

def insert_event(event_name, event_date, event_description):
    conn = sqlite3.connect('calendar.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO events (event_name, event_date, event_description) VALUES (?, ?, ?)',
                   (event_name, event_date, event_description))
    conn.commit()
    conn.close()

@app.route('/add_event', methods=['POST'])
def add_event_route():
    if request.method == 'POST':
        event_name = request.form['event_name']
        event_date = request.form['event_date']
        event_description = request.form['event_description']
        insert_event(event_name, event_date, event_description)  # Call the renamed function
        return redirect(url_for('event'))



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users:
            return render_template('register.html', message='Username already taken.')

        users[username] = {
            'username': username,
            'password': password
        }
        session['username'] = username
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', message='Invalid username or password.')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        # Retrieve events from the database
        events = get_events()
        return render_template('dashboard.html', username=session['username'], events=events)
    return redirect(url_for('login'))



@app.route('/vacancies')
def vacancies():
    return render_template('vacancies.html')

@app.route('/applicants')
def applicants():
    return render_template('applicants.html')

@app.route('/calendar')
def calendar():
    # You can create and populate the weekly calendar data here
    # For simplicity, let's assume you have a list of events for the week

    # Sample weekly events data (replace with your actual data)
    weekly_events = [
        ['Event 1', '2023-10-10', 'Description 1'],
        ['Event 2', '2023-10-11', 'Description 2'],
        # Add more events for the week
    ]

    return render_template('calendar.html', weekly_events=weekly_events)

@app.route('/new_applicants')
def new_applicants():
    return render_template('new_applicants.html')

@app.route('/job_openings')
def job_openings():
    return render_template('job_openings.html')

@app.route('/events')
def event():
    return render_template('events.html')  # You should customize this page to show event details

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
