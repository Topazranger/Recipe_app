from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# ✅ Define an empty list to store pantry items
pantry_items = []  

recipes = [
    {
        "name": "Carbonara",
        "ingredients": ["Tagliatelle", "egg", "parmesan", "bacon", "black pepper"]
    },
    {
        "name": "French Toast",
        "ingredients": ["Bread", "egg", "milk", "cinnamon", "butter"]
    },
    {
        "name": "Sandwich",
        "ingredients": ["Bread", "butter", "lettuce", "Ketchup", "Mayonaise", "Beef"]
    }
]

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
        if any(ingredient in pantry_items for ingredient in recipe['ingredients']):
            matching_recipes.append(recipe)

    if not matching_recipes:
        return jsonify({"message": "No recipes found with current pantry items.", "matching_recipes": []})

    return jsonify({"matching_recipes": matching_recipes})

@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    return jsonify({"recipes": recipes})

if __name__ == '__main__':
    app.run(debug=True)