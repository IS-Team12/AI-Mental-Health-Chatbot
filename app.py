from flask import Flask, render_template, request, redirect, url_for
import nltk
from nltk.stem import WordNetLemmatizer
import numpy as np
import pickle
import json
import random
from keras.models import load_model

# Initialize Flask app
app = Flask(__name__)

# Load necessary files
lemmatizer = WordNetLemmatizer()
model = load_model('model.h5')  # Trained chatbot model
intents = json.loads(open('intents.json').read())
words = pickle.load(open('texts.pkl', 'rb'))
classes = pickle.load(open('labels.pkl', 'rb'))


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


def bow(sentence, words):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return np.array(bag)


def predict_class(sentence, model):
    p = bow(sentence, words)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return [{"intent": classes[r[0]], "probability": str(r[1])} for r in results]


def get_response(ints, intents_json):
    if ints:
        tag = ints[0]['intent']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if i['tag'] == tag:
                return random.choice(i['responses'])
    return "Sorry, I didn't understand that."


def chatbot_response(msg):
    res = get_response(predict_class(msg, model), intents)
    return res


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # Collect user input from the form
        first_name = request.form.get("first-name")
        last_name = request.form.get("last-name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        zip_code = request.form.get("zip-code")

        print(f"First Name: {first_name}, Last Name: {last_name}, Age: {age}, Gender: {gender}, Zip Code: {zip_code}")

        # Redirect to chatbot page
        return redirect(url_for("chatbot"))

    return render_template("signup.html")


@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    if not userText:
        return "Please provide a message."
    return chatbot_response(userText)


if __name__ == "__main__":
    app.run(debug=True)
