from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        username = request.form['username']
        companyname = request.form['companyname']
        emailaddress = request.form['emailaddress']
        jobtitle = request.form['jobtitle']
        companyaddress = request.form['companyaddress']
        password = request.form['password']

        # Hash the password before storing it
        password_hash = generate_password_hash(password)

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users (fullname, username, companyname, emailaddress, jobtitle, companyaddress, password) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (fullname, username, companyname, emailaddress, jobtitle, companyaddress, password_hash))
        conn.commit()

        conn.close()
        return redirect(url_for('login'))

    return render_template('register.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username COLLATE NOCASE=?", (username,))
        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(user[7], password):
            session['username'] = user[2]  # Store the username in the session
            flash('Login successful', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed', 'error')

    return render_template('login.html')



@app.route('/dashboard')
def dashboard():
    if 'username' in session:  # Check if username is in the session
        username = session['username']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username COLLATE NOCASE = ?", (username,))
        user = cursor.fetchone()

        conn.close()

        if user:
            return render_template('dashboard.html', username=username, user=user)
        else:
            return "User not found."
    else:
        return redirect(url_for('login'))



@app.route('/diary', methods=['GET', 'POST'])
def diary():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        event_date = request.form['event_date']
        event_time = request.form['event_time']

        # Insert the event into the database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO events (title, description, event_date, event_time) VALUES (?, ?, ?, ?)",
                       (title, description, event_date, event_time))
        conn.commit()
        conn.close()

        flash('Event added successfully', 'success')

    return render_template('diary.html')

@app.route('/create_event', methods=['POST'])
def create_event():
    if request.method == 'POST':
        # Retrieve event data from the form
        title = request.form['title']
        description = request.form['description']
        event_date = request.form['event_date']
        event_time = request.form['event_time']

        # Get the current user's username from the session
        username = session.get('username')

        # Fetch the user's ID (id) from the database based on their username
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username COLLATE NOCASE = ?", (username,))
        user = cursor.fetchone()

        if user:
            user_id = user[0]  # Extract the user_id (id) from the query result

            # Create a connection to the SQLite database
            cursor.execute("INSERT INTO events (username, title, description, event_date, event_time) VALUES (?, ?, ?, ?, ?)",
                           (username, title, description, event_date, event_time))

            # Commit the changes and close the database connection
            conn.commit()
            conn.close()

            flash('Event created successfully!', 'success')
            return redirect(url_for('events'))  # Redirect to events after creating the event
        else:
            flash('User not found', 'error')

    flash('Please log in to create events.', 'error')
    return redirect(url_for('login'))


@app.route('/events', methods=['GET'])
def events():
    if 'username' in session:  # Check if the user is already logged in
        # Get the username of the currently logged-in user
        username = session['username']
        
        # Create a connection to the SQLite database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Execute an SQL query to retrieve events associated with the current user
        cursor.execute("SELECT title, description, event_date, event_time FROM events WHERE username COLLATE NOCASE = ?", (username,))
        
        # Fetch all events from the cursor
        events = cursor.fetchall()

        # Close the database connection
        conn.close()

        return render_template('events.html', events=events)
    else:
        flash('Please log in to access the events.', 'error')
        return redirect(url_for('login', next='events'))




@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
