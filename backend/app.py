from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/endpoint', methods=['GET', 'POST'])
def api_endpoint():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing input string'}), 400

    input_str = data['text']

    print(input_str)

    return {'message': 'Hello, World!'}

if __name__ == '__main__':
    app.run(debug=True)