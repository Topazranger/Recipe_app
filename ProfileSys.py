from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '101010'
app.secret_key = '432870401928473086574'


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# User table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Create db Tables
with app.app_context():
    db.create_all()

# Serve HTML Page
@app.route('/')
def index():
    return render_template('userCreate.html')

# Register Route
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    # Check if passwords match
    if data['password'] != data['RepeatPassword']:
        return jsonify({'message': 'Passwords do not match.'}), 400
    
    # Check if the user already exists
    user_exists = User.query.filter_by(username=data['username']).first()
    if user_exists:
        return jsonify({'message': 'Username already exists.'}), 400
    
    # Hash the password before storing it
    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    # Create a new user in the database
    new_user = User(username=data['username'], password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'User registered successfully.'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        # Set session values
        session['user_id'] = user.id
        session['username'] = user.username
        return jsonify({'success': True, 'message': 'Login successful'})
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@app.route('/mainmenu')
def mainmenu():
    if 'username' not in session:
        return redirect('/')
    username = session['username']
    return render_template('MainMenu.html', username=username)


if __name__ == '__main__':
    app.run(debug=True)
