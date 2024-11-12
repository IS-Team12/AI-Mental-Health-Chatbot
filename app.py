from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Check if JSON data is received
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid JSON"}), 400
        question = data.get("question", "")

        if not question:
            return jsonify({"error": "No question provided"}), 400

        # Mock response without OpenAI API
        answer = "This is a mock response. Replace this with actual AI logic when available."
        return jsonify({"answer": answer})
    
    except Exception as e:
        print("General Error:", str(e))
        return jsonify({"error": "An internal error occurred", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
