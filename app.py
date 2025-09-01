from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config, get_db_connection, init_database
import mysql.connector

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

# Initialize database tables when app starts
init_database()

# -------------------------
# HOME ROUTE
# -------------------------
@app.route('/')
def index():
    """Homepage - Show available food donations"""
    try:
        connection = get_db_connection()
        if not connection:
            flash("Database connection failed!", "error")
            return render_template("index.html", food_items=[])
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT fd.*, u.username as donor_name 
            FROM food_donations fd 
            JOIN users u ON fd.donor_id = u.id 
            WHERE fd.is_claimed = FALSE 
            ORDER BY fd.created_at DESC
        """)
        food_items = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('index.html', food_items=food_items)
    except Exception as e:
        flash(f"Error loading food items: {e}", "error")
        return render_template('index.html', food_items=[])

# -------------------------
# REGISTER ROUTE
# -------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        connection = get_db_connection()
        if not connection:
            flash("Database connection failed!", "error")
            return redirect(url_for('register'))

        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, hashed_password)
            )
            connection.commit()
            cursor.close()
            connection.close()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except mysql.connector.IntegrityError:
            flash('Username or email already exists!', 'error')
        except Exception as e:
            flash(f'Registration failed: {str(e)}', 'error')
    return render_template('register.html')

# -------------------------
# LOGIN ROUTE
# -------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = get_db_connection()
        if not connection:
            flash("Database connection failed!", "error")
            return redirect(url_for('login'))

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash("Login successful!", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password!", "error")
    return render_template('login.html')

# -------------------------
# LOGOUT ROUTE
# -------------------------
@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('index'))

# -------------------------
# DONATE FOOD ROUTE
# -------------------------
@app.route('/donate', methods=['GET', 'POST'])
def donate():
    if 'user_id' not in session:
        flash("Please log in to donate.", "error")
        return redirect(url_for('login'))

    if request.method == 'POST':
        food_name = request.form['food_name']
        quantity = request.form['quantity']
        location = request.form['location']
        contact_info = request.form['contact_info']
        donor_id = session['user_id']

        connection = get_db_connection()
        if not connection:
            flash("Database connection failed!", "error")
            return redirect(url_for('donate'))

        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO food_donations (food_name, quantity, location, contact_info, donor_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (food_name, quantity, location, contact_info, donor_id))
        connection.commit()
        cursor.close()
        connection.close()
        flash("Food donation posted successfully!", "success")
        return redirect(url_for('index'))
    return render_template('donate.html')

# -------------------------
# CLAIM FOOD ROUTE
# -------------------------
@app.route('/claim/<int:food_id>', methods=['POST'])
def claim_food(food_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please log in to claim food.'})

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT is_claimed FROM food_donations WHERE id=%s", (food_id,))
    result = cursor.fetchone()

    if result and not result[0]:
        cursor.execute("""
            UPDATE food_donations SET is_claimed=TRUE, claimed_by=%s WHERE id=%s
        """, (session['user_id'], food_id))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'success': True, 'message': 'Food claimed successfully!'})
    else:
        cursor.close()
        connection.close()
        return jsonify({'success': False, 'message': 'Food is no longer available.'})

# -------------------------
# SEARCH FOOD API
# -------------------------
@app.route('/api/search')
def search_food():
    search_term = request.args.get('search', '').lower()
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if search_term:
        cursor.execute("""
            SELECT fd.*, u.username as donor_name 
            FROM food_donations fd 
            JOIN users u ON fd.donor_id = u.id 
            WHERE fd.is_claimed = FALSE 
            AND (LOWER(fd.food_name) LIKE %s OR LOWER(fd.location) LIKE %s)
            ORDER BY fd.created_at DESC
        """, (f'%{search_term}%', f'%{search_term}%'))
    else:
        cursor.execute("""
            SELECT fd.*, u.username as donor_name 
            FROM food_donations fd 
            JOIN users u ON fd.donor_id = u.id 
            WHERE fd.is_claimed = FALSE 
            ORDER BY fd.created_at DESC
        """)

    food_items = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(food_items)

if __name__ == '__main__':
    app.run(debug=True)
