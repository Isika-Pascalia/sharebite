from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config, get_db_connection, init_database
import mysql.connector

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

# Initialize database when app starts
init_database()

@app.route('/')
def index():
    """Homepage - Display all available food donations"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Get all unclaimed food donations with donor username
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
        flash(f'Error loading food items: {str(e)}', 'error')
        return render_template('index.html', food_items=[])

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Hash the password for security
        hashed_password = generate_password_hash(password)
        
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            # Insert new user
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            
            # Find user by username
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            
            cursor.close()
            connection.close()
            
            if user and check_password_hash(user['password'], password):
                # Login successful
                session['user_id'] = user['id']
                session['username'] = user['username']
                flash('Login successful!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password!', 'error')
                
        except Exception as e:
            flash(f'Login failed: {str(e)}', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/donate', methods=['GET', 'POST'])
def donate():
    """Food donation form"""
    # Check if user is logged in
    if 'user_id' not in session:
        flash('Please log in to donate food.', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        food_name = request.form['food_name']
        quantity = request.form['quantity']
        location = request.form['location']
        contact_info = request.form['contact_info']
        donor_id = session['user_id']
        
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            # Insert new food donation
            cursor.execute("""
                INSERT INTO food_donations (food_name, quantity, location, contact_info, donor_id)
                VALUES (%s, %s, %s, %s, %s)
            """, (food_name, quantity, location, contact_info, donor_id))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            flash('Food donation posted successfully!', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            flash(f'Error posting donation: {str(e)}', 'error')
    
    return render_template('donate.html')

@app.route('/claim/<int:food_id>', methods=['POST'])
def claim_food(food_id):
    """Claim a food donation"""
    # Check if user is logged in
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please log in to claim food.'})
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Check if food is still available
        cursor.execute("SELECT is_claimed FROM food_donations WHERE id = %s", (food_id,))
        result = cursor.fetchone()
        
        if result and not result[0]:  # If not claimed
            # Mark as claimed
            cursor.execute("""
                UPDATE food_donations 
                SET is_claimed = TRUE, claimed_by = %s 
                WHERE id = %s
            """, (session['user_id'], food_id))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            return jsonify({'success': True, 'message': 'Food claimed successfully!'})
        else:
            cursor.close()
            connection.close()
            return jsonify({'success': False, 'message': 'Food is no longer available.'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error claiming food: {str(e)}'})

@app.route('/api/search')
def search_food():
    """API endpoint for searching/filtering food"""
    search_term = request.args.get('search', '').lower()
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        if search_term:
            # Search in food name and location
            cursor.execute("""
                SELECT fd.*, u.username as donor_name 
                FROM food_donations fd 
                JOIN users u ON fd.donor_id = u.id 
                WHERE fd.is_claimed = FALSE 
                AND (LOWER(fd.food_name) LIKE %s OR LOWER(fd.location) LIKE %s)
                ORDER BY fd.created_at DESC
            """, (f'%{search_term}%', f'%{search_term}%'))
        else:
            # Return all unclaimed food
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
        
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)