from flask import Flask, request, jsonify
import spacy

app = Flask(__name__)

# Load or download SpaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # Download the model if not present
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

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

        # Process question with SpaCy NLP
        doc = nlp(question)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        tokens = [token.text for token in doc]

        response_data = {
            "entities": entities,
            "tokens": tokens,
            "original_question": question,
            "message": "Processed with SpaCy NLP"
        }
        return jsonify(response_data)
    
    except Exception as e:
        print("General Error:", str(e))
        return jsonify({"error": "An internal error occurred", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
