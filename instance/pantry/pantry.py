from flask import Flask, jsonify, request, render_template
import json
import os

app = Flask(__name__)

# Load recipes from a JSON file
with open(os.path.join(os.path.dirname(__file__), 'recipes.json'), 'r', encoding='utf-8') as file:
    data = json.load(file)
    recipes = data.get('recipes', [])

# In-memory pantry (no database)
pantry_items = []


@app.route('/')
def home():
    return render_template('index.html', pantry=pantry_items, recipes=recipes)


@app.route('/api/pantry/add', methods=['POST'])
def add_ingredient():
    data = request.get_json()
    ingredient = data.get('ingredient')
    if ingredient:
        pantry_items.append(ingredient)
        return jsonify({"message": f"{ingredient} added to pantry."}), 201
    return jsonify({"error": "No ingredient provided."}), 400


@app.route('/api/pantry', methods=['GET'])
def get_pantry():
    return jsonify({"pantry": pantry_items})


@app.route('/api/recipes/from-pantry', methods=['GET'])
def get_recipes_from_pantry():
    matching_recipes = []
    for recipe in recipes:
        if any(ingredient.lower() in [item.lower() for item in pantry_items] for ingredient in recipe['ingredients']):
            matching_recipes.append(recipe)
    return jsonify({"matching_recipes": matching_recipes})


@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    return jsonify({"recipes": recipes})


@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    recipe = next((r for r in recipes if r['id'] == recipe_id), None)
    if recipe:
        return render_template('recipe_detail.html', recipe=recipe)
    return "Recipe not found", 404


@app.route('/api/pantry/remove', methods=['POST'])
def remove_ingredient():
    data = request.get_json()
    ingredient = data.get('ingredient')
    if ingredient and ingredient in pantry_items:
        pantry_items.remove(ingredient)
        return jsonify({"message": f"{ingredient} removed from pantry."}), 200
    return jsonify({"error": "Ingredient not found in pantry."}), 404


print("Registered routes:")
for rule in app.url_map.iter_rules():
    print(rule)


if __name__ == '__main__':
    app.run(debug=True)
