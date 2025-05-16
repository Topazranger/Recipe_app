from flask import Flask, request, jsonify, render_template, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '432870401928473086574'

# Extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Pantry and Recipe Logic


pantry_items = []

""" pantry_items = []
recipes = [
    {"name": "Carbonara", "ingredients": ["Tagliatelle", "egg", "parmesan", "bacon", "black pepper"]},
    {"name": "French Toast", "ingredients": ["Bread", "egg", "milk", "cinnamon", "butter"]},
    {"name": "Sandwich", "ingredients": ["Bread", "butter", "lettuce", "Ketchup", "Mayonaise", "Beef"]}
] """

with open('static/recipes_data.json', 'r') as f:
    recipe_data = json.load(f)
    recipes = recipe_data['recipes']  # Adjust depending on structure

ALL_INGREDIENTS = set()
for r in recipes:
    for ing in r.get("ingredients", []):
        ALL_INGREDIENTS.add(ing)

# Create DB Tables
with app.app_context():
    db.create_all()


# Routes
@app.route('/')
def index():
    return render_template('userCreate.html')


@app.route('/mainmenu')
def mainmenu():
    if 'username' not in session:
        return redirect('/')
    return render_template('MainMenu.html', username=session['username'])


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/pantry')
def pantry_page():
    if 'username' not in session:
        return redirect('/')
    return render_template('pantry.html')


@app.route('/timer')
def timer():
    if 'username' not in session:
        return redirect('/')
    return render_template('timer.html')


@app.route('/shoppinglist')
def shoppinglist():
    return render_template('shoppinglist.html')


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if data['password'] != data['RepeatPassword']:
        return jsonify({'message': 'Passwords do not match.'}), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists.'}), 400
    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'success': True, 'message': 'User registered successfully.'})


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        session['user_id'] = user.id
        session['username'] = user.username
        return jsonify({'success': True, 'message': 'Login successful'})
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401


# Pantry API
@app.route('/api/pantry', methods=['GET'])
def get_pantry():
    return jsonify({"pantry": pantry_items})


@app.route('/api/pantry/add', methods=['POST'])
def add_ingredient():
    data = request.get_json()
    ingredient = data.get('ingredient')
    if ingredient:
        pantry_items.append(ingredient)
        return jsonify({"message": f"{ingredient} added to pantry."}), 201
    return jsonify({"error": "No ingredient provided."}), 400


def normalize(ingredient):
    return ingredient.strip().lower()


@app.route('/api/pantry/remove', methods=['POST'])
def remove_ingredient():
    data = request.get_json()
    ingredient = data.get('ingredient')
    if ingredient and ingredient in pantry_items:
        pantry_items.remove(ingredient)
        return jsonify({"message": f"{ingredient} removed from pantry."}), 200
    return jsonify({"error": "Ingredient not found in pantry."}), 404


@app.route('/api/recipes/from-pantry', methods=['GET'])
def get_recipes_from_pantry():
    matching_recipes = []
    for recipe in recipes:
        recipe_ingredients = [i.lower() for i in recipe.get('ingredients', [])]
        for pantry_item in pantry_items:
            if pantry_item.lower() in recipe_ingredients:
                matching_recipes.append(recipe)
                break
    print("Matching recipes:", matching_recipes)  # Debug output
    return jsonify({"matching_recipes": matching_recipes})


# Add a new route to show recipe details:
@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    return jsonify({"recipes": recipes})


@app.route('/recipes')
def all_recipes():
    if 'username' not in session:
        return redirect('/')
    return render_template('recipes.html', recipes=recipes)


@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    recipe = next((r for r in recipes if r['id'] == recipe_id), None)
    if recipe:
        return render_template('recipe_detail.html', recipe=recipe)
    return "Recipe not found", 404


@app.route("/api/ingredients/search")
def ingredient_search():
    q = request.args.get("q", "").strip().lower()
    if not q:
        return jsonify(suggestions=[])
    matches = [ing for ing in ALL_INGREDIENTS if q in ing.lower()]
    return jsonify(suggestions=matches[:10])     # first 10 matches only


# Run server
if __name__ == '__main__':
    app.run(debug=True, port=8080)
