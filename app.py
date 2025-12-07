import sqlite3
import os
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'secure_key_change_in_production'
app.permanent_session_lifetime = timedelta(days=30) # Remember Me duration

# Upload Configuration
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'profile_pics')
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB Limit
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Database Management ---
def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database with all required fields."""
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            profile_pic TEXT DEFAULT NULL,
            last_login TEXT
        )
    ''')
    db.commit()
    db.close()

# Initialize DB immediately
with app.app_context():
    init_db()

# --- Routes ---

@app.route('/')
def home():
    if 'user_id' in session:
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
        conn.close()
        if user:
            return render_template('dashboard.html', user=user)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session: return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = request.form.get('remember') # Checkbox value
        
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            
            # Handle "Remember Me"
            if remember:
                session.permanent = True
            else:
                session.permanent = False
            
            # Update Last Login Time
            try:
                conn = get_db()
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                conn.execute('UPDATE users SET last_login = ? WHERE id = ?', (now, user['id']))
                conn.commit()
            except Exception as e:
                print(f"Error updating last login: {e}")
            finally:
                conn.close()
            
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session: return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm_password']

        if password != confirm:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')

        hashed_pw = generate_password_hash(password)

        try:
            conn = get_db()
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_pw))
            conn.commit()
            conn.close()
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username is already taken.', 'error')
        except Exception as e:
            flash(f'Error: {e}', 'error')

    return render_template('register.html')

@app.route('/upload_pic', methods=['POST'])
def upload_pic():
    if 'user_id' not in session: return redirect(url_for('login'))
    
    file = request.files.get('profile_pic')
    
    if file and file.filename != '' and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Unique Filename: user_ID_TIMESTAMP_name.jpg
        unique_name = f"user_{session['user_id']}_{int(datetime.now().timestamp())}_{filename}"
        
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_name))
        
        conn = get_db()
        conn.execute('UPDATE users SET profile_pic = ? WHERE id = ?', (unique_name, session['user_id']))
        conn.commit()
        conn.close()
        
        flash('Profile picture updated!', 'success')
    else:
        flash('Invalid file or no file selected.', 'error')

    return redirect(url_for('home'))

@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)