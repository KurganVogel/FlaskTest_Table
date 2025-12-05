from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = 'data.json'

# Load existing data or start fresh
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as f:
        try:
            data_store = json.load(f)
        except json.JSONDecodeError:
            data_store = {}
else:
    data_store = {}


@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Flask server is up and running'}), 200


@app.route('/submit', methods=['POST'])
def submit():
    global data_store
    content = request.get_json()

    if not content:
        return jsonify({'error': 'Invalid or missing JSON data'}), 400

    # Each key = user ID; each value = full table replacement
    for user_id, table in content.items():

        # Validate table type
        if not isinstance(table, list):
            return jsonify({'error': f'Table for {user_id} must be a list'}), 400

        # Validate rows within table
        for row in table:
            if not isinstance(row, dict):
                return jsonify({'error': f'Each row in {user_id} table must be a JSON object'}), 400

        # Replace user’s table entirely
        data_store[user_id] = table

    # Save updated data
    with open(DATA_FILE, 'w') as f:
        json.dump(data_store, f, indent=4)

    return jsonify({
        'message': 'Table(s) saved successfully.',
        'current_data': data_store
    }), 200


@app.route('/data', methods=['GET'])
def get_all_data():
    return jsonify({'current_data': data_store}), 200


@app.route('/data/<user_id>', methods=['GET'])
def get_user_table(user_id):
    if user_id in data_store:
        return jsonify({user_id: data_store[user_id]}), 200
    else:
        return jsonify({'error': 'User not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
