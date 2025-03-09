from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# ✅ Define an empty list to store pantry items
pantry_items = []  

@app.route('/')
def home():
    return render_template('index.html', pantry=pantry_items)



# ✅ Get all pantry items
@app.route('/api/pantry', methods=['GET'])
def get_pantry():
    return jsonify({"pantry": pantry_items})

# ✅ Add an item to the pantry
@app.route('/api/pantry/add', methods=['POST'])
def add_pantry_item():
    data = request.json
    item = data.get("item")  # Get item name from request body

    if not item:
        return jsonify({"error": "Item name is required"}), 400

    pantry_items.append(item)  # ✅ Append item to the list
    return jsonify({"message": f"'{item}' added to pantry!", "pantry": pantry_items}), 201

# ✅ Clear all pantry items
@app.route('/api/pantry/clear', methods=['DELETE'])
def clear_pantry():
    pantry_items.clear()  # ✅ Clear the list
    return jsonify({"message": "Pantry cleared!"}), 200

if __name__ == '__main__':
    app.run(debug=True)