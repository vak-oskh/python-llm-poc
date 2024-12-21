from flask import Flask, request, jsonify
from flask_cors import CORS
from call_gpt import query_llm


# Using new function because flask is changing string to byte code
def business_logic(user_text):
    # For loop to grab functions
    functions_list = "Play music('song name'), Play video('movie name')"

    # Call GPT API
    query_llm(user_text, functions_list)

    # Run Function

    return "OK"

app = Flask(__name__)
CORS(app)

@app.route('/api/endpoint', methods=['GET', 'POST'])
def api_endpoint():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing input string'}), 400

    output_str = business_logic(data['text'])


    return {'message': 'Hello, World!'}



if __name__ == '__main__':
    app.run(debug=True)