from flask import Flask, render_template, request, redirect, session, flash
import pyrebase

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'secret'

# Firebase configuration
config = {
    'apiKey': "AIzaSyAlsCrefGoRe0dicA94sKDWtpzSKDNhz9g",
    'authDomain': "ninerthrifts-12436.firebaseapp.com",
    'databaseURL': "https://ninerthrifts-default-rtdb.firebaseio.com",
    'projectId': "ninerthrifts",
    'storageBucket': "ninerthrifts.appspot.com",
    'messagingSenderId': "451155150098",
    'appId': "1:451155150098:web:03f78ececb145baa1c5fcb",
    'measurementId': "G-J2RNLQ8X3R",
    "databaseURL": ''
}

# Initialize Firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
# -> the database/message

# Routes
@app.route('/')
def index():
    return render_template('login_signup.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        session['user'] = user
        return redirect('/dashboard')
    except:
        flash('Invalid email or password. Please try again.')
        return redirect('/')

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    password = request.form['password']
    
    try:
        user = auth.create_user(email=email, password=password)
        session['user'] = user
        return redirect('/dashboard')
    except:
        flash('An account with this email already exists. Please use a different email.')
        return redirect('/')

@app.route('/dashboard')
def dashboard():
    user = session.get('user')
    if user:
        user_email = user['email']
        return render_template('dashboard.html', user_email=user_email)
    else:
        return redirect('/')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/update_account', methods=['POST'])
def update_account():
    email = request.form['email']
    password = request.form['password']
    
    # Update user's login information here (e.g., update database)
    # Example code:
    # user = auth.current_user
    # user.update_email(email)
    # user.update_password(password)

    flash('Your login information has been updated successfully', 'success')
    return redirect('/account')

if __name__ == '__main__':
    app.run(debug=True)
