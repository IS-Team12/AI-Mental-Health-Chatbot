from flask import Flask, request, jsonify
import spacy
import subprocess
import sys

app = Flask(__name__)

# Ensure the 'en_core_web_sm' SpaCy model is installed
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Model 'en_core_web_sm' not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
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

        # Process the question using SpaCy for NLP
        doc = nlp(question)
        entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
        response = {
            "original_text": question,
            "entities": entities,
            "tokens": [{"text": token.text, "lemma": token.lemma_, "pos": token.pos_} for token in doc]
        }
        return jsonify(response)
    
    except Exception as e:
        print("General Error:", str(e))
        return jsonify({"error": "An internal error occurred", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
