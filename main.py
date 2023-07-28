from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = 'undersecretary23'  # This is for session management

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.form
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required.'}), 400

    conn = get_db_connection()
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    # Check if the username is already taken
    existing_user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    if existing_user:
        return jsonify({'error': 'Username already taken.'}), 400

    # Insert the new user into the database
    conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password_hash))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Registration successful.'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.form
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required.'}), 400

    conn = get_db_connection()
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    # Check if the username and password match
    user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password_hash)).fetchone()
    conn.close()

    if not user:
        return jsonify({'error': 'Invalid username or password.'}), 401

    # Store the user's id in the session for later use (e.g., for authentication)
    session['user_id'] = user['id']
    return jsonify({'message': 'Login successful.'}), 200

@app.route('/logout')
def logout():
    # Clear the user's session data
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    create_table()
    app.run(debug=True)