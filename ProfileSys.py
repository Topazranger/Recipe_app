from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

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

# Register Route (POST method)
@app.route('/register', methods=['POST'])
def register():
    data = request.json
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
    
    return jsonify({'message': 'User registered successfully.'})

# Login Route (POST method)
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({'token': access_token, 'user': {'id': user.id, 'username': user.username}})
    return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(debug=True)
