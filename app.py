from flask import Flask, request, render_template, redirect, url_for
from werkzeug.security import generate_password_hash
import pyodbc

app = Flask(__name__)
app.config['SQL_SERVER'] = 'IRIS\\SQLEXPRESS'
app.config['SQL_DATABASE'] = 'userdatabase'

 

def create_connection():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        f'SERVER={app.config["SQL_SERVER"]};'
        f'DATABASE={app.config["SQL_DATABASE"]};'
        'Trusted_Connection=yes;'
  
    )

@app.route('/', methods=['GET', 'POST'])
def start():
    return redirect(url_for('signup'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Hash password (you should import generate_password_hash from werkzeug.security)
        # hashed_password = generate_password_hash(password)
  # Hash password
        hashed_password =         generate_password_hash(password)
        # Insert data into the database
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                       (username, email, hashed_password))
        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('home'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']

        # Query the database for the user
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", 
                       (username, password))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user:
            # User authenticated, redirect to home page
            return redirect(url_for('home'))
        else:
            # Invalid credentials, show error message
            error = 'Invalid username or password'
            return render_template('login.html', error=error)

    return render_template('login.html')


@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
