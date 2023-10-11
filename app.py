from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import hashlib
from database import create_tables  # Import the create_tables function



app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key in a real application

# # Dummy user data (for demonstration purposes)
# users = {
#     'user1': {
#         'username': 'user1',
#         'password': 'password1'
#     }
# }

import sqlite3
from database import create_tables
def create_table():
    conn = sqlite3.connect('calendar.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS events
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       event_name TEXT,
                       event_date DATE,
                       event_description TEXT)''')

    conn.commit()
    conn.close()


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        username = request.form['username']
        companyname = request.form['companyname']
        emailaddress = request.form['emailaddress']
        jobtitle = request.form['jobtitle']
        companyaddress = request.form['companyaddress']
        
        # Define 'password' and 'confirm_password' variables by extracting them from the form data
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match', 'error')
        else:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            conn = get_db_connection()
            
            # Create the 'users' table if it doesn't exist
            create_tables()
            
            conn.execute('INSERT INTO users (fullname, username, companyname, emailaddress, jobtitle, companyaddress, password_hash) VALUES (?, ?, ?, ?, ?, ?, ?)',
                         (fullname, username, companyname, emailaddress, jobtitle, companyaddress, password_hash))
            conn.commit()
            conn.close()
            flash('Registration successful!', 'success')

            return redirect(url_for('login'))

    return render_template('register.html')



# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        password_hash = hashlib.sha256(password.encode()).hexdigest()
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password_hash = ?', (username, password_hash)).fetchone()
        conn.close()

        if user:
            flash('Login successful!', 'success')
            session['user_id'] = user['id']  # Store the user's ID in the session
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Check if the user is logged in
    if 'user_id' not in session:
        flash('You must log in first.', 'danger')
        return redirect(url_for('login'))

    # Render the dashboard template
    return render_template('dashboard.html')

def create_table():
    conn = sqlite3.connect('calendar.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS events
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       event_name TEXT,
                       event_date DATE,
                       event_description TEXT)''')

    conn.commit()
    conn.close()

create_table()

def get_db_connection():
    if 'user_id' in session:
        user_id = session['user_id']
        db_name = f'user_{user_id}_db.sqlite'  # Unique database name for each user
        conn = sqlite3.connect(db_name)
        conn.row_factory = sqlite3.Row
        return conn
    else:
        return None


@app.route('/add_event', methods=['POST'])
def add_event():
    if request.method == 'POST':
        event_name = request.form['event_name']
        event_date = request.form['event_date']
        event_description = request.form['event_description']

        conn = sqlite3.connect('calendar.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO events (event_name, event_date, event_description) VALUES (?, ?, ?)',
                       (event_name, event_date, event_description))
        conn.commit()
        conn.close()

        flash('Event added successfully!', 'success')

    return redirect(url_for('index'))

# Define event_css_class function
def event_css_class(event):
    if event[3] == 'SomeCondition':
        return 'conditional-class'
    else:
        return 'default-class'

# Function to get events from the database with pagination
def get_events(page, per_page):
    conn = sqlite3.connect('calendar.db')
    cursor = conn.cursor()

    offset = (page - 1) * per_page

    cursor.execute('SELECT * FROM events LIMIT ? OFFSET ?', (per_page, offset))
    events = cursor.fetchall()
    
    conn.close()
    return events

# In your route, make sure it's available in the context when rendering the template
@app.route('/events')
def events():
    # Retrieve events from the database
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of events per page

    events = get_events(page, per_page)
    return render_template('events.html', events=events, event_css_class=event_css_class, page=page)

@app.route('/diary')
def diary():
    return render_template('diary.html')


@app.route('/vacancies')
def vacancies():
    return render_template('vacancies.html')

@app.route('/applicants')
def applicants():
    return render_template('applicants.html')

@app.route('/new_applicants')
def new_applicants():
    return render_template('new_applicants.html')

@app.route('/job_openings')
def job_openings():
    return render_template('job_openings.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)