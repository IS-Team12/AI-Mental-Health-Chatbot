from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env if in development
load_dotenv()

app = Flask(__name__)

# Load OpenAI API Key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEYsk-proj-uy3UkYMrPjCAMR_MEkasct9nOq0K5i_McP16oMID-bYst36pylVmOkx3YFEUG-BAc99RbtCl0_T3BlbkFJE3lEpLLtPWiMo7ETTlPFIVRJuB88l8xz_Rlnp5bZSN4zcgyDvDzFQQ5S95Tv199kpXqi0EwRMA")

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

        # Attempt OpenAI API call
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ]
        )
        answer = response.choices[0].message['content'].strip()
        return jsonify({"answer": answer})
    
    except openai.error.OpenAIError as api_error:
        print("Error with OpenAI API:", str(api_error))
        return jsonify({"error": "OpenAI API error", "details": str(api_error)}), 500
    except Exception as e:
        print("General Error:", str(e))
        return jsonify({"error": "An internal error occurred", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
