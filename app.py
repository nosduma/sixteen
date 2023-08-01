from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key in a real application

# Dummy user and post data (for demonstration purposes)
users = {
    'user1': {
        'username': 'user1',
        'password': generate_password_hash('password1')  # Use generate_password_hash to securely store passwords
    }
}

posts = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users:
            return render_template('register.html', message='Username already taken.')

        users[username] = {
            'username': username,
            'password': generate_password_hash(password)
        }
        session['username'] = username
        return redirect(url_for('dashboard'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username not in users or not check_password_hash(users[username]['password'], password):
            return render_template('login.html', message='Invalid username or password.')

        session['username'] = username
        return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'], posts=posts)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/post', methods=['POST'])
def post():
    if 'username' in session:
        post_text = request.form['post']
        posts.append({'author': session['username'], 'text': post_text})
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()











