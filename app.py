from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key in a real application

# Dummy user data (for demonstration purposes)
users = {
    'user1': {
        'username': 'user1',
        'password': 'password1'
    }
}

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
        return redirect(url_for('login'))  # Redirect to login page after successful registration

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))  # Redirect to dashboard after successful login
        else:
            return render_template('login.html', message='Invalid username or password.')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/vacancies')
def vacancies():
    return render_template('vacancies.html')

@app.route('/applicants')
def applicants():
    return render_template('applicants.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/new_applicants')
def new_applicants():
    return render_template('new_applicants.html')

@app.route('/job_openings')
def job_openings():
    return render_template('job_openings.html')

@app.route('/event')
def event():
    return render_template('event.html')  # You should customize this page to show event details

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
