from flask import Flask, render_template, request, redirect, session, url_for, flash
from config import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # for session management

# Route for user login - This will be the default route when users access the app
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Connect to the MySQL database to check the user credentials
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user[4], password):  # If user exists and password matches
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            return redirect('/purchase')  # Redirect to the ticket purchase system after login
        else:
            flash('Invalid credentials, please try again.')  # Show error if login fails
    
    return render_template('login.html')

# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = generate_password_hash(request.form['password'])  # Hash the password for security
        
        # Insert the new user into the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name, email, phone, password) VALUES (%s, %s, %s, %s)',
                       (name, email, phone, password))
        conn.commit()
        conn.close()
        
        return redirect('/login')  # After registration, redirect to the login page
    return render_template('register.html')

# Route for ticket purchase system
@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    if 'user_id' not in session:
        return redirect('/login')  # If the user is not logged in, redirect to the login page
    
    if request.method == 'POST':
        event = request.form['event']
        seat_type = request.form['seat_type']
        train_no=request.form['train_no']
        train_time=request.form['train_time']
       
        user_id = session['user_id']
        
        # Insert the purchase details into the tickets table
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tickets (user_id, event, seat_type,train_no,train_time) VALUES (%s, %s, %s,%s,%s)',
                       (user_id, event, seat_type,train_no,train_time))
        conn.commit()
        conn.close()
        
        return redirect('/')  # Redirect to home or confirmation page after purchase
    
    return render_template('purchase.html')

# Route for logging out
@app.route('/logout')
def logout():
    session.clear()  # Clear the session to log the user out
    return redirect('/login')  # Redirect to the login page after logout

if __name__ == '__main__':
    app.run(debug=True)
