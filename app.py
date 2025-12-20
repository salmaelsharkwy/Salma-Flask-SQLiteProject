import sqlite3
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'secure_key_change_in_production'
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'profile_pics')
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    db = get_db()
    db.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE,
        password TEXT NOT NULL,
        profile_pic TEXT DEFAULT NULL,
        last_login TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    db.execute('''CREATE TABLE IF NOT EXISTS activity_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        action TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    db.commit()
    db.close()

with app.app_context():
    init_db()

def log_activity(user_id, action):
    db = get_db()
    db.execute('INSERT INTO activity_log (user_id, action, timestamp) VALUES (?, ?, ?)',
               (user_id, action, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    db.commit()
    db.close()

@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    db.close()
    if user:
        return render_template('dashboard.html', user=user)
    session.clear()
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['login_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db.execute('UPDATE users SET last_login = ? WHERE id = ?', (now, user['id']))
            db.commit()
            db.close()
            log_activity(user['id'], 'Logged in')
            return redirect(url_for('home'))
        db.close()
        flash('Invalid username or password.', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form['username']
        email = request.form.get('email', '')
        password = request.form['password']
        confirm = request.form['confirm_password']
        if password != confirm:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
        hashed_pw = generate_password_hash(password)
        try:
            db = get_db()
            db.execute('INSERT INTO users (username, email, password, created_at) VALUES (?, ?, ?, ?)',
                      (username, email, hashed_pw, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            db.commit()
            user_id = db.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()['id']
            db.close()
            log_activity(user_id, 'Account created')
            flash('Account created! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username or email already taken.', 'error')
        except Exception as e:
            flash(f'Error: {e}', 'error')
    return render_template('register.html')

@app.route('/upload_pic', methods=['POST'])
def upload_pic():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    file = request.files.get('profile_pic')
    if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}:
        filename = secure_filename(file.filename)
        unique_name = f"user_{session['user_id']}_{int(datetime.now().timestamp())}_{filename}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_name))
        db = get_db()
        db.execute('UPDATE users SET profile_pic = ? WHERE id = ?', (unique_name, session['user_id']))
        db.commit()
        db.close()
        log_activity(session['user_id'], 'Updated profile picture')
        flash('Profile picture updated!', 'success')
    return redirect(url_for('home'))

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    logs = db.execute('SELECT * FROM activity_log WHERE user_id = ? ORDER BY timestamp DESC LIMIT 15',
                      (session['user_id'],)).fetchall()
    total_actions = db.execute('SELECT COUNT(*) as count FROM activity_log WHERE user_id = ?',
                               (session['user_id'],)).fetchone()['count']
    
    login_time = session.get('login_time', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    session_minutes = int((datetime.now() - datetime.strptime(login_time, "%Y-%m-%d %H:%M:%S")).seconds / 60)
    
    db.close()
    return render_template('profile.html', user=user, logs=logs, total_actions=total_actions, 
                         session_minutes=session_minutes)

@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    new_username = request.form.get('username')
    new_email = request.form.get('email')
    try:
        db = get_db()
        if new_username:
            db.execute('UPDATE users SET username = ? WHERE id = ?', (new_username, session['user_id']))
        if new_email:
            db.execute('UPDATE users SET email = ? WHERE id = ?', (new_email, session['user_id']))
        db.commit()
        db.close()
        log_activity(session['user_id'], 'Updated profile information')
        flash('Profile updated successfully', 'success')
    except sqlite3.IntegrityError:
        flash('Username or email already taken', 'error')
    return redirect(url_for('profile'))

@app.route('/clear_activity')
def clear_activity():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db = get_db()
    db.execute('DELETE FROM activity_log WHERE user_id = ?', (session['user_id'],))
    db.commit()
    db.close()
    log_activity(session['user_id'], 'Cleared activity history')
    flash('Activity history cleared', 'success')
    return redirect(url_for('profile'))

@app.route('/delete_account')
def delete_account():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db = get_db()
    db.execute('DELETE FROM activity_log WHERE user_id = ?', (session['user_id'],))
    db.execute('DELETE FROM users WHERE id = ?', (session['user_id'],))
    db.commit()
    db.close()
    session.clear()
    flash('Account deleted successfully', 'success')
    return redirect(url_for('login'))

@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/logout')
def logout():
    if 'user_id' in session:
        log_activity(session['user_id'], 'Logged out')
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
