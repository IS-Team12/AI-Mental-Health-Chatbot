import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env if in development
load_dotenv()

# Set up OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_gpt(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ]
        )
        answer = response.choices[0].message['content']
        return answer
    except openai.error.OpenAIError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

if __name__ == "__main__":
    print("GPT Chatbot - Type 'quit' to exit")
    while True:
        question = input("You: ")
        if question.lower() == "quit":
            break
        response = ask_gpt(question)
        print("Bot:", response)
